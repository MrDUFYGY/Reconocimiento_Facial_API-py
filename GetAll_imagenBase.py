import pyodbc

# Datos de conexión
server = 'FJUAREZ\\SQLEXPRESS'  # El nombre de tu servidor SQL Server
database = 'ReconocimientoFacial'  # El nombre de tu base de datos
username = 'sa'  # Tu usuario
password = 'Inquieto.17'  # Tu contraseña

# Conectar a SQL Server
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Crear un cursor
cursor = conn.cursor()

# Ejecutar el stored procedure para traer información de ImagenBase
cursor.execute("EXEC GetAllImagenBase")

# Obtener los resultados
rows = cursor.fetchall()

# Mostrar los resultados
for row in rows:
    print(row)

# Cerrar la conexión
cursor.close()
conn.close()
