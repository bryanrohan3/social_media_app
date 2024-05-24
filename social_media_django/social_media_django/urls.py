from django.contrib import admin
from django.urls import path, include
from core import viewsets
from rest_framework import routers

api_router = routers.DefaultRouter()
api_router.register(r'users', viewsets.UserViewSet, basename='user')
api_router.register(r'posts', viewsets.PostViewSet, basename='post')
api_router.register(r'comments', viewsets.CommentViewSet, basename='comment')
api_router.register(r'likes', viewsets.LikeViewSet, basename='like')
api_router.register(r'friend-requests', viewsets.FriendRequestViewSet, basename='friend-request')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/unlike/', viewsets.LikeViewSet.as_view({'delete': 'unlike'}), name='unlike'),
     path('api/users/<int:pk>/block/', viewsets.UserViewSet.as_view({'post': 'block_user'}), name='user-block'),
    path('api/users/<int:pk>/unblock/', viewsets.UserViewSet.as_view({'post': 'unblock_user'}), name='user-unblock'),
]

