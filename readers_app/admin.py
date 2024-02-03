from django.contrib import admin
from readers_app.models import BookModels, OnlineRetailer, ReviewModel

# Register your models here.
admin.site.register(BookModels)
admin.site.register(OnlineRetailer)
admin.site.register(ReviewModel)