from rest_framework import serializers

from courses.models import Instruction


class InstructionSerializer(serializers.ModelSerializer):

    completed = serializers.SerializerMethodField()

    class Meta:
        model = Instruction
        exclude = ('exercise',)

    def __init__(self, instance, *args, **kwargs):
        self.user_exercise = kwargs.pop('user_exercise', None)
        super(InstructionSerializer, self).__init__(instance, *args, **kwargs)

    def get_completed(self, instance):
        print(instance)
        if self.user_exercise:
            return self.user_exercise.instructions_completed.all().filter(id=instance.id).exists()
        return False

