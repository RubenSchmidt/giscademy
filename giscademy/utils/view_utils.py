from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
class ProtectedView(View):
    """
    Mixin for decorating the dispatch function with login_required decorator
    """
    pass
