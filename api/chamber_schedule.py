from time import sleep

from flask.views import MethodView
from flask_smorest import Blueprint

from models.models import ConfigurationSchema, Configuration, ExpectedMeasure, ExpectedMeasureSchema

schedule_blp = Blueprint('chamber_schedule', 'chamber_schedule',
                         url_prefix='/api',
                         description='Chamber Schedule')


@schedule_blp.route('/chamber_schedule/<int:chamber_id>')
class ChamberSchedule(MethodView):
    @schedule_blp.doc(operationId='getChamberSchedule')
    @schedule_blp.response(200, ConfigurationSchema)
    def get(self, chamber_id: int):
        configuration = Configuration.query.filter(Configuration.chamber_id == chamber_id).\
            order_by(Configuration.timestamp.desc()).first()
        return configuration


@schedule_blp.route('/chamber_schedule_unit/<int:chamber_id>/<int:unit_id>')
class ChamberScheduleUnit(MethodView):
    @schedule_blp.doc(operationId='getChamberScheduleUnit')
    @schedule_blp.response(200, ExpectedMeasureSchema(many=True))
    def get(self, chamber_id: int, unit_id: int):
        return ExpectedMeasure.query.join(Configuration).filter(Configuration.chamber_id == chamber_id).\
            filter(ExpectedMeasure.unit_id == unit_id).all()
