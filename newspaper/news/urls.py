from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('articles/',views.create_article_list),
    path('articles/<int:articleId>/',views.article_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)