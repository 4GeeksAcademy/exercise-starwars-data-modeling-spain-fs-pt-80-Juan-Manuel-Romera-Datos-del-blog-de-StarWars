import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table  # type: ignore
from sqlalchemy.orm import relationship, declarative_base  # type: ignore
from sqlalchemy import create_engine  # type: ignore
from eralchemy2 import render_er  # type: ignore

Base = declarative_base()

# Tabla intermedia para la relación muchos-a-muchos entre Usuario y Favoritos
user_favorite_association = Table(
    'user_favorite',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('favorite_id', Integer, ForeignKey('favorite.id'), primary_key=True)
)

# Tabla Usuario
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    subscription_date = Column(DateTime, nullable=False)

    favorites = relationship('Favorite', secondary=user_favorite_association, back_populates='users')

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None,
            "favorites": [favorite.id for favorite in self.favorites]
        }

# Tabla Personaje
class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    species = Column(String(250))
    birth_year = Column(String(100))
    gender = Column(String(50))
    homeworld = Column(String(250))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }

# Tabla Planeta
class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    climate = Column(String(250))
    terrain = Column(String(250))
    population = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }

# Tabla Favoritos
class Favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    favorite_type = Column(String(50), nullable=False)  # 'character' o 'planet'
    favorite_id = Column(Integer, nullable=False)  # ID del personaje o planeta correspondiente
    users = relationship('User', secondary=user_favorite_association, back_populates='favorites')

    def to_dict(self):
        return {
            "id": self.id,
            "favorite_type": self.favorite_type,
            "favorite_id": self.favorite_id,
            "users": [user.id for user in self.users]
        }

# Generar el diagrama de la base de datos
render_er(Base, 'diagram.png')

