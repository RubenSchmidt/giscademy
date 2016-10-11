from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.views.generic import FormView, View


def index(request):
    return render(request, 'index.html')


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
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})
