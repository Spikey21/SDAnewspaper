from django.shortcuts import render, get_object_or_404
from .models import Article, User
from .serializers import ArticleSerializer, UserSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from .paginators import UserPaginator
from rest_framework import filters

# Create your views here.

# podejscie przy użyciu funkcji
# @api_view(['GET','POST'])
# def create_article_list(request, format = None):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles,many=True)
#         # gdy tworzymy responsa przy uzyciu jsonresponse
#         # return JsonResponse({'articles':serializer.data})
#         # lepiej uzyc responsa z django_framework
#         return Response(serializer.data)
#     else:
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','DELETE','PUT'])
# def article_detail(request, articleId, format = None):
#     article = get_object_or_404(Article,id=articleId)
#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
# podejscie przy użyciu klas i mixins

# class ListCreateArticles(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class Article_Detail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# 3 podejscie przy użyciu klasy i genericsow

class ListCreateArticles(generics.ListCreateAPIView):
    # musi byc queryset, a nie inna nazwa
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # do testowania readarticle potrzeba zakomentowac 
    # filter_backends = [filters.OrderingFilter]
    # ordering = ['-date']
    def perform_create(self, serializer):
         serializer.save(owner=self.request.user)


class Article_Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ListUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # do testowania readarticle trzeba zakomentowac
    # pagination_class = UserPaginator

    def get_permissions(self):
        # permission_classes = [permissions.IsAdminUser] if self.request.method == "GET" else [permissions.AllowAny] # w wersja dwulinijkowa
        # return [permissions() for permissions in permission_classes]
        # return [permissions() for permissions in ([permissions.IsAdminUser] if self.request.method == "GET" else [permissions.AllowAny])] #wersja jednolinijkowa
        # wersja najkrótsza
        return [permissions.IsAdminUser() if self.request.method == "GET" else permissions.AllowAny()]


class APIRoot(APIView):
    def get(self, request, format = None):
            links = {
                'articles': reverse('articles',request=request),
                'users':reverse('users',request=request),
                'token':reverse('token',request=request),
            }
            return Response(links)
    