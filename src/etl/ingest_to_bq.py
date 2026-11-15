import os
import shutil
import glob
from pathlib import Path
import pandas as pd
import kagglehub
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from src.Routes.Routes import ROUTES

load_dotenv()

PROJECT_ID = os.getenv('GCP_PROJECT_ID')
DATASET_ID = os.getenv('GCP_DATASET_ID')
TABLE_NAME = os.getenv('GCP_TABLE_NAME')
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

routes = ROUTES


if CREDENTIALS_PATH:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_PATH

def download_dataset() -> Path:
    
    print(" Descargando dataset desde Kaggle...")
    
    candidato_dataseet = "yeanzc/telco-customer-churn-ibm-dataset"
    try:
        download_path = Path(kagglehub.dataset_download(candidato_dataseet, force_download=True))
    except Exception:
        print("⚠️ Falló la descarga inicial, intentando con dataset canónico blastchar...")
        candidato_dataseet = "blastchar/telco-customer-churn"
        download_path = Path(kagglehub.dataset_download(candidato_dataseet, force_download=True))

    print(f"Ruta de descarga: {download_path}")

    all_files = list(download_path.rglob("*"))

    data_files = [f for f in all_files if f.is_file() and f.suffix.lower() in [".csv", ".xlsx", ".xls"]]

    if not data_files:
        archivos_encontrados = [f.name for f in all_files if f.is_file()]
        raise FileNotFoundError(
            f"No se encontraron archivos .csv ni .xlsx en {download_path}. "
            f"Archivos presentes: {archivos_encontrados}"
        )

    selected_file = data_files[0]
    print(f"Archivo de datos seleccionado: {selected_file.name} (tipo: {selected_file.suffix})")
    return selected_file

def move_files(origin_path: Path, destination_path: Path):
    file_path = origin_path
    file_name = file_path.name
    
    if not file_path:
        raise FileNotFoundError(f'No seha encontrado el archivo para mover en {origin_path}')
    
    
    shutil.move(file_path, destination_path / file_name)

    print(f'{file_name} movido a {destination_path}')

    return destination_path / file_name 

def create_folders(Routes: dict):
    for r in Routes.values():
        Path(r).mkdir(exist_ok=True, parents=True)

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    reemplazos = str.maketrans({' ':'_', '-':'_', '/':'_', '(':'', ')':''})
    
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.translate(reemplazos)
    )
    return df

def ensure_dataset_exists(client: bigquery.Client, dataset_id: str):

    dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f'Dataset "{dataset_id}" confirmado en Bigquery.')
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location('US')
        client.create_dataset(dataset, timeout=30)
        print(f'Dataset: "{dataset_id}" creado en "{dataset.location}".')

def load_raw_to_bigquery(df:pd.DataFrame, project_id: str, dataset_id: str, table_name: str):
    client = bigquery.Client(project=project_id)
    ensure_dataset_exists(client, dataset_id)

    table_id = f'{project_id}.{dataset_id}.{table_name}'

    job_config = bigquery.LoadJobConfig(
        autodetect = True,
        write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    print(f'Cargando {len(df):,} filas en {table_id}...')

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    table = client.get_table(table_id)
    print(f'Carga exitosa en BigQuery.')
    print(f'    - Tabla: {table.table_id}.')
    print(f'    - Total registros: {table.num_rows:,}.')
    print(f'    - Total Columnas: {len(table.schema)}.')


def main():

    create_folders(routes)
    
    download_path = download_dataset()
    
    file_path = move_files(download_path, ROUTES['input'])
    
    print(f"Leyendo archivo: {file_path.name}...")
    if file_path.suffix.lower() == ".csv":
        df_raw = pd.read_csv(file_path, dtype=str)
    else:
        df_raw = pd.read_excel(file_path, dtype=str)
        
    print(f"Dimensiones crudas: {df_raw.shape[0]} filas, {df_raw.shape[1]} columnas.")
    
    df_clean = clean_column_names(df_raw)
    load_raw_to_bigquery(df_clean, PROJECT_ID, DATASET_ID, TABLE_NAME)

if __name__ == '__main__':
    main()