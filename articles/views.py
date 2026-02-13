from django.shortcuts import render
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView


from articles.services.summary_service import get_or_create_summary
from articles.models import Article
from articles.serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    """Manage articles in the database."""
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleSummaryView(APIView):
    """View to get article summary."""

    def get(self, request, pk):
        """Get the summary for an article."""
        article = get_object_or_404(Article, pk=pk)

        summary = get_or_create_summary(article)

        return Response({'summary': summary}, status=status.HTTP_200_OK)