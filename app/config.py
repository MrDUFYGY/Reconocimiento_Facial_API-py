from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configura la cadena de conexión a SQL Server
SQLALCHEMY_DATABASE_URL = r"mssql+pyodbc://sa:Inquieto.17@FJUAREZ\SQLEXPRESS/reconocimiento facial?driver=SQL+Server+Native+Client+11.0"

# Crea el motor para la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crea la sesión para la interacción con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea la base para definir los modelos
Base = declarative_base()
