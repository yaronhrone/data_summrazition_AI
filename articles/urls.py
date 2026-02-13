from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleSummaryView, ArticleViewSet

router = DefaultRouter()
router.register('article', ArticleViewSet)



urlpatterns = [
    path('', include(router.urls), name='article-list'),
    path("articles/<int:pk>/summary/", ArticleSummaryView.as_view(), name="article-summary"),

        ]
