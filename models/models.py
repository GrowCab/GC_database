from datetime import datetime

from sqlalchemy.orm import relationship

from config import db
from config import ma


class Chamber(db.Model):
    __tablename__ = "chamber"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    configuration = relationship("Configuration")
    sensor = relationship("Sensor")


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chamber.id'))
    chamber = relationship("Chamber")
    sensor_unit = relationship("SensorUnit")


class SensorUnit(db.Model):
    __tablename__ = "sensor_unit"
    id = db.Column(db.Integer, primary_key=True)
    min = db.Column(db.Float)
    max = db.Column(db.Float)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    sensor = relationship('Sensor', foreign_keys=[sensor_id])
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = relationship('Unit')


class Unit(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)


class Configuration(db.Model):
    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chamber.id'))
    expected_measure = relationship("ExpectedMeasure")


class ExpectedMeasure(db.Model):
    __tablename__ = "expected_measure"
    id = db.Column(db.Integer, primary_key=True)
    expected_value = db.Column(db.Float, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    configuration_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))


class ChamberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chamber
        load_instance = True


class SensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor
        include_fk = True
        load_instance = True


class SensorUnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SensorUnit
        load_instance = True


class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit
        include_fk = True
        load_instance = True


class ConfigurationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Configuration
        include_fk = True
        load_instance = True


class ExpectedMeasureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExpectedMeasure
        include_fk = True
        load_instance = True
