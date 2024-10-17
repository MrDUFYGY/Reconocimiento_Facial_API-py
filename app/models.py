from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, VARBINARY
from sqlalchemy.orm import relationship
from app.config import Base
from datetime import datetime


# Modelo para la tabla ImagenBase
class ImagenBase(Base):
    __tablename__ = "ImagenBase"

    IdImagenBase = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(255), nullable=False, default='Nombre no asignado')
    Formato = Column(String(50), nullable=False)
    FechaSubida = Column(DateTime, nullable=False, default=datetime.now)
    DatosImagen = Column(VARBINARY, nullable=True)
    RutaImagen = Column(String(500), nullable=True)
    Descripcion = Column(String(1000), nullable=True)

    # Relación con la tabla ComparacionResultado
    comparaciones = relationship("ComparacionResultado", back_populates="imagen_base")


# Modelo para la tabla ImagenRecibida
class ImagenRecibida(Base):
    __tablename__ = "ImagenRecibida"

    IdImagenRecibida = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(255), nullable=False, default='Nombre no asignado')
    Formato = Column(String(50), nullable=False)
    FechaSubida = Column(DateTime, nullable=False, default=datetime.now)
    DatosImagen = Column(VARBINARY, nullable=True)
    RutaImagen = Column(String(500), nullable=True)
    Ubicacion = Column(String(255), nullable=False, default='Ubicacion no asignada')
    Descripcion = Column(String(1000), nullable=True)

    # Relación con la tabla ComparacionResultado
    comparaciones = relationship("ComparacionResultado", back_populates="imagen_recibida")


# Modelo para la tabla ComparacionResultado
class ComparacionResultado(Base):
    __tablename__ = "ComparacionResultado"

    IdComparacion = Column(Integer, primary_key=True, index=True)
    IdImagenBase = Column(Integer, ForeignKey("ImagenBase.IdImagenBase"), nullable=False)
    IdImagenRecibida = Column(Integer, ForeignKey("ImagenRecibida.IdImagenRecibida"), nullable=False)
    ResultadoComparacion = Column(DECIMAL(5, 2), nullable=False)
    FechaComparacion = Column(DateTime, nullable=False, default=datetime.now)
    Ubicacion = Column(String(255), nullable=False, default='Ubicacion no asignada')

    # Relaciones con las otras tablas
    imagen_base = relationship("ImagenBase", back_populates="comparaciones")
    imagen_recibida = relationship("ImagenRecibida", back_populates="comparaciones")
