"""User admin classes"""
# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# models
from users.models import *
from students.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin"""

    list_display = ('user', 'role', 'institution')
    list_editable = ('role', 'institution')
    search_fields = (
        'user__email',
        'user__first_name'
    )

    list_filter = (
        'created',
        'modified',
        'user__is_active',
    )

    fieldsets = (
        ('Profile', {
            'fields': (
                ('user', 'role'),
            )
        }),
        ('Extra Info', {
            'fields': (
                ('institution'),
            )
        }),
        ('Metadata', {
            'fields': (
                ('created', 'modified'),

            )
        }),
    )

    readonly_fields = ('created', 'modified')


class ProfileInLine(admin.StackedInline):
    """Profile inline admin for users"""

    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Student)
