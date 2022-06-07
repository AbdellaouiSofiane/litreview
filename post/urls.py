from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import TicketCreateView, TicketUpdateView, TicketAndReviewCreateView

app_name = 'post'

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name="post/posts.html")), name='posts'),
    path('add_ticket/', TicketCreateView.as_view(), name='add_ticket'),
    path('update_ticket/<int:pk>', TicketUpdateView.as_view(), name='update_ticket'),
    path('add_ticket_and_review/', TicketAndReviewCreateView.as_view(), name='add_ticket_and_review'),
]
