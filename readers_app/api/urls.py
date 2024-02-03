from django.urls import path
from readers_app.api.views import BookListGV, BookDetailAV, RetailerListAV, RetailerDetailAV, ReviewList, ReviewDetail,ReviewCreate, UserReview

urlpatterns = [
    path('list/', BookListGV.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailAV.as_view(), name='book-detail'),
    path('retail/', RetailerListAV.as_view(), name='retail-list'),
    path('retail/<int:pk>/', RetailerDetailAV.as_view(), name='retail-detail'),
    path ('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name= 'review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name= 'review-detail'),
    path('reviews/', UserReview.as_view(), name= 'user-review-detail'),

]