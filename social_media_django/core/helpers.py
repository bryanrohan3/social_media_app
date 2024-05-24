from django.db.models import Q
from .models import FriendRequest, User

def get_user_friends(user):
    # Get friends of the current authenticated user using Q objects for complex queries
    friend_requests_sent = FriendRequest.objects.filter(from_user=user, status='accepted')
    friend_requests_received = FriendRequest.objects.filter(to_user=user, status='accepted')
    friends_requests = friend_requests_sent | friend_requests_received

    # Extract friends from the friend requests
    friends = [
        friend_request.from_user if friend_request.to_user == user else friend_request.to_user
        for friend_request in friends_requests
    ]
    
    return friends
