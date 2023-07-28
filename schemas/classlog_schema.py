from init import ma


class ClasslogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'gymclass_id', 'trainer_id', 'member_id')
        ordered = True
    
    # @validates('maxcap')
    # def validate_maxcap(self, value):
    #     if value == max__capacity:
    #         raise ValidationError(f'Unfortunately, the class {} for {} has reached max capacity.')

classlog_schema = ClasslogSchema()
classlogs_schema = ClasslogSchema(many=True)