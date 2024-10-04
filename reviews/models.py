from django.db import models
from django.contrib import admin
from django.conf import settings


# Create your models here.


class Review(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete= models.CASCADE
    )
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    @admin.display(ordering= 'user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering= 'user__last_name')
    def last_name(self):
        return self.user.last_name
    
    description = models.TextField()
    reviewed_at = models.DateField(auto_now_add= True)
    review_updated_at = models.DateField(auto_now= True)

    WORST_RATING = '1'
    BAD_RATING = '2'
    GOOD_RATING = '3'
    BETTER_RATING = '4'
    EXCELLENT_RATING = '5'

    RATING_CHOICES = [
        (WORST_RATING, '1 Star'),
        (BAD_RATING, '2 Stars'),
        (GOOD_RATING, '3 Stars'),
        (BETTER_RATING, '4 Stars'),
        (EXCELLENT_RATING, '5 Stars')
        ]
    rating = models.CharField(max_length= 10, choices= RATING_CHOICES, default= GOOD_RATING, blank= True)
    rated_at = models.DateField(auto_now_add= True)
    rate_updated_at = models.DateField(auto_now= True)