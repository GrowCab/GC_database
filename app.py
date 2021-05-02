from api.chamber_schedule import schedule_blp
from api.chambers import chamber_blp
from api.configurations import configuration_blp
from api.measure_group import measure_group_blp
from api.sensors import sensors_blp, sensor_blp
from config import config

app = config.app  # Flask app instance initiated
api = config.api
api.register_blueprint(sensors_blp)
api.register_blueprint(configuration_blp)
api.register_blueprint(sensor_blp)
api.register_blueprint(schedule_blp)
api.register_blueprint(chamber_blp)
api.register_blueprint(measure_group_blp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
