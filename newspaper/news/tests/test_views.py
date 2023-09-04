from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Article
from django.urls import reverse
from rest_framework import status
from ..serializers import ArticleSerializer

class ReadArticleTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testUser', password = '12345'
        )
        self.articles = [
            Article.objects.create(
            title = 'Test Article 1', text = 'This is a test',
            owner = self.user),
            Article.objects.create(
            title = 'Test Article 2', text = 'This is a test',
            owner = self.user),
            Article.objects.create(
            title = 'Test Article 3', text = 'This is a test',
            owner = self.user)
        ]
        self.expected_data = ArticleSerializer(self.articles, many = True)
        self.urlList = reverse('articles')
        # self.urlRetrieve = reverse('articleDetail')

    def test_list_articles(self):
        response = self.client.get(self.urlList)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data.data)

class CreateArticleTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testUser', password = '12345'
        )
        self.data = {'title':'Hello world','text':'Something intrest.'}
        self.url = reverse('articles')
        self.client.force_authenticate(self.user)

    def test_create_article(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)