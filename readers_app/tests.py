from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from readers_app.api.serializers import *
from readers_app import models


class OnlineRetailerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example1", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.retail = models.OnlineRetailer.objects.create(name="Amazon", 
                                about="Biggest Online Retailer in the World", website="https://www.amazon.in")

    def test_onlineretail_create(self):
        data = {
            "name": "Amazon",
            "about": "Biggest Online Retailer in the World",
            "website": "https://www.amazon.in"
        }
        response = self.client.post(reverse('retail-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_onlineretail_list(self):
        response = self.client.get(reverse('retail-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_onlineretail_ind(self):
        response = self.client.get(reverse('retail-detail', args=(self.retail.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_onlineretail_update(self):
        data={
            "name": "Amazon",
            "about": "Online Retailer in the world",
            "website": "https://www.amazon.in"
        }
        response=self.client.put(reverse('retail-detail', args=(self.retail.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_onlineretail_delete(self):
        response=self.client.delete(reverse('retail-detail', args=(self.retail.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        


class BookListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.retail = models.OnlineRetailer.objects.create(name="Flipkart",
                                about="Online Retailer", website="https://www.flipkart.com")
        self.booklist = models.BookModels.objects.create(retailer=self.retail, title="Atomic Habits",
                                description="To motivate to build good habits",author="James Clear", active=True)

    def test_booklist_create(self):
        data = {
            "retailer": self.retail,
            "title": "Atomic Habits",
            "description": "To motivate to build good habits",
            "author": "James Clear",
            "active": True
        }
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_booklist_list(self):
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_bookist_ind(self):
        response = self.client.get(reverse('book-detail', args=(self.booklist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.BookModels.objects.count(), 1)
        self.assertEqual(models.BookModels.objects.get().title, 'Atomic Habits')
        
    def test_booklist_update(self):
        data={
            "retailer": self.retail,
            "title": "Atomic Habits",
            "description": "Give formula to motivate to build good habits",
            "author": "James Clear",
            "active": True
        }
        response=self.client.put(reverse('book-detail', args=(self.booklist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.retail = models.OnlineRetailer.objects.create(name="Flipkart", 
                                about="Online Retailer", website="https://www.flipkart.com")
        self.booklist = models.BookModels.objects.create(retailer=self.retail, title="Atomic Habits",
                                description="To motivate to build good habits",author="James Clear", active=True)
        self.booklist2 = models.BookModels.objects.create(retailer=self.retail, title="Atomic Habits",
                                description="To motivate to build good habits",author="James Clear", active=True)
        self.review = models.ReviewModel.objects.create(reviewer=self.user, rating=5, description="Great Book", 
                                booklist=self.booklist2, active=True)
    
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Book!",
            "watchlist": self.booklist,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=(self.booklist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.ReviewModel.objects.count(), 2)
        # self.assertEqual(models.ReviewModel.objects.get().rating, 5)

        response = self.client.post(reverse('review-create', args=(self.booklist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)#If the user create review second time for the same movie

    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Bppk!",
            "watchlist": self.booklist,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.booklist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Great Book! - Updated",
            "watchlist": self.booklist,
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.booklist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/book/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
