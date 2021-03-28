"""
This is the configurations module and supports all the REST actions for the configuration data
"""
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from config.config import db
from models.models import Configuration, ConfigurationSchema

configuration_blp = Blueprint('configurations', 'configurations',
                              url_prefix='/api',
                              description='Operations on Configurations')


@configuration_blp.route('/configurations')
class ConfigurationsList(MethodView):
    @configuration_blp.doc(operationId='getConfigurations')
    @configuration_blp.response(200, ConfigurationSchema(many=True))
    def get(self):
        """Get the list of configurations

        -------------------
        :return: Returns a list of configurations objects
        """
        return Configuration.query.order_by(Configuration.description).all()

    @configuration_blp.doc(operationId='putConfiguration')
    @configuration_blp.arguments(ConfigurationSchema(partial=True))
    @configuration_blp.response(200, ConfigurationSchema)
    def put(self, configuration):
        """Stores a new configuration

        ----------------------------
        :param configuration:
        :return:
        """
        existing_configuration = Configuration.query.filter(
            Configuration.description == configuration.description,
            Configuration.chamber_id == configuration.chamber_id,
            Configuration.start == configuration.start,
            Configuration.end == configuration.end,
            Configuration.expected_measure == configuration.expected_measure).one_or_none()

        if existing_configuration is None:
            db.session.add(configuration)
            db.session.commit()

            return configuration, 201
        else:
            abort(409,
                  f"Configuration {configuration} exists already")
