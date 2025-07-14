import os
import json
from openai import OpenAI
from urllib.parse import quote, unquote

from dotenv import load_dotenv
load_dotenv()

from lib.lib_class import create_class

from pydantic import BaseModel, Field

def streamGPT(json_data):
    mova = json_data["mova"]
    tapr = unquote(json_data["tapr"])
    tach = unquote(json_data["tach"])
    tasc = unquote(json_data["tasc"])
    client = OpenAI(api_key = os.getenv("GPT_API_KEY"))
    kwargs = {}
    try:
        kwargs["model"] = mova
        kwargs["input"] = [
            {
                "role": "system",
                "content": tapr,
            },
            {
                "role": "user",
                "content": "Clinical case: " + tach + "\nPlease reply using the same language as the clinical case.",
            },
        ]
        kwargs["temperature"] = 0.
        if tapr.strip() == "":
            kwargs["input"][1]["content"] = tach

        if tasc.strip() != "":
            try:
                singDiag = create_class("openaiClass", tasc)
                class diffDiag(BaseModel):
                    diagnosis_list: list[singDiag]
                kwargs["text_format"] = diffDiag
            except Exception as e:
                pass

        response = client.responses.parse(**kwargs)

    except Exception as e:
        print(f'*** GPT error:\nerror: {e}')
        return f'{e}'

    try:
        if "text_format" in kwargs:
            ret_val = json.dumps(json.loads(response.output[0].content[0].text)["diagnosis_list"], indent = 2).encode().decode("unicode-escape")
        else:
            ret_val = f'{response.output[0].content[0].text}'
    except Exception as e:
        print(f'Exception converting json: {e}')
        ret_val = f'{response.output[0].content[0].text}'

    return ret_val
