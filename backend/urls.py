from django.urls import path
from backend.views import GamesTogether, Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('compare/', GamesTogether.as_view(), name='compare')
]
