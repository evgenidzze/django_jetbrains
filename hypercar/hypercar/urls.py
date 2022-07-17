from django.urls import path
from tickets.views import *
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='welcome/', permanent=False)),
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view()),
    path('get_ticket/<service>/', GetTicket.as_view(), name="tickets"),
    path('processing', processing, name="processing"),
    path('processing/', RedirectView.as_view(url='/processing')),
    path('next', NextPage.as_view(), name="next")
]
