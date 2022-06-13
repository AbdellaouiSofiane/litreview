from django.urls import path

from .views import (
    TicketCreateView, TicketUpdateView, TicketDeleteView,
    ReviewUpdateView, TicketAndReviewCreateView, ReviewDeleteView,
    posts, feed
)


app_name = 'post'

urlpatterns = [
    path('', feed, name='feed'),
    path('posts/', posts, name='posts'),
    path('add_ticket/', TicketCreateView.as_view(), name='add_ticket'),
    path('update_ticket/<int:pk>', TicketUpdateView.as_view(), name='update_ticket'),
    path('delete_ticket/<int:pk>', TicketDeleteView.as_view(), name='delete_ticket'),
    path('add_ticket_and_review/', TicketAndReviewCreateView.as_view(), name='add_ticket_and_review'),
    path('update_review/<int:pk>', ReviewUpdateView.as_view(), name='update_review'),
    path('delete_review/<int:pk>', ReviewDeleteView.as_view(), name='delete_review'),
]
