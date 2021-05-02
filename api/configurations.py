"""
This is the configurations module and supports all the REST actions for the configuration data
"""
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from api.chambers import get_chamber_units
from config.config import db
from models.models import Configuration, ConfigurationSchema, EditableConfigurationSchema

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
    @configuration_blp.arguments(EditableConfigurationSchema)
    @configuration_blp.response(200, ConfigurationSchema)
    def put(self, configuration):
        """Stores a new configuration

        ----------------------------

        This is an example of the data required to insert a new configuration
        {
          "description": "Initial configuration",
          "expected_measure": [
            {
              "expected_value": 10,
              "end_hour": 23,
              "end_minute": 59,
              "unit_id": 1
            },
            {
              "expected_value": 10,
              "end_hour": 23,
              "end_minute": 59,
              "unit_id": 2
            },
            {
              "expected_value": 10,
              "end_hour": 23,
              "end_minute": 59,
              "unit_id": 3
            }
          ],
          "chamber_id": 1
        }
        :param configuration:
        :return:
        """

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
            db.session.commit()

            return configuration, 201
        else:
            abort(400,
                  f"Configuration {configuration} is invalid")
