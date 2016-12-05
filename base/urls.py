from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'redirect_field_name': '/learn/'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^sandbox/$', views.SandboxView.as_view(), name='sandbox'),
    url(r'^learn/$', views.LearnView.as_view(), name='learn'),
    url(r'^learn/(?P<slug>[-\w]+)/$', views.CourseDetailView.as_view(), name='learn-course-detail'),
    url(r'^catalog/$', views.CatalogView.as_view(), name='catalog'),

]
