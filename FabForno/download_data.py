import requests

def download_file_from_google_drive(file_id, destination):
    # URL base de descarga directa
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Iniciar la sesión
    session = requests.Session()

    # Hacer la solicitud inicial para obtener los posibles cookies y redirecciones
    response = session.get(URL, stream=True)

    # Comprobar si se requiere una confirmación para proceder con la descarga (cuando es un archivo grande)
    if 'confirm' in response.cookies:
        # Obtener el token de confirmación de la cookie
        confirm = response.cookies['confirm']
        # Volver a hacer la solicitud, pasando el token de confirmación
        response = session.get(URL + "&confirm=" + confirm, stream=True)

    # Guardar el archivo en la ubicación especificada
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

    print(f"Archivo descargado en: {destination}")

# ID del archivo de Google Drive (extraído del enlace)
file_id = '1BUcl9T1Z9_BJo7c64tSSkkyCNJholImF'  # Sustituye esto con el ID real
destination = 'fabforno_live.csv'  # Nombre o ruta del archivo donde deseas guardar

download_file_from_google_drive(file_id, destination)

#a = 'https://drive.google.com/file/d/16LPV6DA0VUWwkMQPPNhnbU8slH4sikyG/view?usp=drive_link'
#a = 'https://drive.google.com/file/d/1BUcl9T1Z9_BJo7c64tSSkkyCNJholImF/view?usp=sharing