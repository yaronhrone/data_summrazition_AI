
from django.shortcuts import get_object_or_404
from django.core.cache import cache

from drf_spectacular.utils import extend_schema

from rest_framework import  status, viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView


from articles.services.summary_service import get_or_create_summary
from articles.models import Article
from articles.serializers import ArticleSerializer , ArticleSummarySerializer
from articles.constants import ARTICLES_LIST_CACHE_KEY

@extend_schema(tags=["Articles"])
class ArticleViewSet(viewsets.ModelViewSet):
    """Manage articles in the database."""
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by("-published_at")

    def list(self, request, *args, **kwargs):
        """List all articles."""
        page = request.query_params.get("page", 1)
        cache_key = f"{ARTICLES_LIST_CACHE_KEY}_page_{page}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=21600)
        return response

    def perform_create(self, serializer):
        serializer.save()
        cache.delete_pattern(f"{ARTICLES_LIST_CACHE_KEY}_page_*")

    def perform_update(self, serializer):
        serializer.save()
        cache.delete_pattern(f"{ARTICLES_LIST_CACHE_KEY}_page_*")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete_pattern(f"{ARTICLES_LIST_CACHE_KEY}_page_*")


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all().order_by("-published_at")
    serializer_class = ArticleSerializer


class ArticleSummaryView(APIView):
    """View to get article summary."""
    @extend_schema(
        summary="Retrieve AI summary for an article",
        description="Returns a cached or AI-generated summary for the given article ID.",
        responses={200: ArticleSummarySerializer, 404: "Article not found"}
    )
    def get(self, request, pk):
        """Get the summary for an article."""
        article = get_object_or_404(Article, pk=pk)

        summary = get_or_create_summary(article)
        serializer = ArticleSummarySerializer({"summary": summary})
        return Response(serializer.data, status=status.HTTP_200_OK)