import pandas as pd
from pathlib import Path


def migrate_datasets_metadata(conn):
    data = pd.read_csv(Path('DATA') / 'datasets_metadata.csv', index_col='dataset_id')
    data.to_sql('datasets_metadata', conn, if_exists='append')

def insert_dataset_metadata(conn):

    name = input('What is the name of the dataset? ')
    rows = input('How many rows in the dataset? ')
    columns = input('How many columns in the dataset? ')
    uploaded_by = input('Who is uploading the dataset? ')
    upload_date = input('What is the date? ')
    
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO datasets_metadata (name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, rows, columns, uploaded_by, upload_date)
    )
    conn.commit()

def delete_dataset(conn, id):
    '''Delete a dataset from the database.'''
    cur = conn.cursor() 
    cur.execute(
        'DELETE FROM datasets_metadata WHERE incident_id = ?', (id,)
    )
    conn.commit()
    cur.rowcount

def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    
    return data