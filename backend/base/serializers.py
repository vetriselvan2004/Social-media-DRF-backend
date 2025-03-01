from rest_framework import serializers
from .models import MyUser, Post

class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = MyUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class MyUserProfileSerializer(serializers.ModelSerializer):

    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['username', 'bio', 'profile_image', 'follower_count', 'following_count']

    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()
    

class PostSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    user_profile_image = serializers.SerializerMethodField()

    class Meta:
        
        model = Post
        fields = ['id', 'username', 'description', 'formatted_date','post_image','likes', 'like_count','user_profile_image']
    
    def get_user_profile_image(self, obj):
            if obj.user.profile_image:
                return obj.user.profile_image.url  # 👈 Returns the image URL
            return None  # 👈 If no image, return None

    def get_post_image_url(self, obj):
        request = self.context.get('request')  # ✅ Get request from serializer context
        if obj.post_image:
            return request.build_absolute_uri(obj.post_image.url)  # ✅ Returns full image URL
        return None  
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_formatted_date(self, obj):
        return obj.created_at.strftime("%d %b %y")
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'bio', 'email', 'profile_image', 'first_name', 'last_name']
