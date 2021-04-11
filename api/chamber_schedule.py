from time import sleep

from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from config.config import db
from .chambers import get_chamber_units
from models.models import ConfigurationSchema, Configuration, ExpectedMeasure, ExpectedMeasureSchema

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

    @schedule_blp.doc(operationId='putChamberSchedule')
    @schedule_blp.arguments(ConfigurationSchema)
    @schedule_blp.response(200, ConfigurationSchema)
    def put(self, configuration: Configuration):
        chamber_units = get_chamber_units(configuration.chamber_id)
        is_valid = True

        # Check if:
        for unit in chamber_units:
            unit_interval = [em for em in configuration.expected_measure if em.unit_id == unit.id]
            #   - There is a range for each unit in the chamber
            if not unit_interval:
                is_valid = False
                break
            #   - Each units' configuration is a valid 24h interval
            for interval in unit_interval:
                #   - Each interval is within 0000 - 2359
                if 0 < interval.end_minute > 59:
                    is_valid = False
                    break
                if 0 < interval.end_hour > 23:
                    is_valid = False
                    break
            # - The last interval ends at 2359
            if unit_interval[-1].end_minute != 59:
                is_valid = False
            if unit_interval[-1].end_hour != 23:
                is_valid = False

            if not is_valid:
                break

        if is_valid:
            db.session.add(configuration)
            return configuration
        else:
            return abort(409,
                         f"The configuration provided {configuration} is not valid",
                         )


@schedule_blp.route('/chamber_schedule_unit/<int:chamber_id>/<int:unit_id>')
class ChamberScheduleUnit(MethodView):
    @schedule_blp.doc(operationId='getChamberScheduleUnit')
    @schedule_blp.response(200, ExpectedMeasureSchema(many=True))
    def get(self, chamber_id: int, unit_id: int):
        return ExpectedMeasure.query.join(Configuration).filter(Configuration.chamber_id == chamber_id).\
            filter(ExpectedMeasure.unit_id == unit_id).all()
