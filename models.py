from datetime import datetime

from sqlalchemy.orm import relationship

from config import db
from config import ma


class Sensor(db.Model):
    __tablename__ = "sensor"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class UnitType(db.Model):
    __tablename__ = "unit_type"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)


class Unit(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    unit_type_id = relationship('UnitType', uselist=False, back_populates="unit_type")


class SensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor
        load_instance = True
