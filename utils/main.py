import os
import subprocess
import sys
import requests
import winreg as reg
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_pytesseract_installed():
    try:
        import pytesseract
        return True
    except ImportError:
        return False

def install_pytesseract():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])
        logging.info("Pytesseract instalado correctamente.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al instalar Pytesseract: {e}")
        return False

def download_tesseract():
    url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open("tesseract-setup.exe", "wb") as file:
            file.write(response.content)
        logging.info("Tesseract descargado correctamente.")
        return True
    except requests.RequestException as e:
        logging.error(f"Error al descargar Tesseract: {e}")
        return False

def install_tesseract():
    if os.path.exists("tesseract-setup.exe"):
        try:
            subprocess.run(["tesseract-setup.exe", "/SILENT"], check=True)
            logging.info("Tesseract instalado correctamente.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al instalar Tesseract: {e}")
            return False
    else:
        logging.error("El archivo de instalación de Tesseract no se encontró.")
        return False

def add_tesseract_to_path():
    user = os.getlogin()
    tesseract_path = f"C:\\Program Files\\Tesseract-OCR\\"
    tessdata_prefix = f"{tesseract_path}\\tessdata\\"

    try:
        # Obtener las variables de entorno actuales
        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, reg.KEY_ALL_ACCESS)
        path, _ = reg.QueryValueEx(key, "Path")
        
        # Añadir Tesseract al PATH si no está ya
        if tesseract_path not in path:
            new_path = f"{path};{tesseract_path}"
            reg.SetValueEx(key, 'Path', 0, reg.REG_EXPAND_SZ, new_path)
        
        # Establecer TESSDATA_PREFIX
        reg.SetValueEx(key, 'TESSDATA_PREFIX', 0, reg.REG_EXPAND_SZ, tessdata_prefix)
        
        reg.CloseKey(key)
        logging.info("Rutas añadidas al PATH y TESSDATA_PREFIX configurado.")
        return True
    except Exception as e:
        logging.error(f"Error al modificar las variables de entorno: {e}")
        return False

def main():
    if not is_pytesseract_installed():
        logging.info("Instalando Pytesseract...")
        if not install_pytesseract():
            return
    else:
        logging.info("Pytesseract ya está instalado.")

    logging.info("Descargando Tesseract...")
    if download_tesseract() and install_tesseract():
        logging.info("Configurando variables de entorno...")
        if add_tesseract_to_path():
            logging.info("Instalación y configuración completadas. Por favor, reinicia tu computadora para aplicar los cambios.")
        else:
            logging.warning("La instalación se completó, pero hubo problemas al configurar las variables de entorno.")
    else:
        logging.error("No se pudo completar la instalación de Tesseract.")

if __name__ == "__main__":
    main()
