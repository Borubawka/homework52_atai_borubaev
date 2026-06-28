from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import UserRegisterForm

class RegisterView(CreateView):

    form_class = UserRegisterForm

    template_name = 'registration/register.html'

    success_url = reverse_lazy('index')

    def form_valid(self, form):

        response = super().form_valid(form)

        login(
            self.request,
            self.object
        )

        messages.success(
            self.request,
            'Регистрация прошла успешно!'
        )

        next_url = self.request.GET.get('next')

        if next_url:
            return redirect(next_url)

        return response