from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "external_id",
            "title",
            "abstract",
            "author",
            "published_at",
            "url",
            "section_name"
        ]
        read_only_fields = ["external_id" ,"id", ]

