import pyodbc

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=192.168.1.68;"
    "Database=empresa;"
    "Encrypt=no;"
    "UID=sa;"
    "PWD=123;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Conexión exitosa")
except Exception as e:
    print(f"Error al conectar: {e}")