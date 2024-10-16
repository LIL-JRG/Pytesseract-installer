@ECHO OFF

echo Instalando las dependencias necesarias, por favor espere...
cd utils
pip install -r requirements.txt > nul
echo Listo, comenzando con la instalación de Pytesseract...
python main.py

pause
