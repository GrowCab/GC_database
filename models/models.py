from datetime import datetime

from config.config import ma
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
    chamber_actuator = relationship("ChamberActuator")


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sensor_unit = relationship("SensorUnit")
    chamber_sensor = relationship("ChamberSensor")


class ChamberSensor(db.Model):
    __tablename__ = "chamber_sensor"
    id = Column(Integer, primary_key=True)
    chamber_id = Column(Integer, ForeignKey('chamber.id'))
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    chamber = relationship("Chamber", back_populates='chamber_sensor')
    sensor = relationship("Sensor", viewonly=True)
    sensor_measure = relationship("SensorMeasure", back_populates='chamber_sensor')


class SensorUnit(db.Model):
    __tablename__ = "sensor_unit"
    id = Column(Integer, primary_key=True)
    min = Column(Float)
    max = Column(Float)
    sensor_id = Column(Integer, ForeignKey('sensor.id'), nullable=False)
    sensor = relationship('Sensor', back_populates='sensor_unit', foreign_keys=[sensor_id])
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)
    unit = relationship('Unit')
    sensor_measure = relationship('SensorMeasure', back_populates='sensor_unit')


class SensorMeasure(db.Model):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    current_value = Column(Float, nullable=False)
    measure_group_id = Column(Integer, ForeignKey('measure_group.id'), nullable=False)
    sensor_unit_id = Column(Integer, ForeignKey('sensor_unit.id'), nullable=False)
    chamber_sensor_id = Column(Integer, ForeignKey('chamber_sensor.id'), nullable=False)
    sensor_unit = relationship('SensorUnit', back_populates='sensor_measure')
    chamber_sensor = relationship('ChamberSensor', back_populates='sensor_measure')
    measure_group = relationship('MeasureGroup', back_populates='sensor_measure')


class Unit(db.Model):
    __tablename__ = "unit"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)


class Configuration(db.Model):
    __tablename__ = "configuration"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    chamber_id = Column(Integer, ForeignKey('chamber.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expected_measure = relationship("ExpectedMeasure", back_populates='configuration')
    chamber = relationship("Chamber", back_populates='configuration')


class MeasureGroup(db.Model):
    __tablename__ = "measure_group"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sensor_measure = relationship("SensorMeasure")
    actuator_measure = relationship("ActuatorMeasure")


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
    configuration_id = Column(Integer, ForeignKey('configuration.id'), nullable=False)
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)
    unit = relationship('Unit')
    configuration = relationship('Configuration', back_populates='expected_measure')


class Actuator(db.Model):
    __tablename__ = "actuator"
    id = Column(Integer, primary_key=True)
    description = Column(String(512), nullable=False)
    actuator_effect = relationship("ActuatorEffect")


class ChamberActuator(db.Model):
    __tablename__ = "chamber_actuator"
    id = Column(Integer, primary_key=True)
    chamber_id = Column(Integer, ForeignKey('chamber.id'), nullable=False)
    actuator_id = Column(Integer, ForeignKey('actuator.id'), nullable=False)


class ActuatorEffect(db.Model):
    __tablename__ = "actuator_effect"
    id = Column(Integer, primary_key=True)
    change = Column(Integer, nullable=False)
    actuator_id = Column(Integer, ForeignKey('actuator.id'), nullable=False)
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)
    actuator = relationship('Actuator', back_populates='actuator_effect')
    unit = relationship('Unit')


class ActuatorMeasure(db.Model):
    __tablename__ = "actuator_measure"
    id = Column(Integer, primary_key=True)
    current_value = Column(Integer, nullable=False)
    measure_group_id = Column(Integer, ForeignKey('measure_group.id'), nullable=False)
    chamber_actuator_id = Column(Integer, ForeignKey('chamber_actuator.id'), nullable=False)


class ChamberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chamber
        load_instance = True
    chamber_sensor = Nested('ChamberSensorSchema', many=True)


class ChamberSensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChamberSensor
        include_fk = True
        load_instance = True
    sensor = Nested("SensorSchema")


class SensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor
        include_fk = True
        load_instance = True
    chamber = Nested('ChamberSchema')


class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit
        include_fk = True
        load_instance = True


class SensorUnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SensorUnit
        load_instance = True
    unit = Nested('UnitSchema')


class ExpectedMeasureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExpectedMeasure
        include_fk = True
        load_instance = True
    unit = Nested('UnitSchema')


class ConfigurationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Configuration
        include_fk = True
        load_instance = True
    expected_measure = Nested('ExpectedMeasureSchema', many=True)


class ChamberScheduleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Configuration
        include_fk = True
        load_instance = True
    expected_measure = Nested('ExpectedMeasureSchema', many=True, exclude=('unit',))


class MeasureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SensorMeasure
        include_fk = True
        load_instance = True
    sensor_unit = Nested('SensorUnitSchema')
