
## Descripción

Su objetivo es que te ayuda a analizar el texto  o audio de distontos tipos de archivos el cual te proporcionara un resumen en el idioma que tu elijas del contenido de 1 a 5 temas pricipales del resumen optenido.


## 📋 Requisitos Previos
- Cuenta AWS con acceso a Amazon Bedrock
- Cuenta AWS con acceso a S3
- Acceso a cuenta AWS con permisos administrativos
- Python 3.12+
- AWS CLI configurado
- Visual Studio Code (recomendado)
- Git

## Inicio Rápido

1. Cree un entorno virtual:
```
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
```

2. Instale las dependencias:
```
python -m pip install -r requirements.txt
```

3. configurar de las constantes a usar de AWS :

Del archivo de app/constants.py

- region = 'us-east-1' #REEMPLAZAR CON SU PROPIA REGIÓN DE AWS
- s3_bucket = 'bedrock-carlos-file' #REEMPLAZAR CON SU PROPIA AMAZON S3 BUCKET
- s3_prefix = 'temp/file' #REEMPLAZAR CON SU PROPIA AMAZON S3 BUCKET PREFIX


3. Ejecutar proyecto:
```
streamlit run app\content_analyzer.py
```

4. Desactivar el entorno virtual:
```
deactivate
```

