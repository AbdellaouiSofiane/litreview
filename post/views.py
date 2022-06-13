from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import CharField, Value, F, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from .forms import ReviewForm, TicketUpdateForm
from .models import Ticket, Review


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'description', 'picture']
    success_url = reverse_lazy('post:posts')

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        self.object = ticket.save()
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    success_url = reverse_lazy('post:posts')


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('post:posts')


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('post:posts')

    def get_queryset(self):
        return Review.objects.select_related('ticket')


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('post:posts')


class ReviewInline(InlineFormSetFactory):
    model = Review
    form_class = ReviewForm
    factory_kwargs = {'extra': 1, 'can_delete': False}


class TicketAndReviewCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Ticket
    fields = ['title', 'description', 'picture']
    inlines = [ReviewInline,]
    template_name = 'post/ticket_and_review.html'
    success_url = reverse_lazy('post:posts')

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        self.object = ticket.save()
        return super().form_valid(form)

    def forms_valid(self, form, inlines):
        response = self.form_valid(form)
        for formset in inlines:
            for form_inline in formset:
                review = form_inline.save(commit=False)
                review.user = self.request.user
            formset.save()
        return response


@login_required
def posts(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user).annotate(
        content_type=Value('TICKET', CharField())
    )
    reviews = Review.objects.filter(user=user).annotate(
        content_type=Value('REVIEW', CharField())
    ).select_related('ticket', 'ticket__user')
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'post/posts.html', context={'posts': posts})


@login_required
def feed(request):
    user = request.user
    followed_users = user.following.all().values('pk')

    tickets = Ticket.objects.filter(
        Q(user__in=followed_users) | Q(user=user)
    ).annotate(
        content_type=Value('TICKET', CharField())
    )
    reviews = Review.objects.filter(
        Q(user__in=followed_users) | Q(user=user) | Q(ticket__user=user)
    ).annotate(
        content_type=Value('REVIEW', CharField())
    ).select_related('ticket', 'ticket__user')
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'post/feed.html', context={'posts': posts})