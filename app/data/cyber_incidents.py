import pandas as pd
from pathlib import Path



def migrate_cyber_incidents(conn):
    data = pd.read_csv(Path('DATA') / 'cyber_incidents.csv', index_col='incident_id')
    data.to_sql('cyber_incidents', conn, if_exists='append')

def insert_cyber_incident(conn):

    severity = input('What is the severity of the incident? ')
    category = input('What is the category of the incident? ')
    status = input('What is the status of the incident? ')
    description = input('What is the description of the incident? ')
    
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO cyber_incidents (severity, category, status, description)
        VALUES (?, ?, ?, ?)
        ''', (severity, category, status, description)
    )
    conn.commit()
    return cur.lastrowid

def update_incident_status(conn, id, status):
    '''Update the status of an incident.'''
    cur = conn.cursor() 
    cur.execute(
        'UPDATE cyber_incidents SET status = ? WHERE incident_id = ?', (status, id)
    )
    conn.commit()
    cur.rowcount

def delete_incident(conn, id):
    '''Delete an incident from the database.'''
    cur = conn.cursor() 
    cur.execute(
        'DELETE FROM cyber_incidents WHERE incident_id = ?', (id,)
    )
    conn.commit()
    cur.rowcount

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """

    return pd.read_sql_query(
        '''SELECT category, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY category
        ORDER BY count DESC
    ''', conn
    )

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """

    return pd.read_sql_query(
        '''SELECT status, COUNT(*) as count
        FROM cyber_incidents
        WHERE severity = 'High'
        GROUP BY status
        ORDER BY count DESC
    ''', conn
    )

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """

    return pd.read_sql_query(
        '''SELECT category, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY category
        HAVING count > ?
        ORDER BY count DESC
    ''', conn, params=(min_count,)
    )

def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql, conn)

    return data
