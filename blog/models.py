from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title       = models.CharField(max_length=200)
    content     = models.TextField(blank=True)
    link        = models.URLField(blank=True, null=True)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at  = models.DateTimeField(default=timezone.now)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_posts')
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def short_description(self):
        if len(self.content) > 200:
            return self.content[:200] + '…'
        return self.content
