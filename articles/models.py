from django.db import models


class Article(models.Model):
    """article model."""

    id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=255, unique=True)
    published_at = models.DateTimeField()
    abstract = models.TextField()
    author = models.CharField(max_length=455)
    url = models.URLField(max_length=455)
    title = models.CharField(max_length=455)
    section_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    USERNAME_FIELD = 'external_id'

    def __str__(self):
        return self.title

class Summary(models.Model):
    """Summary model."""

    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="summaries")
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Summary for {self.article.title}"