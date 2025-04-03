import pandas as pd
import matplotlib.pyplot as plt
import json
from tqdm import tqdm
import time
import logging
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fragrance_analysis.log'),
        logging.StreamHandler()
    ]
)

def load_checkpoint(checkpoint_file):
    """Load previously processed results from checkpoint"""
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                return json.load(f), True
        except Exception as e:
            logging.warning(f"Could not load checkpoint: {e}")
    return [], False

def save_checkpoint(data, checkpoint_file):
    """Save current progress to checkpoint file"""
    try:
        with open(checkpoint_file, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        logging.error(f"Failed to save checkpoint: {e}")
        return False

def query_ollama(prompt, system_prompt=None, model="llama2"):
    """Query the local Ollama API directly"""
    url = "http://localhost:11434/api/chat"
    
    if system_prompt:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    else:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    
    response = requests.post(url, json=payload)
    response_json = response.json()
    
    if "message" in response_json and "content" in response_json["message"]:
        return response_json["message"]["content"]
    
    return str(response_json)

def analyze_fragrance_notes(row_data):
    """Use Ollama to analyze and extract fragrance notes using all available context"""
    try:
        # Create comprehensive context from available columns
        prompt = f"""
        Analyze this fragrance product:
        Name: {row_data['Product Name']}
        Brand: {row_data['Desc.']}
        Category: {row_data['Category']} ({row_data['Category Group']})
        Size: {row_data['Size']}
        
        Classify the fragrance notes into:
        1. Top Notes
        2. Middle Notes (Heart Notes)
        3. Base Notes
        
        Reply in strict JSON format only:
        {{"top_notes": "notes", "middle_notes": "notes", "base_notes": "notes"}}
        """
        
        response = query_ollama(
            prompt,
            system_prompt="You are a perfumery expert. Provide fragrance analysis in JSON format.",
            model="llama2"
        )
        return json.loads(response.strip())
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        return {
            "top_notes": "Error",
            "middle_notes": "Error",
            "base_notes": "Error"
        }
    except Exception as e:
        logging.error(f"Analysis error: {e}")
        return {
            "top_notes": "Error",
            "middle_notes": "Error",
            "base_notes": "Error"
        }

def process_batch(df_batch, max_workers=3):
    """Process a batch of items in parallel with proper throttling"""
    results = []
    processed_count = 0
    error_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all rows for processing
        future_to_idx = {
            executor.submit(analyze_fragrance_notes, row): idx 
            for idx, row in df_batch.iterrows()
        }
        
        # Process completed futures with progress bar
        with tqdm(total=len(future_to_idx), desc="Processing items") as pbar:
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    result = future.result()
                    results.append((idx, result))
                    
                    if result['top_notes'] != 'Error':
                        processed_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    error_count += 1
                    logging.error(f"Failed to process row {idx}: {str(e)}")
                    results.append((idx, {
                        "top_notes": "Error",
                        "middle_notes": "Error",
                        "base_notes": "Error"
                    }))
                finally:
                    pbar.update(1)
                    pbar.set_postfix({
                        'processed': processed_count,
                        'errors': error_count
                    })
                    
                    # Add delay between requests to avoid overwhelming Ollama
                    time.sleep(1)
    
    logging.info(f"Batch complete - Successfully processed: {processed_count}, Errors: {error_count}")
    return results

def main():
    # Configuration
    input_file = '/Users/sudarshan/Downloads/Grouped_Inventory_by_Category.csv'
    output_file = '/Users/sudarshan/Downloads/Inventory_with_FragranceNotes.csv'
    checkpoint_file = '/Users/sudarshan/Downloads/fragrance_notes_checkpoint.json'
    batch_size = 5  # Smaller batch size for better control
    
    try:
        # Load data
        df = pd.read_csv(input_file)
        logging.info(f"Loaded CSV with {len(df)} rows and columns: {df.columns.tolist()}")
        
        # Verify required columns exist
        required_columns = ['Product Name', 'Desc.', 'Category', 'Category Group', 'Size']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Initialize/load checkpoint
        processed_results, checkpoint_loaded = load_checkpoint(checkpoint_file)
        if checkpoint_loaded:
            logging.info(f"Loaded checkpoint with {len(processed_results)} processed items")
        
        # Create output columns if needed
        if not all(col in df.columns for col in ['Top_Notes', 'Middle_Notes', 'Base_Notes']):
            df['Top_Notes'] = None
            df['Middle_Notes'] = None
            df['Base_Notes'] = None
        
        # Apply any previously processed results from checkpoint
        if checkpoint_loaded and processed_results:
            for idx_str, result in processed_results:
                idx = int(idx_str)  # Convert string index to integer
                if idx < len(df):
                    df.loc[idx, 'Top_Notes'] = result['top_notes']
                    df.loc[idx, 'Middle_Notes'] = result['middle_notes']
                    df.loc[idx, 'Base_Notes'] = result['base_notes']
        
        # Identify rows that need processing (where notes are missing)
        to_process = df[df['Top_Notes'].isna()].index.tolist()
        
        if not to_process:
            logging.info("All rows already processed. Nothing to do.")
            return
            
        logging.info(f"Need to process {len(to_process)} items")
        
        # Process in batches
        all_results = [(str(idx), result) for idx, result in processed_results]
        
        for i in range(0, len(to_process), batch_size):
            batch_indices = to_process[i:i+batch_size]
            batch_df = df.loc[batch_indices]
            
            logging.info(f"Processing batch {i//batch_size + 1}/{(len(to_process) + batch_size - 1)//batch_size}")
            batch_results = process_batch(batch_df)
            
            # Update DataFrame with results
            for idx, result in batch_results:
                df.loc[idx, 'Top_Notes'] = result['top_notes']
                df.loc[idx, 'Middle_Notes'] = result['middle_notes']
                df.loc[idx, 'Base_Notes'] = result['base_notes']
                all_results.append((str(idx), result))  # Add to checkpoint data
            
            # Save progress after each batch
            df.to_csv(output_file, index=False)
            save_checkpoint(all_results, checkpoint_file)
            logging.info(f"Saved progress: {i + len(batch_indices)}/{len(to_process)} items processed")
        
        # Display final statistics
        success_count = len(df[df['Top_Notes'] != 'Error'].dropna())
        error_count = len(df[df['Top_Notes'] == 'Error'])
        not_processed = df['Top_Notes'].isna().sum()
        
        logging.info(f"\nFinal Statistics:\n- Successful: {success_count}\n- Errors: {error_count}\n- Not processed: {not_processed}")
        print(f"\nProcessing complete!\nResults saved to: {output_file}")
        
    except Exception as e:
        logging.error(f"Main process error: {e}")
        raise

if __name__ == "__main__":
    main()