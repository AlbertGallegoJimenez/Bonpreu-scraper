# web-scraping-pr1

## Descripción del repositorio

## Estructura de la carpeta

- 📂 **data**: Los datos obtenidos de la práctica.
- 📂 **docs**: Archivos de documentación.
- 📂 **src**: Código fuente.
- 📂 **tests**: Tests automatizados.
- 📄 **environment.yml**: Archivo YML para instalar un environment de Anaconda igual que el usado para el desarrollo del proyecto.
- 📄 **LICENSE**: Archivo de licencia.
- 📄 **requirements.txt**: Un archivo de requirements donde se detallan las librerías utilizadas con sus respectivas versiones.
- 📄 **README.md**: Este mismo archivo README.

## Cómo ejecutar el proyecto?

0. Si usas [Anaconda](https://www.anaconda.com/) puedes crear un **environment** directamente desde el archivo **environment.yml** de la siguiente forma:
      ``` bash
      conda env create --file environment.yml
      conda activate web_scraping_env
      ```
   Este environment ya tiene especificada tanto la versión de Python utilizada, como las librerías de las que depende. De esta forma, puedes saltarte el siguiente paso e **ir directamente al 2**. 


1. Si no usas Anaconda y/o no tienes instaladas las librerías usadas en el programa:
      ``` bash
      pip install -r requirements.txt
      ```
   
2. Ejecutar el **script principal desde consola**(``main.py``):
      ``` bash
      python3 main.py
      ```

Importante:
> ⚠️ **Si usas Windows**: reemplaza "python3" por "python".

## Colaboradores
Este repositorio ha sido desarrollado por:
- 👨‍💻 David Roldán Puig
- 👨‍💻 Albert Gallego Jiménez