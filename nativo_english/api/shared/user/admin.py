from django.contrib import admin
from .models import User  # Importing Custome User model

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'date_joined')  # Adjust fields as needed
    search_fields = ('username', 'email')  # Enable searching by these fields