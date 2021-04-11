from time import sleep

from flask.views import MethodView
from flask_smorest import Blueprint

from models.models import ConfigurationSchema, Configuration

schedule_blp = Blueprint('chamber_schedule', 'chamber_schedule',
                         url_prefix='/api',
                         description='Chamber Schedule')


@schedule_blp.route('/chamber_schedule/<int:chamber_id>')
class ChamberSchedule(MethodView):
    @schedule_blp.doc(operationId='getChamberSchedule')
    @schedule_blp.response(200, ConfigurationSchema)
    def get(self, chamber_id: int):
        sleep(1)
        configuration = Configuration.query.filter(Configuration.chamber_id == chamber_id).\
            order_by(Configuration.timestamp).one_or_none()
        return configuration
