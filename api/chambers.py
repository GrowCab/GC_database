from time import sleep

from flask.views import MethodView
from flask_smorest import Blueprint

from models.models import Chamber, ChamberSensor, ChamberSchema, Unit, SensorUnit, Sensor, UnitSchema, Configuration

chamber_blp = Blueprint('chambers', 'chambers',
                        url_prefix='/api',
                        description='Operations on Chambers')


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
        """Get the
        :param chamber_id: ID of the chamber
        :return: Returns a Chamber object
        """
        return Chamber.query.filter(Chamber.id == chamber_id).one_or_none()


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
        sleep(1)
        return Unit.query.join(SensorUnit.sensor).join(Sensor.chamber_sensor).\
            filter(ChamberSensor.chamber_id == chamber_id).all()
