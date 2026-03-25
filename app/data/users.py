
def add_user(conn, username, password_hash):
    cur = conn.cursor()
    sql = "INSERT INTO users (username, password_hash) VALUES(?,?)"
    params = (username, password_hash)
    cur.execute(sql,params)
    conn.commit()

def get_all_users(conn):
    cur = conn.cursor()
    sql = 'SELECT * FROM users'
    cur.execute(sql)
    users = cur.fetchall()
    
    return users

def get_user(conn, username):
    cur = conn.cursor()
    sql = 'SELECT * FROM users WHERE username = ?'
    param = (username,)
    cur.execute(sql, param)
    user = cur.fetchone()
    
    return user

def update_user_username(conn, new_name, old_name):
    cur = conn.cursor()
    sql = 'UPDATE users SET username = ? WHERE username = ?'
    params = (new_name, old_name)
    cur.execute(sql, params)
    conn.commit()

def upgrade_user_role(conn, new_role, username):
    cur = conn.cursor()
    sql = 'UPDATE users SET role = ? WHERE username = ?'
    params = (new_role, username)
    cur.execute(sql, params)
    conn.commit()

def delete_user(conn, username):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (username,)
    cur.execute(sql, param)
    conn.commit()