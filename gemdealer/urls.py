from .api import DealsGetView, DealsUploadView
from django.urls import re_path, path

urlpatterns = [
    re_path(r'^api/post/(?P<filename>[^/]+)$', DealsUploadView.as_view()),
    path('api/get/', DealsGetView.as_view()),
]
