from django.urls import path
from backend.views import GamesTogether, Home, UnitImages

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('compare/', GamesTogether.as_view(), name='compare'),
    path('units/<str:unit>', UnitImages.as_view(), name='units')
]
