from django.db import models

# Create your models here.
class HomeCards(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    roommate_score = models.IntegerField(max_length=255, blank=True, null=True)
    housing_score = models.IntegerField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Profile'