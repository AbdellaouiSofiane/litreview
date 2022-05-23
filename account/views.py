from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.edit import FormView

from .forms import SubscriptionForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('account:login')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SubscriptionsView(LoginRequiredMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    template_name = 'account/subscriptions.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription_form'] = SubscriptionForm()
        return context


@login_required
@require_POST
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(get_user_model(), pk=user_id)
    if user_to_unfollow in request.user.following.all():
        request.user.following.remove(user_to_unfollow)
    return redirect('account:subscriptions')


@login_required
@require_POST
def subscribe(request):
    form = SubscriptionForm(request.POST)
    if form.is_valid():
        user_follows = form.save(commit=False)
        if user_follows.followed_user not in request.user.following.all():
            user_follows.user = request.user
            user_follows.save()
    return redirect('account:subscriptions')