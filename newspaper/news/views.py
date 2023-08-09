from django.shortcuts import render, get_object_or_404
from .models import Article
from .serializers import ArticleSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.

@api_view(['GET','POST'])
def create_article_list(request, format = None):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        # gdy tworzymy responsa przy uzyciu jsonresponse
        # return JsonResponse({'articles':serializer.data})
        # lepiej uzyc responsa z django_framework
        return Response(serializer.data)
    else:
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','DELETE','PUT'])
def article_detail(request, articleId, format = None):
    article = get_object_or_404(Article,id=articleId)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        