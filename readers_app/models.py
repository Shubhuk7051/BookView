from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class OnlineRetailer(models.Model):
    
    name=models.CharField(max_length=50)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=100)
    
    def __str__(self):
        return self.name

class BookModels(models.Model):
    
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    author=models.CharField(max_length=50)
    retailer=models.ForeignKey(OnlineRetailer, on_delete=models.CASCADE, related_name='books', blank=True, null=True)
    active=models.BooleanField(default=True)
    genre=models.CharField(max_length=50)
    avg_rating=models.FloatField(default=0)
    number_of_reviews=models.IntegerField(default=0)
    created=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.id) + " | " + self.title
    
    
class ReviewModel(models.Model):
    
    reviewer=models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description=models.CharField(max_length=200, null=True)
    booklist=models.ForeignKey(BookModels, on_delete=models.CASCADE, related_name='reviews')
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    
    
    def __str__(self):
        return str(self.rating) + " | " + self.booklist.title + " | " + str(self.reviewer)
