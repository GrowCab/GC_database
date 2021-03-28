from ctypes import Union
from datetime import datetime

from sqlalchemy.orm import relationship

from config.config import db
from config.config import ma


class Chamber(db.Model):
    __tablename__ = "chamber"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    configuration = relationship("Configuration")
    sensor = relationship("Sensor")
    actuator = relationship("Actuator")


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chamber.id'))
    chamber = relationship("Chamber", back_populates='sensor')
    sensor_unit = relationship("SensorUnit")


class SensorUnit(db.Model):
    __tablename__ = "sensor_unit"
    id = db.Column(db.Integer, primary_key=True)
    min = db.Column(db.Float)
    max = db.Column(db.Float)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    sensor = relationship('Sensor', back_populates='sensor_unit', foreign_keys=[sensor_id])
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = relationship('Unit')


class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    current_value = db.Column(db.Float, nullable=False)
    sensor_unit_id = db.Column(db.Integer, db.ForeignKey('sensor_unit.id'))
    sensor_unit = relationship('SensorUnit')


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
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = relationship('Unit')


class Actuator(db.Model):
    __tablename__ = "actuator"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chamber.id'))
    actuator_effect = relationship("ActuatorEffect")


class ActuatorEffect(db.Model):
    __tablename__ = "actuator_effect"
    id = db.Column(db.Integer, primary_key=True)
    change = db.Column(db.Integer, nullable=False)
    actuator_id = db.Column(db.Integer, db.ForeignKey('actuator.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    unit = relationship('Unit')


class ChamberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chamber
        load_instance = True


class SensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor
        include_fk = True
        load_instance = True
        exclude = ("chamber_id",)
    chamber = ma.Nested(ChamberSchema)


class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit
        include_fk = True
        load_instance = True


class SensorUnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SensorUnit
        load_instance = True
    unit = ma.Nested(UnitSchema)


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
