from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=280)
    date_time_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Post by {self.user.username} at {self.date_time_created}'

    
class Like(models.Model):  # Define the Like model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # ForeignKey to link to the Post model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to the User model

    def __str__(self):  # String representation of the Like object
        return f'{self.user.username} liked {self.post}'

class Comment(models.Model):  # Define the Comment model
    is_active = models.BooleanField(default=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # ForeignKey to link to the Post model
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to the User model
    text = models.TextField()  # Text of the comment
    date_time_created = models.DateTimeField(auto_now_add=True)  # Date and time when the comment was created

    def __str__(self):  # String representation of the Comment object
        return f'Comment by {self.user.username} on {self.post}'


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    date_time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # Ensures only one request between two users

    def __str__(self):
        return f"Friend request from {self.from_user} to {self.to_user}"


class Block(models.Model):
    blocker = models.ForeignKey(User, related_name='blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked_by', on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f'{self.blocker.username} blocked {self.blocked.username}'
