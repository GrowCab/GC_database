from flask.views import MethodView
from flask_smorest import Blueprint

from models.models import ExpectedMeasureSchema, ExpectedMeasure

schedule_blp = Blueprint('chamber_schedule', 'chamber_schedule',
                         url_prefix='/api',
                         description='Chamber Schedule')


@schedule_blp.route('/chamber_schedule/<int:configuration_id>')
class ChamberSchedule(MethodView):
    @schedule_blp.doc(opertationId='getChamberSchedule')
    @schedule_blp.response(200, ExpectedMeasureSchema(many=True))
    def get(self, configuration_id: int):
        return ExpectedMeasure.query.filter(ExpectedMeasure.configuration_id == configuration_id).order_by(
            ExpectedMeasure.start_hour, ExpectedMeasure.start_minute,
            ExpectedMeasure.end_hour, ExpectedMeasure.end_minute).all()
