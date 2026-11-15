import os
from pathlib import Path
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv('GCP_DATASET_ID')
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def excecute_tranformation():
    client = bigquery.Client(project=PROJECT_ID)

    sql_file_path = Path('src/etl/sql/create_features.sql')
    if not sql_file_path.exists():
        raise FileNotFoundError(f'No se encontró el script SQL en {sql_file_path}')

    print(f'Leyendo consulta desde {sql_file_path}')

    with open(sql_file_path, 'r',encoding='utf-8') as f:
        sql_query = f.read()

    print(f'Ejecutando pipeline ETL en BigQuery (creando tabla features)')
    query_job = client.query(sql_query)
    query_job.result()

    table_id = f'{PROJECT_ID}.{DATASET_ID}.telco_churn_features'
    table = client.get_table(table_id)

    print("Tabla de features creada con éxito.")
    print(f"   - Nombre: {table.table_id}")
    print(f"   - Total Filas: {table.num_rows:,}")
    print(f"   - Total Columnas: {len(table.schema)}")
    print("Variables creadas destacadas:")
    for field in table.schema[-6:]:
        print(f"     * {field.name} ({field.field_type})")


if __name__ == "__main__":
    excecute_tranformation()