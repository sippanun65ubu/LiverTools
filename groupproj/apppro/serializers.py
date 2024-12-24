from rest_framework import serializers
from .models import Person, Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = '__all__'
