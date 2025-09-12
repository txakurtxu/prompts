import base64
def index():
    path= "sm/"
    psx= "XX"
    files= ["styles.css", "js_vars.js", "js_lib.js"]
    fdata= []
    for f in files:
        with open(path+ f) as ff:
            fdata.append(ff.read())
    with open(path+ "index.html") as f:
       rdata= f.read()
    for i in range(len(files)):
        if i!= 1:
            rdata= rdata.replace(psx+ str(i+ 1)+ psx, " ".join(fdata[i].replace("\n", " ").replace("\t", " ").split()));
        else:
            rdata= rdata.replace(psx+ str(i+ 1)+ psx, fdata[i]);
    img_data= base64.b64encode(open(path+ 'knidian.png', 'rb').read()).decode('utf-8')
    rdata= rdata.replace(psx+ str(4)+ psx, "data:image/png;base64, "+ img_data)
    img_data= base64.b64encode(open(path+ 'sanmiguel.png', 'rb').read()).decode('utf-8')
    rdata= rdata.replace(psx+ str(5)+ psx, "data:image/png;base64, "+ img_data)
    return rdata

from lib.lib_class import create_class

import os
import json
from google import genai
from google.genai import types
from urllib.parse import quote, unquote
def qGemini(json_data):
    mova= json_data["mova"]
    tapr= unquote(json_data["tapr"])
    tach= unquote(json_data["tach"])
    tasc= unquote(json_data["tasc"])

    client= genai.Client(api_key = os.getenv("GEMINI_API_KEY"))
    try:
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
                kwargs["response_schema"]= singDiag
            except Exception as e:
                pass
        if tapr.strip()!= "":
            contents= "Clinical case: " + tach + "\nPlease reply using the same language as the clinical case."
            kwargs["system_instruction"]= tapr
        else:
            contents= tach
        config= types.GenerateContentConfig(**kwargs)
        response= client.models.generate_content(model= mova, contents= contents, config= config)
        return json.loads(response.text)
    except Exception as e:
        print(f'*** Gemini error:\nerror: {e}')
        return f'{e}'

    return "Empty response!"

from openai import OpenAI
def qGPT(json_data):
    mova= json_data["mova"]
    tapr= unquote(json_data["tapr"])
    tach= unquote(json_data["tach"])
    tasc= unquote(json_data["tasc"])

    client= OpenAI(api_key= os.getenv("GPT_API_KEY"))
    try:
        kwargs= {}
        kwargs["model"]= mova
        kwargs["input"]= [
            {
                "role": "system",
                "content": tapr,
            },
            {
                "role": "user",
                "content": "Clinical case: " + tach + "\nPlease reply using the same language as the clinical case.",
            },
        ]
        kwargs["temperature"]= 0
        if tapr.strip()== "":
            kwargs["input"][1]["content"]= tach

        if tasc.strip()!= "":
            try:
                singDiag= create_class("openaiClass", tasc)
                kwargs["text_format"]= singDiag
            except Exception as e:
                pass

        response= client.responses.parse(**kwargs)
        r= response.output[0].content[0].text
        return json.loads(r[r.find("{"): r.rfind("}")+ 1])

    except Exception as e:
        print(f'*** chatGPT error:\nerror: {e}')
        return f'{e}'

    return "Empty response!"
