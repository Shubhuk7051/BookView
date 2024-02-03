from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle , ScopedRateThrottle
from rest_framework import filters
# from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from readers_app.models import BookModels, OnlineRetailer, ReviewModel
from readers_app.api.serializers import BookSerializer, RetailerSerializer, ReviewSerializer
from readers_app.api.permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly,IsAuthenticatedUser
from readers_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from readers_app.api.pagination import BookListLOPagination


class BookListGV(generics.ListCreateAPIView):
    
    queryset=BookModels.objects.all()
    serializer_class=BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title', 'retailer__name', 'genre']
    ordering_fields = ['title', 'avg_rating']
    pagination_class=BookListLOPagination 
    

# class BookListAV(APIView):
    
#     permission_classes = [IsAdminOrReadOnly]

#     def get(self, request):
#         books=BookModels.objects.all()
#         serializer=BookSerializer(books, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
        
#         serializer=BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         else:
#             return Response(serializer.errors)
        
        
class BookDetailAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        
        try:
            
            books=BookModels.objects.get(pk=pk)
            
        except BookModels.DoesNotExist:
            return Response({'Error' : 'Not Found' })
        
        serializer=BookSerializer(books)
        return Response(serializer.data)
    
    def put(self,request, pk):
        
        books=BookModels.objects.get(pk=pk)
        serializer=BookSerializer(books, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)
        
        
    def delete(self, request, pk):
        
        books=BookModels.objects.get(pk=pk)
        books.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class RetailerListAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    
    def get(self, request):
        
        retailers=OnlineRetailer.objects.all()
        r_serializer=RetailerSerializer(retailers, many=True)
        return Response(r_serializer.data)
    
    def post(self, request):
        
        r_serializer=RetailerSerializer(data=request.data)
        if r_serializer.is_valid():
            r_serializer.save()
            return Response(r_serializer.data)
        else:
            return Response(r_serializer.errors)
        
class RetailerDetailAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        
        try:
            
            retailer=OnlineRetailer.objects.get(pk=pk)
            
        except OnlineRetailer.DoesNotExist:
            return Response({'Error' : 'Not Found' })
        
        r_serializer=RetailerSerializer(retailer)
        return Response(r_serializer.data)
    
    def put(self,request, pk):
        
        retailer=OnlineRetailer.objects.get(pk=pk)
        r_serializer=RetailerSerializer(retailer, data=request.data)
        if r_serializer.is_valid():
            r_serializer.save()
            return Response(r_serializer.data)
        
        else:
            return Response(r_serializer.errors)
        
        
    def delete(self, request, pk):
        
        retailer=OnlineRetailer.objects.get(pk=pk)
        retailer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ReviewList(generics.ListCreateAPIView):
    
    
    permission_classes = [IsAuthenticatedUser]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewer__username', 'booklist__title']
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes=[ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
    
class ReviewCreate(generics.CreateAPIView):
    
    
    throttle_classes = [ReviewCreateThrottle]
    permission_classes = [IsAuthenticatedUser]
    
    def get_queryset(self):
        return ReviewModel.objects.all()
    
    serializer_class=ReviewSerializer
    
    def perform_create(self, serializer):
        
        pk=self.kwargs.get('pk')
        books=BookModels.objects.get(pk=pk)
        
        user=self.request.user
        user_queryset=ReviewModel.objects.filter(booklist=books, reviewer=user)
        
        if user_queryset.exists():
            raise ValidationError("You have already review this book!")
        
        if books.number_of_reviews==0:
            books.avg_rating=serializer.validated_data['rating']
        
        else:
            books.avg_rating= (books.avg_rating + serializer.validated_data['rating'])/2
        books.number_of_reviews+=1
        books.save()
        
        
        serializer.save(booklist=books, reviewer=user)
        
        
class UserReview(generics.ListAPIView): #To get review from an individual user
    
    permission_classes=[IsAuthenticatedUser]
            
    serializer_class=ReviewSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return ReviewModel.objects.filter(reviewer__username=username)
        
    
    