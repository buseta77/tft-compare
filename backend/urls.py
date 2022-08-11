from django.urls import path
from backend.views import GamesTogether

urlpatterns = [
    path('compare/', GamesTogether.as_view(), name='compare')
]
