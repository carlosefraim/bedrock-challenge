
## Descripción

Su objetivo es analizar el texto o audio de diferentes tipos de archivos, el cual te proporcionará un resumen y del contenido del resumen te generará de 1 a 5 temas principales en el idioma que tu elijas tanto el resumen y los temas.


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

3. configurar de las constantes a usar de AWS del archivo de app/constants.py

- region = 'us-east-1' #REEMPLAZAR CON SU PROPIA REGIÓN DE AWS
- s3_bucket = 'bedrock-carlos-file' #REEMPLAZAR CON SU PROPIA AMAZON S3 BUCKET
- s3_prefix = 'temp/file' #REEMPLAZAR CON SU PROPIA AMAZON S3 BUCKET PREFIX


4. Ejecutar proyecto:
```
streamlit run app\content_analyzer.py
```

4. Desactivar el entorno virtual:
```
deactivate
```

