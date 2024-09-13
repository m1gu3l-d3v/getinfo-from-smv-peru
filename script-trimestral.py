from zeep import Client
import json
import csv

# Crear cliente para el servicio SOAP
client = Client('https://mvnet.smv.gob.pe/ws_od_eeff/WebServiceInfoFinanciera.asmx?wsdl')

# Definir el rango de años
start_year = 2022
end_year = 2023

# Definir nombres de archivos
json_file = 'respuesta_balance_general_trimestral.json'
sql_file = 'respuesta_balance_general_trimestral.sql'
csv_file = 'respuesta_balance_general_trimestral.csv'

# SQL Statement Template
sql_template = (
    "('{RPJ}', '{TipoEmpresa}', '{TipoSector}', '{NombreEmpresa}', '{RUC}', '{CIIU}', '{Ejercicio}', "
    "'{TipoInformacion}', '{Trimestre}', '{Moneda}', '{MetodoFlujoEfectivo}', '{Cuenta}', '{DescripcionCuenta}', "
    "{Monto1}, {Monto2})"
)

# SQL to create table if it does not exist
create_table_sql = (
    "CREATE TABLE IF NOT EXISTS balance_general (\n"
    "    ID INT AUTO_INCREMENT,\n"
    "    RPJ VARCHAR(50),\n"
    "    TipoEmpresa VARCHAR(50),\n"
    "    TipoSector VARCHAR(50),\n"
    "    NombreEmpresa VARCHAR(255),\n"
    "    RUC VARCHAR(20),\n"
    "    CIIU VARCHAR(10),\n"
    "    Ejercicio YEAR,\n"
    "    TipoInformacion VARCHAR(50),\n"
    "    Trimestre VARCHAR(15),\n"
    "    Moneda VARCHAR(20),\n"
    "    MetodoFlujoEfectivo VARCHAR(50),\n"
    "    Cuenta VARCHAR(20),\n"
    "    DescripcionCuenta VARCHAR(255),\n"
    "    Monto1 DECIMAL(15, 2),\n"
    "    Monto2 DECIMAL(15, 2),\n"
    "    PRIMARY KEY (ID)\n"
    ");\n"
    "\n"
    "INSERT INTO balance_general (RPJ, TipoEmpresa, TipoSector, NombreEmpresa, RUC, CIIU, Ejercicio, \n"
    "TipoInformacion, Trimestre, Moneda, MetodoFlujoEfectivo, Cuenta, DescripcionCuenta, Monto1, Monto2) \n"
    "VALUES\n"
)

# Abrir archivos para escritura
with open(json_file, 'w') as json_f, open(sql_file, 'w') as sql_f, open(csv_file, 'w', newline='', encoding='utf-8') as csv_f:
    # Inicializar escritor CSV
    csv_writer = csv.DictWriter(csv_f, fieldnames=[
        'RPJ', 'TipoEmpresa', 'TipoSector', 'NombreEmpresa', 'RUC', 'CIIU', 'Ejercicio',
        'TipoInformacion', 'Trimestre', 'Moneda', 'MetodoFlujoEfectivo', 'Cuenta',
        'DescripcionCuenta', 'Monto1', 'Monto2'
    ])
    csv_writer.writeheader()
    
    # Escribir la sentencia SQL para crear la tabla
    sql_f.write(create_table_sql + '\n')
    
    # Lista para almacenar las filas de datos SQL
    values = []

    # Iterar sobre el rango de años y trimestres
    for year in range(start_year, end_year + 1):
        for trimestre in range(1, 5):
            try:
                # Realizar la consulta para el año y trimestre actual
                response = client.service.obtener_BalanceGeneral(
                    Ejercicio=str(year),
                    Periodo=str(trimestre),
                    Tipo='I'
                )
                
                # Verifica si la respuesta es una cadena de texto que parece JSON
                response_json = json.loads(response)
                
                # Procesar cada ítem en la respuesta
                for item in response_json:
                    # Escribir en el archivo CSV
                    csv_writer.writerow(item)
                    
                    # Crear la sentencia SQL
                    sql = sql_template.format(
                        RPJ=item.get('RPJ', ''),
                        TipoEmpresa=item.get('TipoEmpresa', ''),
                        TipoSector=item.get('TipoSector', ''),
                        NombreEmpresa=item.get('NombreEmpresa', ''),
                        RUC=item.get('RUC', ''),
                        CIIU=item.get('CIIU', ''),
                        Ejercicio=item.get('Ejercicio', ''),
                        TipoInformacion=item.get('TipoInformacion', ''),
                        Trimestre=item.get('Trimestre', ''),
                        Moneda=item.get('Moneda', ''),
                        MetodoFlujoEfectivo=item.get('MetodoFlujoEfectivo', ''),
                        Cuenta=item.get('Cuenta', ''),
                        DescripcionCuenta=item.get('DescripcionCuenta', ''),
                        Monto1=item.get('Monto1', '0'),
                        Monto2=item.get('Monto2', '0')
                    )
                    values.append(sql)
                
                print(f'Datos para el año {year}, trimestre {trimestre} han sido procesados.')

            except json.JSONDecodeError:
                print(f"La respuesta para el año {year}, trimestre {trimestre} no es un JSON válido o no está bien formada.")
            except Exception as e:
                print(f"Se produjo un error para el año {year}, trimestre {trimestre}: {e}")

    # Escribir todas las filas en el archivo SQL
    if values:
        with open(sql_file, 'a') as sql_f:
            sql_f.write("INSERT INTO balance_general (RPJ, TipoEmpresa, TipoSector, NombreEmpresa, RUC, CIIU, Ejercicio, \n"
                        "TipoInformacion, Trimestre, Moneda, MetodoFlujoEfectivo, Cuenta, DescripcionCuenta, Monto1, Monto2) \n"
                        "VALUES\n")
            sql_f.write(",\n".join(values))
            
    # Reemplazar la última coma por punto y coma
    with open(sql_file, 'r+') as sql_f:
        content = sql_f.read()
        # Reemplazar la última coma por punto y coma
        if content.endswith(",\n"):
            content = content[:-2] + ';\n'
        elif content.endswith(","):
            content = content[:-1] + ';\n'
        # Volver al inicio del archivo y sobrescribir el contenido modificado
        sql_f.seek(0)
        sql_f.write(content)
        sql_f.truncate()

# Asegúrate de agregar un punto y coma al final del archivo SQL
with open(sql_file, 'a') as sql_f:
    sql_f.write(';\n')

print(f'La respuesta JSON se ha guardado en {json_file}')
print(f'Las consultas SQL se han guardado en {sql_file}')
print(f'La respuesta CSV se ha guardado en {csv_file}')
