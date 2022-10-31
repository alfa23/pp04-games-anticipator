from django.conf import settings
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Game(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    dev_pub = models.CharField(max_length=200)
    release_date = models.DateField()
    feature_image = models.CloudinaryField('image', default='placeholder')
    website = models.URLField()
    game_info = models.TextField()
    info_excerpt = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )

    class Meta:
        ordering = ['release_date']

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    """
    Rating method theory & constraints settings below referenced/sourced from:
    https://stackoverflow.com/questions/58115738/realizing-rating-in-django
    """
    class Meta:
        constraints = [
            CheckConstraint(check=Q(rate__range=(0, 5)), name='valid_rate'),
            UniqueConstraint(fields=['user', 'game'], name='rating_once')
        ]

    def __str__(self):
        return self.rating


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User, related_name='comment_likes', blank=True)

    class Meta:
        ordering = ['posted_on']

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment {self.content} by {user.first_name} {user.last_name}"
