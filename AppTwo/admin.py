from django.contrib import admin

# Register your models here.
from django.contrib import admin
from AppTwo.models import UsersModel, UserProfileInfo

admin.site.register(UserProfileInfo)

@admin.register(UsersModel)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'last_name')
