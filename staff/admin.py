from django.contrib import admin
from .models import Voter

class VoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'reg_number', 'department', 'voter_code')  # Columns shown in admin list
    search_fields = ('name', 'email', 'reg_number', 'voter_code')  # Search functionality
    list_filter = ('department',)  # Filter voters by department
    ordering = ('id',)  # Order by ID (oldest first)

admin.site.register(Voter, VoterAdmin)

from django.contrib import admin
from .models import Candidate

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'admission_number', 'department', 'course')  # Ensure these fields exist in the model

admin.site.register(Candidate, CandidateAdmin)

from django.contrib import admin
from .models import AdminProfile

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'institution')  # Columns shown in the admin panel
    search_fields = ('user__username', 'city', 'institution')  # Enable searching
    list_filter = ('city', 'institution')  # Enable filtering by city and institution


