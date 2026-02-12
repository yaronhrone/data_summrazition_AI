from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from articles.models import Article
from articles.serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    """Manage articles in the database."""
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
