from rest_framework import generics
from .models import Person
from .serializers import PersonSerializer
from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage.html')

class PersonListView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
