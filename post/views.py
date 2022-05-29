from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Ticket

class TicketCreateView(CreateView):
    model = Ticket
    fields = ['title', 'description', 'picture']
    template_name = 'post/ticket_form.html'
    success_url = reverse_lazy('post:posts')

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user = self.request.user
        self.object = ticket.save()
        return super().form_valid(form)
