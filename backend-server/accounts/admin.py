from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # these fields tell Django Admin what to show
    list_display = ('email', 'username', 'is_doctor', 'is_patient', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_doctor', 'is_patient')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_doctor', 'is_patient')}),
    )