# -*- encoding: utf-8 -*-
# begin

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger,String, ForeignKey, Unicode, Binary, LargeBinary, Time, DateTime, Date, Text, Boolean, Float
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.orm import sessionmaker

from app import app, db

class Enfant (db.Model):
    __tablename__ = "enfants"
    id = Column('id', Integer, primary_key = True)
    prenom = Column('prenom', Unicode)
    nom = Column('nom', Unicode)

class Contrat (db.Model):
    __tablename__ = "contrats"
    id = Column('id', Integer, primary_key = True)
    enfant_id = Column('enfant_id', Integer, ForeignKey('enfants.id'))
    anniversaire = Column('anniversaire', Date)
    nb_semaine = Column('nb_semaine', Integer)
    salaire = Column('salaire', Float)
    indemnite = Column('indemnite', Float)
    etat = Column('etat', String)
    enfant = relationship('Enfant', foreign_keys=enfant_id)
    horaires = relationship('Horaire', backref='contrat',
                            lazy='dynamic')

class Horaire (db.Model):
    __tablename__ = "horaires"
    id = Column('id', Integer, primary_key = True)
    # Unknown SQL type: 'tinyint' 
    jour = Column('jour', Integer)
    debut = Column('debut', DateTime)
    fin = Column('fin', DateTime)
    commentaire = Column('commentaire', String)
    contrat_id = Column('contrat_id', Integer, ForeignKey('contrats.id'))

    # contrat = relationship('Contrat', foreign_keys=contrat_id)

# end
