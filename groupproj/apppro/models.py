from django.db import models

# Model for Person
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Model for Habit
class Habit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='habits')
    habit_name = models.CharField(max_length=100)
    frequency = models.CharField(
        max_length=50,
        choices=[
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Monthly', 'Monthly'),
            ('Twice a Week', 'Twice a Week')
        ]
    )
    duration_minutes = models.PositiveIntegerField()
    goal = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.habit_name} ({self.person.name})"
