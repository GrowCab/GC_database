from datetime import datetime

from sqlalchemy.orm import relationship

from config import db
from config import ma


class Chamber(db.Model):
    __tablename__ = "chamber"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    sensor = relationship("Sensor")


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sensor_unit_id = db.Column(db.Integer, db.ForeignKey('sensor_unit.id'))
    sensor_unit = relationship("SensorUnit")


class SensorUnit(db.Model):
    __tablename__ = "sensor_unit"
    id = db.Column(db.Integer, primary_key=True)
    min = db.Column(db.Float)
    max = db.Column(db.Float)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = relationship('Unit', back_populates='sensor_unit')


class Unit(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    sensor_unit = relationship('SensorUnit', uselist=False, back_populates='unit')


class SensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor
        load_instance = True
