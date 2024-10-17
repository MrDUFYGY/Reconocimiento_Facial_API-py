from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cadena de conexión a SQL Server usando pyodbc
SQLALCHEMY_DATABASE_URL = r"mssql+pyodbc://sa:Inquieto.17@FJUAREZ\SQLEXPRESS/ReconocimientoFacial?driver=SQL+Server+Native+Client+11.0"

# Crear el motor de conexión a la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de la que heredarán los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
