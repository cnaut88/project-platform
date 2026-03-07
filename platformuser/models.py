from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ("user","User"),
        ("admin","Admin"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.username

    
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ProjectTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = (
        ("idea","Idea"),
        ("in_progress","In progress"),
        ("mvp","Mvp"),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="projects")
    title = models.CharField(max_length=200)
    descriphion = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="idea")
    git_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/images/", blank=True, null=True)
    file = models.FileField(upload_to="projects/files/", blank=True, null=True)
    tags = models.ManyToManyField(ProjectTag, blank=True)
    created_a = models.DateField(auto_now_add=True)
    updated_a = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class ProjectLike(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user} likes {self.project}"
    
class ProjectComment(models.Model):
    FEEDBACK_TYPES = (
        ("feedback","Feedback"),
        ("idea","Idea"),
        ("bug","Bug"),
    )
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.TextField()
    type =  models.CharField(max_length=20,choices=FEEDBACK_TYPES,default = "feedback")
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.author}"
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="subscriptions")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="subscribers")
    class Meta:
        unique_together = ("subscriber", "author")

    def __str__(self):
        return f"{self.subscriber} -> {self.author}"
video_url = models.URLField(blank=True)

class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to="projects/images/", blank=True, null=True)
    video_url = models.URLField(blank=True)