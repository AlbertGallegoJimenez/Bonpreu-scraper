# Bonpreu-scraper
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.14036298.svg.svg)](https://doi.org/10.5281/zenodo.14036298)


## Descripción del repositorio

Este repositorio contiene el código para realizar _web scraping_ para obtener datos de productos a la venta en la empresa de alimentación BonpreuEsclat.

<div align="center">
      <img src="image.png" width="50%">
</div>

El producto final de este proyecto se almacena en la carpeta [data](/data) en formato CSV, que incluye información detallada sobre los productos en venta.
<br>Para obtener más información sobre el enfoque metodológico utilizado, la estructura del conjunto de datos resultante y otros detalles relevantes, consulta la documentación disponible en la carpeta [docs](/docs).

Este proyecto se presenta como la Práctica 1 de la asignatura M2.851 - Tipología y Ciclo de Vida de los Datos del Máster de Data Science de la UOC.

## Estructura del repositorio

- 📂 [**data**](/data): Carpeta con datos obtenidos de la práctica.
  - 📄[**bonpreu_products_20241104_173704.csv**](/data/bonpreu_products_20241104_173704.csv): Dataset resultante de ejecutar el programa.
- 📂 [**docs**](/docs): Carpeta con archivos de documentación.
  - 📝[**PR1_Memoria_Roldan_Gallego.pdf**](/src/main.py): Memoria de la práctica.
- 📂 [**src**](/src): Carpeta con el código fuente.
  - 📄[**main.py**](/src/main.py): Script principal para ejecutar el scraper.
  - 📄[**scraper.py**](/src/scraper.py): Define la clase ``BonpreuScraper`` con las funciones principales de scraping.
  - 📄[**merge_csv.py**](/src/merge_csv.py): Script que automatiza la fusión de los CSVs exportados por categorías en un solo archivo CSV llamado ``bonpreu_products_YYYYmmdd_HHMMSS.csv``.
- 📂 [**tests**](/tests): Pruebas automatizados.
  - 📄[**test_scraper.py**](/tests/test_scraper.py): Script que contiene varias pruebas unitarias del scraper. 
- 📄 **environment.yml**: Archivo YML para instalar un environment de Anaconda igual que el usado para el desarrollo del proyecto.
- 🖼️ **imagen.png**: Imagen que contiene el logo de BonpreuEsclat.
- 📄 **LICENSE**: Archivo de licencia.
- 📄 **requirements.txt**: Un archivo de requirements donde se detallan las librerías utilizadas con sus respectivas versiones.
- 📄 **README.md**: Este mismo archivo README.

## Instalación

0. Si usas [Anaconda](https://www.anaconda.com/) puedes crear un **environment** directamente desde el archivo **environment.yml** de la siguiente forma:
      ``` bash
      conda env create --file environment.yml
      conda activate web_scraping_env
      ```
   Este environment ya tiene especificada tanto la versión de Python utilizada, como las librerías de las que depende. De esta forma, puedes saltarte el siguiente paso. 
   <br>

1. Si no usas Anaconda y/o no tienes instaladas las librerías usadas en el programa, usa:
      ``` bash
      pip install -r requirements.txt
      ```

## Cómo ejecutar el proyecto?

El proyecto se ejecuta desde el script principal (``main.py``) a través de consola. A continuación, se detallan las opciones de ejecución disponibles.

### 0.1. Listar las categorías disponibles

Para ver todas las categorías que se pueden seleccionar, utiliza el siguiente comando:

```bash
python main.py --list-categories
```
Este comando **solo muestra las categorías disponibles**.

### 0.2. Listar las subcategorías disponibles

Para ver todas las subcategorías que se pueden seleccionar de una categoría, utiliza el siguiente comando:

```bash
python main.py --category <NOMBRE_CATEGORÍA> --list-subcategories
```
Este comando **solo muestra las subcategorías disponibles** de una categoría dada.

> [!IMPORTANT]
> Para conocer qué subcategorías hay disponibles, es necesario proporcionar una única categoría. También devolverá error si se usa la opción de "todas las categorías" (--category all).

### 1. Ejecutar el scraper en una categoría completa

Para ejecutar el scraper en una **categoría completa** (es decir, en todas sus subcategorías), usa:

```bash
python main.py --category <NOMBRE_CATEGORÍA>
```

Ejemplo:

```bash
python main.py --category Frescos
```

### 2. Ejecutar el scraper en subcategorías específicas

Para ejecutar el scraper en **subcategorías específicas**, usa:

```bash
python main.py --category <NOMBRE_CATEGORÍA> --subcategories <SUBCATEGORÍA_1> <SUBCATEGORÍA_2>
```

Ejemplo:

```bash
python main.py --category Frescos --subcategories "Fruites i verdura" "Xarcuteria"
```

De la misma forma también se pueden ejecutar **varias categorías a la vez**, aunque en este caso **no se podrán especificar subcategorías** específicas de cada cateogoría.

### 3. Ejecutar el scraper en todas las categorías

Para ejecutar el scraper en **todas las categorías** disponible, usa:

```bash
python main.py --category all
```

Este comando ejecutará el scraper en todas las categorías y sus subcategorías.

> [!CAUTION]
>Si seleccionas la opción de "todas las categorías" (`--category all`), utiliza el programa de forma responsable. Aunque el código implementa medidas para evitar la sobrecarga del servidor (como tiempos de espera), es importante moderar el uso para no saturar los recursos del sitio web de Bonpreu.

### 4. Fusionar CSVs exportados

Para **fusionar varios CSVs** exportados por categorías en un solo archivo CSV, usa:

```bash
python merge_csv.py
```

Ten en cuenta que este script identifica **todos los CSVs** presentes en la carpeta [data](/data) (con excepción a posibles archivos fusionados anteriores) y junta todos los registros en un archivo resultante llamado ``bonpreu_products_YYYYmmdd_HHMMSS.csv``.

## DOI del dataset generado

El dataset generado está publicado en [Zenodo](https://zenodo.org/) con el título: "".

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.14036298.svg.svg)](https://doi.org/10.5281/zenodo.14036298)


## Colaboradores
Este repositorio ha sido desarrollado por:
- 👨‍💻 David Roldán Puig
- 👨‍💻 Albert Gallego Jiménez