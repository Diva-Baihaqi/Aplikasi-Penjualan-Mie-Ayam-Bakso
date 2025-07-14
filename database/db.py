import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'kedai_mie_ayam_bakso'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG) 