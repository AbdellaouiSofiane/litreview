from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSetFactory
from .forms import ReviewForm, TicketUpdateForm
from .models import Ticket, Review


class TicketCreateView(CreateView):
    model = Ticket
    fields = ['title', 'description', 'picture']
    success_url = reverse_lazy('post:posts')

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        self.object = ticket.save()
        return super().form_valid(form)


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    success_url = reverse_lazy('post:posts')


class ReviewInline(InlineFormSetFactory):
    model = Review
    form_class = ReviewForm
    factory_kwargs = {'extra': 1, 'can_delete': False}


class TicketAndReviewCreateView(CreateWithInlinesView):
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
