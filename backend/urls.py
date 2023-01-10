from django.urls import path
from backend.views import GamesTogether, Home, CheckEight, Example, FileTest, PreviousSearch

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('compare/', GamesTogether.as_view(), name='compare'),
    path('example/', Example.as_view(), name='example'),
    path('testing/', FileTest.as_view(), name='testing'),
    path('previous-search', PreviousSearch.as_view(), name='previous-search')
]
