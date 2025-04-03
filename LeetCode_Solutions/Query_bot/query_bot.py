from IPython.display import display, Markdown, HTML
import requests

def query_ollama(querry, system_prompt="You are a Python expert specializing in algorithm implementation", model="llama3.2"):
    """Query the local Ollama API directly"""
    url = "http://localhost:11434/api/chat"

    prompt = """
        You are a highly skilled code assistant. Your task is to analyze the given request and provide a code snippet that fulfills the requirements. 
        Ensure the output is in JSON format with the following structure:
        {
            "code": "the Python code snippet that satisfies the request",
            "response_text": "a detailed explanation of the code and how it addresses the request"
        }

        Please ensure the code is well-documented, follows best practices, and includes comments where necessary.
        """
    prompt += f"""
        Request:
        {querry}
    """
    
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
    # return 
