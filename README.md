# Script para Adquirir Datos del Portal de Datos Abiertos de la Superintendencia del Mercado de Valores de Perú
Este script está diseñado para adquirir datos del Portal de Datos Abiertos de la Superintendencia del Mercado de Valores de Perú (SMV) utilizando el servicio web proporcionado en la siguiente URL: https://mvnet.smv.gob.pe/ws_od_eeff/WebServiceInfoFinanciera.asmx?wsdl.

## Descripción
Este script permite acceder a los datos financieros proporcionados por la SMV a través de su servicio web. El objetivo es obtener y procesar la información financiera disponible en el portal para su análisis y uso en informes o investigaciones.

## Requisitos
Python: El script está escrito en Python 3.6 o superior.

Bibliotecas: Se requieren las siguientes bibliotecas Python:
    zeep (para interactuar con el servicio web SOAP)
    json (para manejar datos JSON, si es necesario)
    csv (para guardar datos en formato CSV)

Puedes instalar la biblioteca zeep utilizando pip:
```sh
    pip install zeep
```
## Instalación
Clona este repositorio en tu máquina local:
```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
```
# Uso
Edita el rango de años en el script según tus necesidades. Busca las siguientes líneas:
```py
    # Definir el rango de años
    start_year = 2022
    end_year = 2023
```
## Ejemplo de Salida
Al ejecutar el script, se generarán tres archivos en el directorio actual:

Archivo JSON (`respuesta_balance_general_trimestral.json`):
    Contiene la respuesta en formato JSON de las consultas realizadas al servicio web. Este archivo almacena los datos crudos obtenidos del servicio web.

Archivo SQL (`respuesta_balance_general_trimestral.sql`):
    Contiene el script SQL que incluye una sentencia para crear la tabla balance_general si no existe y una serie de sentencias INSERT para agregar los datos obtenidos del servicio web a la tabla.
    La última línea del archivo SQL tiene un punto y coma ; al final de la última sentencia INSERT para asegurar que el script SQL sea válido y pueda ser ejecutado sin problemas en una base de datos SQL.

Archivo CSV (`respuesta_balance_general_trimestral.csv`):
    Contiene los datos en formato CSV, facilitando la visualización y el análisis de los datos en herramientas como Microsoft Excel o Google Sheets. El archivo CSV tiene columnas que corresponden a los campos de datos extraídos y se estructuran en formato tabular.
