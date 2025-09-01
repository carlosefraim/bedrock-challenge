import json
import boto3
from pypdf import PdfReader
import os
import constants
import speech_recognition as sr


s3 = boto3.client(service_name='s3',region_name=constants.region)
boto3_bedrock = boto3.client(service_name='bedrock-runtime',region_name='us-east-1')


def call_anthropic(query):
    """Construye el prompt que se enviará al modelo de lenguaje en Bedrock.
    Args:
        -query: pregunta a pocesar al Prompt

    Returns:
        str:
            respuesta optenida del Prompt en formato de texto listo.
    """
    prompt_data = f"""Human: {query} Assistant:"""
    body = json.dumps({
        "prompt": prompt_data,
        "max_tokens_to_sample":8000,
        "temperature":0,
        "top_p":0.9
    })
    modelId = 'anthropic.claude-v2'
    #modelId = 'anthropic.claude-instant-v1'
    response = boto3_bedrock.invoke_model(body=body, modelId=modelId)
    response_body = json.loads(response.get('body').read())
    outputText = response_body.get('completion')
    return outputText


def upload_get_summary(file_type, s3_file_name, language):
    """Carga el archivo almacenado y en base al archivo se procesara para obtener el resumen deseado medilante la funcion call_anthropic()

    Args:
        -type_file: tipo de archivo
        -s3_file_name: archivo
        -language: idioma

    Returns:
        str:
            respuesta optenida del Prompt en formato de texto .
    """
    summary = ''
    s3.download_file(constants.s3_bucket, constants.s3_prefix+'/'+s3_file_name, s3_file_name)
    if file_type == 'pdf':
        contents = read_pdf(s3_file_name)
        new_contents = contents[:50000].replace("$","\\$")
    elif file_type in ['mp3','wav']:
        contents = transcribir_audio(s3_file_name)
        new_contents = contents[:50000].replace("$","\\$")
    else:
        with open(s3_file_name, 'rb') as f:
            contents = f.read()
        new_contents = contents[:50000].decode('utf-8')
    if constants.model.lower() == 'anthropic claude':  
        generated_text = call_anthropic('Create a 300-word summary of the following text '+ new_contents+' in ' +language)
        if generated_text != '':
            summary = str(generated_text)+' '
            summary = summary.replace("$","\\$")
        else:
            summary = 'Claude did not find an answer to your question, please try again'
    if os.path.exists(s3_file_name):
        os.remove(s3_file_name)
    return new_contents, summary    


def read_pdf(filename):
    """Lee el contenido del archivo pdf 

    Args:
        -filename: archivo

    Returns:
        str:
            retona el texto obtenido de la lectura.
    """
    reader = PdfReader(filename)
    raw_text = []
    for page in reader.pages:
        raw_text.append(page.extract_text())
    return '\n'.join(raw_text)



def transcribir_audio(filename):
    """transcribe el un archivo de audio a texto

    Args:
        -filename: archivo

    Returns:
        str:
            retona el texto obtenido.
    """
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)  
    try:
        text = r.recognize_google(audio, language='es') 
        return text
    except sr.UnknownValueError:
        return None
        
    