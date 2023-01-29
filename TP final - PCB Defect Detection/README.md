Set up (Windows cmd)

1. Crear un entorno virtual (recomendado) e instalar las librerías necesarias:

    `python -m venv venv`

    `.\venv\Scripts\activate`

    `pip install -r ".\TP final - PCB Defect Detection\requirements.txt"`

2. Bajar el token para la API de Kaggle (https://www.kaggle.com/docs/api). Luego bajar la base de datos (1.88GB):

    `cd "TP final - PCB Defect Detection"`

    `kaggle datasets download -d akhatova/pcb-defects`

    `tar -xf pcb-defects.zip`

    `del pcb-defects.zip`