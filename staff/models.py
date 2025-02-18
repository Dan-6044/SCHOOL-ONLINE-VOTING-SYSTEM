from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='candidates/')
    email = models.EmailField(unique=True)  # Ensure this field exists
    admission_number = models.CharField(max_length=50, unique=True)  # Ensure this field exists
    votes = models.IntegerField(default=0)  # Track votes


class Voter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    reg_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    voter_code = models.CharField(max_length=10, unique=True)
    voted_candidate = models.ForeignKey('Candidate', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.voter_code})"

from django.db import models
from django.contrib.auth.models import User

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Profile"
