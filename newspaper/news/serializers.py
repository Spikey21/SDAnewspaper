from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError 

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'date', 'owner')
        read_only_fields = ('owner',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = False,
        validators = [
            UniqueValidator(
                queryset = User.objects.all(),
                message = "A user with that email already exists."
            )
        ]
    )

    # articles = serializers.PrimaryKeyRelatedField(
    #     queryset=Article.objects.all(), many=True)
    # articles = serializers.StringRelatedField(many=True)
    articles = serializers.HyperlinkedRelatedField(
        view_name='articleDetail', 
        queryset=Article.objects.all(), 
        many=True)

    
    class Meta:
        model = User
        fields = ('id','username','email','password','articles')
        extra_kwargs = {'password':{'write_only':True}}
    
    # walidacja hasła
    # walidacja username +
    # walidacja email (format) +
    # walidacja maila (zajety) +
    # email opcjonalny +
    def create(self, validated_data): #request.data
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise exceptions.ValidationError({'password':e.messages})
        user = User.objects.create_user(username,email,password)
        return user