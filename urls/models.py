from django.db import models
from django.utils import timezone

class ShortURL(models.Model):
    short_code = models.CharField(max_length=32, unique=True, db_index=True)
    long_url = models.URLField(max_length=2048)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        if self.expires_at is None:
            return False
        return timezone.now() >= self.expires_at

    def __str__(self):
        return self.short_code