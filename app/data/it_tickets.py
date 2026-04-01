import pandas as pd
from pathlib import Path


def migrate_it_tickets(conn):
    data = pd.read_csv(Path('DATA') / 'it_tickets.csv', index_col='ticket_id')
    data.to_sql('it_tickets', conn, if_exists='append')

def insert_it_ticket(conn):

    priority = input('What is the priority? ')
    description = input('What is the description of the ticket? ')
    status = input('What is the status of the ticket? ')
    assigned_to = input('Who is the ticket assigned to? ')
    resolution_time_hours = input('How long will it take to resolve? ')

    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO it_tickets (priority, description, status, assigned_to, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?)
        ''', (priority, description, status, assigned_to, resolution_time_hours)
    )
    conn.commit()

def update_ticket_status(conn, id, status):
    '''Update the status of an ticket.'''
    cur = conn.cursor() 
    cur.execute(
        'UPDATE it_tickets SET status = ? WHERE incident_id = ?', (status, id)
    )
    conn.commit()
    cur.rowcount

def delete_ticket(conn, id):
    '''Delete a ticket from the database.'''
    cur = conn.cursor() 
    cur.execute(
        'DELETE FROM it_tickets WHERE incident_id = ?', (id,)
    )
    conn.commit()
    cur.rowcount

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn, index_col='ticket_id')
    
    return data   