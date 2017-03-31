from marshmallow import Schema, fields, validate, validates_schema, \
    ValidationError


class DistanceSchema(Schema):
    distance = fields.Integer(missing=30, validate=validate.Range(min=0))
    points = fields.Integer(missing=100, validate=validate.Range(min=0))


class SpaceTimeSchema(Schema):
    time_shift = fields.Integer(missing=1, validate=validate.Range(min=0))
    time_duration = fields.Integer(missing=30, validate=validate.Range(min=1))
    space_distance = fields.Integer(missing=500,
                                    validate=validate.Range(min=1))
    min_count = fields.Integer(missing=1, validate=validate.Range(min=1))
    points = fields.Integer(missing=50, validate=validate.Range(min=0))


class CurrentActivitySchema(Schema):
    still_points = fields.Float(missing=1, validate=validate.Range(min=0))
    other_points = fields.Float(missing=.5, validate=validate.Range(min=0))


class SpeedSchema(Schema):
    max_speed = fields.Integer(missing=1, validate=validate.Range(min=0))
    speed_points = fields.Integer(missing=50, validate=validate.Range(min=0))
    penalty_speed = fields.Integer(missing=10)
    penalty_points = fields.Integer(missing=50, validate=validate.Range(min=0))

    @validates_schema
    def validate_penalty_speed(self, data):
        """Make sure penalty speeds is higher than max speed."""
        if data['max_speed'] >= data['penalty_speed']:
            raise ValidationError('penalty_speed must be greater than '
                                  'max_speed')


class AnalysisSchema(Schema):
    distance = fields.Nested(DistanceSchema, missing=dict())
    space_time = fields.Nested(SpaceTimeSchema, missing=dict())
    current_activity = fields.Nested(CurrentActivitySchema, missing=dict())
    speed = fields.Nested(SpeedSchema, missing=dict())
