# Register your models here.
from django.contrib import admin
from mainapp.models import MyUser
from django.contrib.auth.admin import UserAdmin



class MyUserAdmin(UserAdmin):
    list_display = ('username', 'is_superuser', 'is_staff', 'is_active', 'color')
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('color',)}),
    )


admin.site.register(MyUser, MyUserAdmin)
