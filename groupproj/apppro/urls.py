from django.urls import path
from .views import PersonListView, homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('api/people/', PersonListView.as_view(), name='person-list'),
]