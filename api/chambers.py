from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import desc

from config.config import db
from models.models import Chamber, ChamberSensor, ChamberSchema, Unit, SensorUnit, Sensor, UnitSchema, \
    SensorUnitSchema, SensorMeasure, MeasureSchema, MeasureGroup, ChamberStatusSchema, MeasureGroupSchema, \
    ChamberPowerStatusSchema

chamber_blp = Blueprint('chambers', 'chambers',
                        url_prefix='/api',
                        description='Operations on Chambers')


def get_chamber_units(chamber_id):
    return Unit.query.join(SensorUnit.sensor).join(Sensor.chamber_sensor). \
        filter(ChamberSensor.chamber_id == chamber_id).all()


def get_chamber_sensor(chamber_id):
    return SensorUnit.query.join(ChamberSensor.sensor).filter(ChamberSensor.chamber_id == chamber_id).all()


@chamber_blp.route('/chambers')
class ChambersList(MethodView):
    @chamber_blp.doc(operationId='getChambers')
    @chamber_blp.response(200, ChamberSchema(many=True))
    def get(self):
        """Get the list of configurations

        -------------------
        :return: Returns a list of configurations objects
        """
        return Chamber.query.all()


@chamber_blp.route('/chamber/<int:chamber_id>')
class ChamberAPI(MethodView):
    @chamber_blp.doc(operationId='getChamber')
    @chamber_blp.response(200, ChamberSchema)
    def get(self, chamber_id):
        """Get the chamber and related objects
        :param chamber_id: ID of the chamber
        :return: Returns a Chamber object
        """
        return Chamber.query.join(ChamberSensor.chamber).filter(Chamber.id == chamber_id).one_or_none()


@chamber_blp.route('/chamber/power/<int:chamber_id>')
class ChamberPowerAPI(MethodView):
    @chamber_blp.doc(operationId='getChamberPowerStatus')
    @chamber_blp.response(200, ChamberPowerStatusSchema)
    def get(self, chamber_id: int):
        ret = Chamber.query.filter(Chamber.id == chamber_id).one_or_none()
        return ret

    @chamber_blp.doc(operationId='setChamberPowerStatus')
    @chamber_blp.arguments(ChamberPowerStatusSchema)
    @chamber_blp.response(200, ChamberSchema)
    def put(self, chamber_power_status: Chamber.ChamberPowerStatus, chamber_id: int):
        chamber = Chamber.query.filter(Chamber.id == chamber_id).one_or_none()
        chamber.status = Chamber.ChamberPowerStatus[chamber_power_status['status']]
        db.session.commit()
        return chamber


@chamber_blp.route('/chamber_sensors/<int:chamber_id>')
class ChamberSensorAPI(MethodView):
    @chamber_blp.doc(operationId='getChamberSensors')
    @chamber_blp.response(200, SensorUnitSchema(many=True))
    def get(self, chamber_id):
        """Get the sensors for a chamber
        :param chamber_id:
        :return:
        """
        return get_chamber_sensor(chamber_id)


@chamber_blp.route('/chamber_units/<int:chamber_id>')
class ChamberUnitsAPI(MethodView):
    @chamber_blp.doc(operationId='getChamberUnits')
    @chamber_blp.response(200, UnitSchema(many=True))
    def get(self, chamber_id):
        """Get the units available for this chamber

        This is useful for understanding which dials to present but also which values to use for filtering/separating
        the ExpectedMeasure(s) of a Configuration for a Chamber
        :param chamber_id: ID of the chamber
        :return: Returns a list of Unit objects
        """
        return get_chamber_units(chamber_id)


@chamber_blp.route('/chamber_status/<int:chamber_id>')
class ChamberMeasureAPI(MethodView):
    @chamber_blp.doc(operationId='getChamberStatus')
    @chamber_blp.response(200, MeasureGroupSchema)
    def get(self, chamber_id):
        measure_group = MeasureGroup.query.join(SensorMeasure).join(ChamberSensor.sensor).\
            filter(ChamberSensor.chamber_id == chamber_id).order_by(desc(MeasureGroup.timestamp)).limit(1).one()
        return measure_group

    @chamber_blp.doc(operationId='putChamberStatus')
    @chamber_blp.arguments(ChamberStatusSchema)
    @chamber_blp.response(200, MeasureSchema(many=True))
    def put(self, chamber_status: ChamberStatusSchema, chamber_id: int):
        chamber = Chamber.query.filter(Chamber.id == chamber_id).one()

        print(f"Chamber {chamber}")
        #print(f"{chamber_status}")
        #print("Ssssss........................................................................................")
        measure_group = MeasureGroup()
        db.session.add(measure_group)
        db.session.commit()
        for sensor_hardware_name, sensor_hardware_unit_values in chamber_status["data"].items():
            #print(f"sensor_hardware_name ----------------------------- {sensor_hardware_name}")
            for csensor in chamber.chamber_sensor:
                #print(f"csensor.sensor.hardware_classname ~~~~~~~~~~~~~~~~~~~~~~ {csensor.sensor.hardware_classname}")
                if csensor.sensor.hardware_classname == sensor_hardware_name:
                    for unit, value in sensor_hardware_unit_values.items():
                        for csensor_unit in csensor.sensor.sensor_unit:
                            if csensor_unit.unit.hardware_label == unit:
                                print(f"{sensor_hardware_name} - {unit} - {value}")
                                measure_group.sensor_measure.extend([
                                    SensorMeasure(sensor_unit=csensor_unit, chamber_sensor=csensor, current_value=value)
                                ])
        db.session.commit()

        measure_group = MeasureGroup.query.join(SensorMeasure).join(ChamberSensor.sensor).\
            filter(ChamberSensor.chamber_id == chamber_id).order_by(desc(MeasureGroup.timestamp)).limit(1).one()
        return measure_group.sensor_measure
