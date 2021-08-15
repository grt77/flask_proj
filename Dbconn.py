import sqlite3

def open_conn():
    conn=sqlite3.connect('C:\\Users\\FL_LPT-255\\Desktop\\db\\emp.db')
    print("connecting to data base")
    return conn


def close_conn(db):
    db.close()
    print("closed the connection")



if __name__=="__main__":
    print(open_conn())