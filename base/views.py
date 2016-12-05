from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View

from courses.models import Course


@method_decorator(login_required, name='dispatch')
class ProtectedView(View):
    """
    Mixin for decorating the dispatch function with login_required decorator
    """
    pass


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


class LearnView(ProtectedView):
    template_name = 'learn.html'

    def get(self, request):
        user = request.user
        courses = Course.objects.filter(enrollment__user=user)
        return render(request, self.template_name, {'courses': courses})


class CatalogView(ProtectedView):
    template_name = 'catalog.html'
    valid_params = ['easy', 'medium', 'expert']

    def get(self, request):
        courses = Course.objects.all()
        difficulty_filter = request.GET.get('courses')
        if difficulty_filter and difficulty_filter in self.valid_params:
            courses = courses.filter(**{'difficulty': difficulty_filter})

        # Annotate the courses where the user is enrolled
        user_courses = request.user.enrollment_set.all().values_list('course_id', flat=True)
        for course in courses:
            if course.id in user_courses:
                course.user_is_enrolled = True

        return render(request, self.template_name, {'courses': courses})

    def post(self, request):
        course_id = request.POST.get('course_id')
        try:
            course = Course.objects.get(id=int(course_id))
            course.enroll(request.user)
            return HttpResponseRedirect(reverse('learn'))
        except Course.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('catalog'))


class SandboxView(View):
    template_name = 'sandbox.html'

    def get(self, request):
        return render(request, self.template_name)
