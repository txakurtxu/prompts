import os
import json
import google.generativeai as genai
from urllib.parse import quote, unquote

from dotenv import load_dotenv
load_dotenv()

from lib.lib_class import create_class

def streamGem(json_data):
    mova = json_data["mova"]
    tapr = unquote(json_data["tapr"])
    tach = unquote(json_data["tach"])
    tasc = unquote(json_data["tasc"])

    genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
    try:
        singDiag = create_class("geminiClass", tasc)
        generation_config = {
          "temperature": 0,
          "top_p": 0.95,
          "top_k": 40,
          "max_output_tokens": 8192 * 2,
          "response_mime_type": "application/json",
          "response_schema": list[singDiag],
        }

        model = genai.GenerativeModel(
          model_name = mova,
          generation_config = generation_config,
          system_instruction = tapr,
        )

        response = model.generate_content("Clinical case: " + tach + "\nPlease reply using the same language as the clinical case.", stream = True)
    except Exception as e:
        print(f'*** Gemini error:\nerror: {e}')
        return f'{e}'

    for part in response:
        #print(f'{part.text}')
        yield part.text

    return "Empty response!"
