import config
from api.configurations import configuration_blp
from api.sensors import sensors_blp, sensor_blp

app = config.app  # Flask app instance initiated
api = config.api
api.register_blueprint(sensors_blp)
api.register_blueprint(configuration_blp)
api.register_blueprint(sensor_blp)
if __name__ == '__main__':
    app.run(debug=True)
