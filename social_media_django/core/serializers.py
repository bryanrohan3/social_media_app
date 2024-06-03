from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Post, Like, Comment, FriendRequest, Block


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.CharField(source='user.username', read_only=True)
    liked = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'caption', 'date_time_created', 'username', 'user', 'is_active', 'liked', 'like_id']

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(post=obj, user=request.user).exists()
        return False

    def get_like_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            like = Like.objects.filter(post=obj, user=request.user).first()
            return like.id if like else None
        return None

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    username = serializers.CharField(source='user.username', read_only=True)  # Include the username

    class Meta:
        model = Like
        fields = ['id', 'user', 'username', 'post']

    def validate(self, attrs):
        request = self.context['request']
        post = attrs.get('post')

        if not post:
            raise serializers.ValidationError('Post is required.')

        if Block.objects.filter(blocker=request.user, blocked=post.user).exists():
            raise serializers.ValidationError('You are blocked by the post owner.')
        if Block.objects.filter(blocker=post.user, blocked=request.user).exists():
            raise serializers.ValidationError('The post owner is blocking you.')

        if Like.objects.filter(post=post, user=request.user).exists():
            raise serializers.ValidationError('You have already liked this post.')

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'date_time_created', 'username', 'is_active']

class ShortCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'date_time_created', 'username']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())    
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'date_time_created']

    def validate_to_user(self, value):
        # Check if the requesting user has already sent a friend request to the recipient
        if FriendRequest.objects.filter(from_user=self.context['request'].user, to_user=value).exists():
            raise serializers.ValidationError('A friend request has already been sent to this user.')
        return value

    def create(self, validated_data):
        # Add the requesting user to the validated data and create the friend request
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['blocker', 'blocked', 'date_time_created']