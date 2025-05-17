import requests 
import json
from core.config import OPENROUTER_API_KEY, OPENROUTER_API_URL, MODEL_NAME, MAX_HISTORY_LENGTH, TEMPERATURE, MAX_TOKENS

def call_llama_api(messages, system_prompt=None):
    header={
        "Authorization": f"Bearer {'OPENROUTER_API_KEY'}" , # this is the api key, this is the first step, who you are
        "Content-type" : "application/json", #how you are speaking 
        "http-referer": "https://localhost:8000", #where you are coming from
        "x-title": "Airline-Agent"

    }
    conversation=[]
    if system_prompt:
        conversation.append({"role":"system","content":system_prompt})

    for message in messages:
        conversation.append({"role":message["role"], "content": message["content"]})

    payload={
        "model": MODEL_NAME,
        "messages":conversation,
        "temperature":TEMPERATURE,
        "max_tokens":MAX_TOKENS,

    }
    try:
        response = requests.post(OPENROUTER_API_URL,
                               headers=header,
                               data=json.dumps(payload))
        response.raise_for_status()
        response_data=response.json()
        if "choices" in response_data and len(response_data["choices"])>0:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "No response from the model"
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling the API: {e}")
        return "An error occurred while calling the API"






