from flask.views import MethodView
from flask_smorest import Blueprint

from config.config import db
from models.models import MeasureGroup, ChamberSensor, SensorMeasure, MeasureGroupSchema, EditableMeasureGroup

measure_group_blp = Blueprint('measure_group', 'measure_group',
                              url_prefix='/api',
                              description='Measure Group')


@measure_group_blp.route('/measure_group/<int:chamber_id>')
class ChamberMeasureGroup(MethodView):
    @measure_group_blp.doc(operationId='getLatestMeasureGroup')
    @measure_group_blp.response(200, MeasureGroupSchema)
    def get(self, chamber_id: int):
        latest_measure_group = MeasureGroup.query.join(SensorMeasure).join(ChamberSensor)\
            .filter(ChamberSensor.chamber_id == chamber_id).\
            order_by(MeasureGroup.timestamp.desc()).first()
        return latest_measure_group


@measure_group_blp.route('/measure_group')
class MeasureGroup(MethodView):
    @measure_group_blp.doc(operationId='putLatestMeasureGroup')
    @measure_group_blp.arguments(EditableMeasureGroup)
    @measure_group_blp.response(200, MeasureGroupSchema)
    def put(self, measure_group: EditableMeasureGroup):
        db.session.add(measure_group)
        db.session.commit()
        return measure_group
