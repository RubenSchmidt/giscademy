from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.urls import reverse
from django.views.generic import FormView, View


class IndexView(View):
    form_class = UserCreationForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            # No need to show the index page, go straight to learn dashboard
            return HttpResponseRedirect(reverse('learn'))

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in for convenience.
            login(request, user)
            return HttpResponseRedirect(reverse('learn'))
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class RegistrationView(View):
    form_class = UserCreationForm
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in for convenience.
            login(request, user)
            return HttpResponseRedirect(reverse('learn'))
        return render(request, self.template_name, {'form': form})


class LearnView(View):
    template_name = 'learn.html'

    def get(self, request):
        return render(request, self.template_name)


class SandboxView(View):
    template_name = 'sandbox.html'

    def get(self, request):
        return render(request, self.template_name)
