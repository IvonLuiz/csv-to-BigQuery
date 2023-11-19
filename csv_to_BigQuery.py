from pathlib import Path
import time
import os
from google.cloud import bigquery

# Set credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'northwind-analytics-405521-584059f4e180.json'

def table_reference(project_id, dataset_id, table_id):
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    table_ref = dataset_ref.table(table_id)
    return table_ref


def delete_dataset_tables(project_id, dataset_id):
    tables = client.list_tables(f'{project_id}.{dataset_id}')
    for table in tables:
        client.delete_table(table)
    print('Tables deleted.')

def upload_csv(client, table_ref, csv_file):
    # client.delete_table(table_ref, not_found_ok=True)

    load_job_configuration = bigquery.LoadJobConfig()
    
    # Manually define the schema if necessary
    # load_job_configuration.schema = [
    #     bigquery.SchemaField('<field name1>', '<data type>', mode='<mode type>'),
    #     bigquery.SchemaField('<field name2>', '<data type>', mode='<mode type>'),
    #     bigquery.SchemaField('<field name3>', '<data type>', mode='<mode type>')
    # ]

    load_job_configuration.autodetect = True
    load_job_configuration.source_format = bigquery.SourceFormat.CSV
    load_job_configuration.skip_leading_rows = 1
    load_job_configuration.allow_quoted_newlines = True

    # Api request to
    with open(csv_file, 'rb') as source_file:
        upload_job = client.load_table_from_file(
            source_file,
            destination=table_ref,          
            location='US',
            job_config=load_job_configuration
        )

    while upload_job.state != 'DONE':
        time.sleep(2)
        upload_job.reload()
        print(upload_job.state)

    print(upload_job.result())

#------------------------------Main------------------------------

# Insert project variables
project_id = 'northwind-analytics-405521'
dataset_id = 'public'

client = bigquery.Client()
# Folder path
data_file_folder = Path('D:\\Code\\Indicium\\northwind\\seeds\\erp_northwind')

for file in os.listdir(data_file_folder):
    if file.endswith('.csv'):
        print('Processing file: {0}'.format(file))
        # Change accordingly to the file names 
        table_name = file.replace('.csv', '')
        csv_file = data_file_folder.joinpath(file)
        table_ref = table_reference(project_id, dataset_id, table_name)
        upload_csv(client, table_ref, csv_file)
        print()

# delete_dataset_tables(project_id, dataset_id)     