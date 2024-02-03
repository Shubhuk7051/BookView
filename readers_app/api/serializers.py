from rest_framework import serializers
from readers_app.models import BookModels, OnlineRetailer, ReviewModel


class BookSerializer(serializers.ModelSerializer):
    retailer=serializers.CharField(source='retailer.name', read_only=True)
    
    class Meta:
        model=BookModels
        exclude=('created',)
        

class RetailerSerializer(serializers.ModelSerializer):
    
    booklist=BookSerializer(many=True, read_only=True)
    
    class Meta:
        model=OnlineRetailer
        fields='__all__'
        
        
class ReviewSerializer(serializers.ModelSerializer):
    
    reviewer=serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model=ReviewModel
        exclude=('booklist',)
        