from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import (
    TicketCreateView, TicketUpdateView, TicketDeleteView,
    TicketAndReviewCreateView, posts
)


app_name = 'post'

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name="post/feed.html")), name='feed'),
    path('posts/', posts, name='posts'),
    path('add_ticket/', TicketCreateView.as_view(), name='add_ticket'),
    path('update_ticket/<int:pk>', TicketUpdateView.as_view(), name='update_ticket'),
    path('delete_ticket/<int:pk>', TicketDeleteView.as_view(), name='delete_ticket'),
    path('add_ticket_and_review/', TicketAndReviewCreateView.as_view(), name='add_ticket_and_review'),
]
