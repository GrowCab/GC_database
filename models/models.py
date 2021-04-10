from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from config.config import db


class Chamber(db.Model):
    __tablename__ = "chamber"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    configuration = relationship("Configuration")
    chamber_sensor = relationship("ChamberSensor")
    actuator = relationship("Actuator")


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sensor_unit = relationship("SensorUnit")


class ChamberSensor(db.Model):
    __tablename__ = "chamber_sensor"
    id = Column(Integer, primary_key=True)
    chamber_id = Column(Integer, ForeignKey('chamber.id'))
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    chamber = relationship("Chamber", back_populates='chamber_sensor')
    sensor = relationship("Sensor")


class SensorUnit(db.Model):
    __tablename__ = "sensor_unit"
    id = Column(Integer, primary_key=True)
    min = Column(Float)
    max = Column(Float)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship('Sensor', back_populates='sensor_unit', foreign_keys=[sensor_id])
    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit')


class Measure(db.Model):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    current_value = Column(Float, nullable=False)
    sensor_unit_id = Column(Integer, ForeignKey('sensor_unit.id'))
    sensor_unit = relationship('SensorUnit')


class Unit(db.Model):
    __tablename__ = "unit"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)


class Configuration(db.Model):
    __tablename__ = "configuration"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    chamber_id = Column(Integer, ForeignKey('chamber.id'))
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expected_measure = relationship("ExpectedMeasure", back_populates='configuration')
    chamber = relationship("Chamber", back_populates='configuration')


class ExpectedMeasure(db.Model):
    """
    The first value of the intervals (0000) is implicit making the last interval
    (2359) always required. Any configuration of intervals in-between is be valid.
    """
    __tablename__ = "expected_measure"
    id = Column(Integer, primary_key=True)
    expected_value = Column(Float, nullable=False)
    end_hour = Column(Integer, nullable=False)
    end_minute = Column(Integer, nullable=False)
    configuration_id = Column(Integer, ForeignKey('configuration.id'))
    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit')
    configuration = relationship('Configuration', back_populates='expected_measure')


class Actuator(db.Model):
    __tablename__ = "actuator"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    chamber_id = Column(Integer, ForeignKey('chamber.id'))
    actuator_effect = relationship("ActuatorEffect")


class ActuatorEffect(db.Model):
    __tablename__ = "actuator_effect"
    id = Column(Integer, primary_key=True)
    change = Column(Integer, nullable=False)
    actuator_id = Column(Integer, ForeignKey('actuator.id'))
    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit')


class ChamberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Chamber
        load_instance = True


class SensorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor
        include_fk = True
        load_instance = True
    chamber = Nested(ChamberSchema)


class UnitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Unit
        include_fk = True
        load_instance = True


class SensorUnitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SensorUnit
        load_instance = True
    unit = Nested(UnitSchema)


class ExpectedMeasureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ExpectedMeasure
        include_fk = True
        load_instance = True
    unit = Nested(UnitSchema)


class ConfigurationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Configuration
        include_fk = True
        load_instance = True
