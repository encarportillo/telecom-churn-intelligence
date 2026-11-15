import os
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
project_id = os.getenv('GCP_PROJECT_ID')

if credentials_path:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

try:
    client = bigquery.Client(project=project_id)
    datasets = list(client.list_datasets())
    print(f'Conexión exitosa a GCP ({client.project}).')
    print(f'Datasets encontrados: {[d.dataset_id for d in datasets]}')
except Exception as e:
    print(f'Error de autenticacion: {e}')