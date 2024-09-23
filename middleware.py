from django.utils import translation
from django.conf import settings

class TRSLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.headers.get('Accept-Language', settings.LANGUAGE_CODE)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
        response = self.get_response(request)
        translation.deactivate()
        return response
