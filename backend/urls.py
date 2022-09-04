from django.urls import path
from backend.views import GamesTogether, Home, CheckEight, Example

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('compare/', GamesTogether.as_view(), name='compare'),
    path('check8/', CheckEight.as_view(), name='check8'),
    path('example/', Example.as_view(), name='example')
]
