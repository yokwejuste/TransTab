from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext as _


class SimpleView(APIView):
    def get(self, request, *args, **kwargs):
        message = _("Hello, world!")
        return Response({"message": message})
