# Import necessary modules and serializers
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, mixins, permissions
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, status
from django.contrib.auth import authenticate 
from rest_framework.decorators import action
# Import Serializer and Models
from .serializers import UserSerializer, UserLoginSerializer, PostSerializer, LikeSerializer, CommentSerializer, FriendRequestSerializer, BlockSerializer, ShortCommentSerializer
from .models import Post, Like, Comment, FriendRequest, Block
from django.db.models import Q  # Import the Q object
from .helpers import get_user_friends  # Import the helper function
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from django.http import Http404





def filter_blocked_objects(queryset, user):
    # Filter queryset to exclude objects blocked by the user.
    blocked_users = Block.objects.filter(blocker=user).values_list('blocked', flat=True)
    return queryset.exclude(pk__in=blocked_users)


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin):
    queryset = User.objects.all() # Define queryset
    serializer_class = UserSerializer # Define serializer class

    serializer_classes = {
        'login': UserLoginSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action,
            super().get_serializer_class(),
        )

    def filter_queryset(self, queryset):
        # Filter the queryset to only include the authenticated user's information
        queryset = super().filter_queryset(queryset)
        full_availability_actions = ["list"]
        available_to_current_user_only = ["update", "partial_update"]

        all_actions = full_availability_actions + available_to_current_user_only

        if self.action in full_availability_actions:
            queryset = queryset
        if self.action in available_to_current_user_only: 
            queryset = queryset.filter(pk=self.request.user.pk) # current user

        # Exclude blocked users
        blocked_users = Block.objects.filter(blocker=self.request.user).values_list('blocked', flat=True)
        queryset = queryset.exclude(pk__in=blocked_users)

        if self.action not in all_actions:
            queryset = queryset.none()

        return queryset
    
    def list(self, request, *args, **kwargs):
        query = request.query_params.get('query', '')
        users = self.filter_queryset(self.get_queryset()).filter(username__icontains=query)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], url_path='current')
    def current(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object() # Get the instance of the user to be updated
        serializer = self.get_serializer(instance, data=request.data, partial=True) # Initialize the serializer with the instance and request data
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer) # Perform the update using the serializer

        return Response(serializer.data, status=status.HTTP_200_OK) # Return a response with the updated user data

    # Creating A User
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # Initialize UserSerializer with request data
        print(serializer)
        serializer.is_valid(raise_exception=True) # Validate serializer data
        user = serializer.save() # Save user using serializer
        return Response({'user': serializer.data}, status=status.HTTP_201_CREATED) # Return response with user data

    # LogIn
    # @action(detail=False, methods=['POST'], permission_classes=[])
    # def login(self, request):
    #     serializer = self.get_serializer(data=request.data) # Initialize UserLoginSerializer with request data
    #     serializer.is_valid(raise_exception=True) # Validate serializer data
        
    #     user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password']) # Authenticate user with provided username and password
    #     print(user)
    #     # If authentication is successful
    #     if user is not None:
    #         # Return response with success message and user data
    #         return Response({'message': 'Login successful', 'user': UserSerializer(user).data})
    #     else:
    #         # Return response with error message for invalid credentials
    #         return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST) 
    
    @action(detail=False, methods=['POST'], permission_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        
        if user is not None:
            login(request, user)  # Log the user in
            
            # Generate or retrieve the authentication token for the user
            token, created = Token.objects.get_or_create(user=user)
            print(request, user)
            print(token)
            
            # Return response with success message, user data, and authentication token
            return Response({'message': 'Login successful', 'user': UserSerializer(user).data, 'token': token.key})
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        
    # BLOCKING USERS
    @action(detail=True, methods=['POST'], url_name='block')
    def block_user(self, request, pk=None):
        blocked_user = get_object_or_404(User, pk=pk) # Retrieve the user based on the provided pk
        blocker = request.user # user doing the blocking

        if blocker == blocked_user:
            return Response({'error': 'You cannot block yourself'}, status=status.HTTP_400_BAD_REQUEST)

        block, created = Block.objects.get_or_create(blocker=blocker, blocked=blocked_user)
        if not created:
            return Response({'error': 'User is already blocked'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BlockSerializer(block)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'], url_name='unblock')
    def unblock_user(self, request, pk=None):
        # Retrieve the user based on the provided pk
        blocked_user = get_object_or_404(User, pk=pk)
        blocker = request.user

        block = Block.objects.filter(blocker=blocker, blocked=blocked_user).first()
        if not block:
            return Response({'error': 'User is not blocked'}, status=status.HTTP_400_BAD_REQUEST)

        block.delete()
        return Response({'message': 'User unblocked successfully'}, status=status.HTTP_200_OK)


# TODO: Remove the destroy mixin
# Alternatively, override the destroy method to soft delete the user in either the ViewSet or the Serializer (prob viewset is better)
# 2 Thoughts:
# Either, remove Retrieve Model Mixin because we never use it.
# Or
# Use seperate serializers for Retrieve and List and pick a point of difference for them
# An example of when this is good: 
# A Post has 50 likes. On the feed, you only want to show the number of likes, eg: "Hello World" -> "This post has 50 likes" 
# But when you click on the post, you want to see the users who liked the post
# TODO: Implement "Has been edited"
# Multiple ways to do this:
# 1. Add a field to the model that is a timestamp of the last edit -> In serializer, if this field exists, make a custom field that says "Has been edited" or is a boolean
# 2. Add a field to the model that is a boolean that is set to true when the post is edited -> Set to true in update
class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PostSerializer  # Commented out to use default serializer class

    def get_queryset(self):
        queryset = Post.objects.all()

        queryset = filter_blocked_objects(queryset, self.request.user)

        # Check if a username parameter is provided in the query parameters
        username = self.request.query_params.get('username')
        user_id = self.request.query_params.get('user_id')

        if username:
            user = get_object_or_404(User, username=username)
            queryset = queryset.filter(user=user)
        elif user_id:
            user = get_object_or_404(User, pk=user_id)
            queryset = queryset.filter(user=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Save post with authenticated user

    @action(detail=False, methods=['GET'])
    def my_posts(self, request):
        # Get posts of the current authenticated user
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='friends_posts')
    def friends_posts(self, request):
        # Use the helper function to get friends of the current authenticated user
        friends = get_user_friends(request.user)

        # Get posts created by friends of the current authenticated user
        posts = self.get_queryset().filter(user__in=friends)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'], url_path='likes')
    def post_likes(self, request, pk=None):
        post = self.get_object()
        likes = Like.objects.filter(post=post)
        likes = filter_blocked_objects(likes, self.request.user)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class LikeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = filter_blocked_objects(queryset, self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        post_id = request.data.get('post')
        if not post_id:
            return Response({'error': 'post parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, id=post_id)
        post_owner = post.user

        if Block.objects.filter(blocker=request.user, blocked=post_owner).exists() or Block.objects.filter(blocker=post_owner, blocked=request.user).exists():
            return Response({'error': 'You cannot like this post'}, status=status.HTTP_400_BAD_REQUEST)

        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unlike(self, request, *args, **kwargs):
        like_id = request.query_params.get('like')
        print("Received like_id:", like_id)  # Add this line
        if not like_id:
            return Response({'error': 'like parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            like = Like.objects.get(id=like_id, user=request.user)
        except Like.DoesNotExist:
            print("Like not found")  # Add this line
            return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    # This prepares us for different serializers
    # List serializer is like first 50 characters
    # Retrieve serializer is full comment
    # TODO:
    serializer_classes = {
        'list': CommentSerializer,
        'create': CommentSerializer,
        'update': CommentSerializer,
        'partial_update': CommentSerializer,
        'retrieve': CommentSerializer,
        'short_list': ShortCommentSerializer
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action,
            super().get_serializer_class(),
        )

    def get_queryset(self):
        # I would use the super, but this is fine
        # If you ever want to change the object of this viewset, you would have to change it in two places
        queryset = Comment.objects.all()
        queryset = filter_blocked_objects(queryset, self.request.user)
        return queryset

    def filter_queryset(self, queryset):
        # Filter the queryset based on the action
        queryset = super().filter_queryset(queryset)

        if self.action in ['update', 'partial_update', 'destroy']:
            # Allow users to update or delete only their own comments
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def destroy(self, request, *args, **kwargs):
        # This is really good!
        instance = self.get_object()
        # Soft delete the comment by marking it as inactive
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        post_id = request.query_params.get('post_id')
        latest = request.query_params.get('latest')  # Add this line

        if post_id is None:
            return super().list(request, *args, **kwargs)

        comments = self.get_queryset().filter(post_id=post_id)
        comments = filter_blocked_objects(comments, self.request.user)

        if latest:  # Add this block to handle the latest comment
            comments = comments.order_by('-date_time_created')[:1]
            self.action = 'short_list'  # Change action to use the short serializer

        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        # Ensure the user is not blocked or blocking the owner of the post they are commenting on
        post_id = request.data.get('post')
        post = get_object_or_404(Post, pk=post_id)
        post_owner = post.user
        # Use helper function
        if Block.objects.filter(blocker=request.user, blocked=post_owner).exists() or Block.objects.filter(blocker=post_owner, blocked=request.user).exists():
            return Response({'error': 'You cannot comment on this post'}, status=status.HTTP_400_BAD_REQUEST)

        # Associate the comment with the currently authenticated user
        # This can be done in the serialzier, but this is fine
        # The better way is to use the serializer, but this works
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Associate the comment with the currently authenticated user
        # TODO: I would do this in the serializer, but this is fine
        serializer.save(user=self.request.user)


class FriendRequestViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = FriendRequest.objects.all()  # Queryset for FriendRequestViewSet
    serializer_class = FriendRequestSerializer  # Serializer class for FriendRequestViewSet

    serializer_classes = {
        'create': FriendRequestSerializer,  # Serializer class for create action
        'friends': UserSerializer,  # Serializer class for friends action
        'pending_requests': FriendRequestSerializer,  # Serializer class for pending_requests action
    }

    def get_serializer_class(self):
        # Customizes serializer class based on action.
        return self.serializer_classes.get(
            self.action,
            super().get_serializer_class(),
        )

    def get_queryset(self):
        #  Retrieves the queryset based on the action and user_id.
        user_id = self.request.query_params.get('user_id', self.request.user.id)  # Retrieve user_id from request params, default to current user
        user = get_object_or_404(User, pk=user_id)  # Get the User object using the user_id

        if self.action == 'friends':
            # Retrieve friends who have accepted friend requests and are not blocked
            friends = (
                User.objects
                .filter(Q(sent_friend_requests__to_user=user, sent_friend_requests__status='accepted') | 
                        Q(received_friend_requests__from_user=user, received_friend_requests__status='accepted'))
                .exclude(pk__in=Block.objects.filter(blocker=user).values_list('blocked', flat=True))  # Exclude blocked users
            )
            return friends

        elif self.action == 'pending_requests':
            # Retrieve pending friend requests for the user
            return FriendRequest.objects.filter(to_user=user, status='pending')

        return super().get_queryset()    # Call parent class method if action is not 'friends' or 'pending_requests'
    
    @action(detail=False, methods=['get'])
    def friends_count(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', request.user.id)
        user = get_object_or_404(User, pk=user_id)
        
        friends_count = (
            User.objects
            .filter(Q(sent_friend_requests__to_user=user, sent_friend_requests__status='accepted') | 
                    Q(received_friend_requests__from_user=user, received_friend_requests__status='accepted'))
            .exclude(pk__in=Block.objects.filter(blocker=user).values_list('blocked', flat=True))
            .count()
        )
        
        return Response({'friends_count': friends_count})


    def update(self, request, *args, **kwargs):
        # Updates the status of a friend request.
        instance = self.get_object()  # Get the friend request instance
        status = request.data.get('status')  # Retrieve status from request data
        if status not in ['accepted', 'rejected', 'pending']:
            return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = status  # Update the status
        instance.save()  # Save the instance
        serializer = self.get_serializer(instance)  # Serialize the instance
        return Response(serializer.data)  # Return the serialized data

    @action(detail=False, methods=['GET'])
    def friends(self, request):
        # Retrieves the list of friends.
        queryset = self.filter_queryset(self.get_queryset())  # Filter queryset based on request
        serializer = self.get_serializer(queryset, many=True)  # Serialize queryset
        return Response(serializer.data)  # Return serialized data

    @action(detail=False, methods=['GET'])
    def pending_requests(self, request):
        # Retrieves pending friend requests.
        queryset = self.filter_queryset(self.get_queryset())  # Filter queryset based on request
        received_requests = queryset.filter(status='pending', to_user=request.user)  # Filter received requests
        sent_requests = queryset.filter(status='pending', from_user=request.user)  # Filter sent requests
        received_serializer = self.get_serializer(received_requests, many=True)  # Serialize
        sent_serializer = FriendRequestSerializer(sent_requests, many=True)

        return Response({
            'received_requests': received_serializer.data,
            'sent_requests': sent_serializer.data
        })
