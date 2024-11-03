# web-scraping-pr1

## Descripción del repositorio

Este repositorio contiene el código para realizar _web scraping_ sobre la empresa de alimentación BonpreuEsclat.

<div align="center">
      <img src="image.png" width="50%">
</div>

El producto final de este proyecto se almacena en la carpeta [data](/data) en formato CSV, que incluye información detallada sobre los productos en venta.
<br>Para obtener más información sobre el enfoque metodológico utilizado, la estructura del conjunto de datos resultante y otros detalles relevantes, consulta la documentación disponible en la carpeta [docs](/docs).

Este proyecto se presenta como la Práctica 1 de la asignatura M2.851 - Tipología y Ciclo de Vida de los Datos del Máster de Data Science de la UOC.

## Estructura de la carpeta

- 📂 [**data**](/data): Los datos obtenidos de la práctica.
- 📂 [**docs**](/docs): Archivos de documentación.
- 📂 [**src**](/src): Código fuente.
- 📂 [**tests**](/tests): Tests automatizados.
- 📄 **environment.yml**: Archivo YML para instalar un environment de Anaconda igual que el usado para el desarrollo del proyecto.
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

1. Si no usas Anaconda y/o no tienes instaladas las librerías usadas en el programa:
      ``` bash
      pip install -r requirements.txt
      ```

## Cómo ejecutar el proyecto?

El proyecto se ejecuta desde el script principal (``main.py``) desde consola. A continuación, se detallan las opciones de ejecución disponibles.

### 0.1. Listar las categorías disponibles

Para ver todas las categorías que se pueden seleccionar, utiliza el siguiente comando:

```bash
python main.py --list-categories
```
Este comando solo muestra las categorías disponibles.

### 0.2. Listar las categorías disponibles

```bash
python main.py --category <NOMBRE_CATEGORÍA> --list-subcategories
```
Este comando solo muestra las subcategorías disponibles de una categoría dada.

### 1. Ejecutar el scraper en una categoría completa

Para ejecutar el scraper en una categoría completa (es decir, en todas sus subcategorías), usa:

```bash
python main.py --category <NOMBRE_CATEGORÍA>
```

Ejemplo:

```bash
python main.py --category Frescos
```

### 2. Ejecutar el scraper en subcategorías específicas

Para ejecutar el scraper en subcategorías específicas, usa:

```bash
python main.py --category <NOMBRE_CATEGORÍA> --subcategories <SUBCATEGORÍA_1> <SUBCATEGORÍA_2>
```

Ejemplo:

```bash
python main.py --category Frescos --subcategories "Fruites i verdura" "Xarcuteria"
```

### 3. Ejecutar el scraper en todas las categorías

Para ejecutar el scraper en todas las categorías disponible, usa:

```bash
python main.py --category all
```

Este comando ejecutará el scraper en todas las categorías y sus subcategorías.

> [!CAUTION]
>Si seleccionas la opción de "todas las categorías" (`--category all`), utiliza el programa de forma responsable. Aunque el código implementa medidas para evitar la sobrecarga del servidor (como tiempos de espera), es importante moderar el uso para no saturar los recursos del sitio web de Bonpreu.


## Colaboradores
Este repositorio ha sido desarrollado por:
- 👨‍💻 David Roldán Puig
- 👨‍💻 Albert Gallego Jiménez
