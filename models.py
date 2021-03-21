from datetime import datetime
from config import db
from config import ma


class Sensor(db.Model):
    __tablename__ = "sensor"
    sensor_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class SensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor
        load_instance = True
