import os
import json
from google import genai
from google.genai import types
from urllib.parse import quote, unquote

from dotenv import load_dotenv
load_dotenv()

from lib.lib_class import create_class

def streamGem(json_data):
    mova = json_data["mova"]
    tapr = unquote(json_data["tapr"])
    tach = unquote(json_data["tach"])
    tasc = unquote(json_data["tasc"])

    client= genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
    try:
        '''
        generation_config = {
          "temperature": 0,
          "top_p": 0.95,
          "top_k": 40,
          "max_output_tokens": 8192 * 2,
          "response_mime_type": "application/json",
        }
        if tasc.strip() != "":
            try:
                singDiag = create_class("geminiClass", tasc)
                generation_config["response_schema"] = list[singDiag]
            except Exception as e:
                pass

        kwargs = {}
        kwargs["model_name"] = mova
        kwargs["generation_config"] = generation_config
        if tapr.strip() != "":
            kwargs["system_instruction"] = tapr
            model = genai.GenerativeModel(**kwargs)
            response = model.generate_content("Clinical case: " + tach + "\nPlease reply using the same language as the clinical case.", stream = True)
        else:
            model = genai.GenerativeModel(**kwargs)
            response = model.generate_content(tach + "\nPlease reply using the same language as above.", stream = True)
        '''
        kwargs= {}
        kwargs["temperature"]= 0
        kwargs["top_p"]= 0.95
        kwargs["top_k"]= 40
        kwargs["max_output_tokens"]= 8192* 2
        kwargs["response_mime_type"]= 'application/json'
        kwargs["thinking_config"]= types.ThinkingConfig(thinking_budget= 1024)
        if tasc.strip()!= "":
            try:
                singDiag= create_class("geminiClass", tasc)
                kwargs["response_schema"]= list[singDiag]
            except Exception as e:
                pass
        if tapr.strip()!= "":
            contents= "Clinical case: " + tach + "\nPlease reply using the same language as the clinical case."
            kwargs["system_instruction"]= tapr
        else:
            contents= tach + "\nPlease reply using the same language as above."
        config= types.GenerateContentConfig(**kwargs)
        for part in client.models.generate_content_stream(model= mova, contents= contents, config= config):
            try:
                yield part.text.encode("utf-8")
            except Exception as e:
                print(f'Gemini exception: {e}')
                yield ''
        
    except Exception as e:
        print(f'*** Gemini error:\nerror: {e}')
        return f'{e}'

    '''
    for part in response:
        try:
            yield part.text.encode("utf-8")
        except Exception as e:
            print(f'Gemini exception: {e}')
            yield ''
    '''

    return "Empty response!"
