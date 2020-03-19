from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import User, Prompt, Video

def send_welcome_email(modeladmin, request, queryset):
    for element in queryset:
        element.send_welcome_email()
send_welcome_email.short_description = "Send welcome email"

class CoreUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('display_name', 'email')}),
        (_('General information'), {'fields': ('verified_email', 'email_opt_out', 'location', 'age')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    actions = [send_welcome_email]
    list_display = ('username', 'email', 'display_name', 'verified_email', 'email_opt_out', 'location', 'age')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'verified_email', 'email_opt_out')
    search_fields = ('username', 'display_name', 'email', 'location')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, CoreUserAdmin)

class PromptAdmin(admin.ModelAdmin):
    list_display = ('day', 'text')
    search_fields = ('text',)
    ordering = ('-day',)

admin.site.register(Prompt, PromptAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ("created", "title", "user", "prompt")
    search_fields = ('title',)
    ordering = ("-created",)

admin.site.register(Video, VideoAdmin)
