def create_users_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT'user')
    '''
    cur.execute(sql)
    conn.commit()

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

def create_cyber_incidents_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS cyber_incidents(
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        severity TEXT NOT NULL,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        description TEXT NOT NULL
        )
    '''
    cur.execute(sql)
    conn.commit()

def create_datasets_metadata_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS datasets_metadata(
        dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rows INTEGER NOT NULL,
        columns INTEGER NOT NULL,
        uploaded_by TEXT NOT NULL,
        upload_date TEXT NOT NULL
        )
    '''
    cur.execute(sql)
    conn.commit()

def create_it_tickets_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS it_tickets(
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        priority TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        assigned_to TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolution_time_hours INTEGER NOT NULL
        )
    '''
    cur.execute(sql)
    conn.commit()