from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class ImagenBase(Base):
    __tablename__ = 'ImagenBase'
    Id = Column(Integer, primary_key=True, index=True)
    Ubicacion = Column(String)

    # Relación con la tabla ComparacionResultado
    comparaciones = relationship('ComparacionResultado', back_populates='imagen_base')

class ImagenRecibida(Base):
    __tablename__ = 'ImagenRecibida'
    Id = Column(Integer, primary_key=True, index=True)
    Ubicacion = Column(String)

    # Relación con la tabla ComparacionResultado
    comparaciones = relationship('ComparacionResultado', back_populates='imagen_recibida')

class ComparacionResultado(Base):
    __tablename__ = 'ComparacionResultado'
    Id = Column(Integer, primary_key=True, index=True)
    IdImagenBase = Column(Integer, ForeignKey('ImagenBase.Id'))
    IdImagenRecibida = Column(Integer, ForeignKey('ImagenRecibida.Id'))
    Resultado = Column(String)

    # Relaciones con las tablas ImagenBase e ImagenRecibida
    imagen_base = relationship('ImagenBase', back_populates='comparaciones')
    imagen_recibida = relationship('ImagenRecibida', back_populates='comparaciones')
