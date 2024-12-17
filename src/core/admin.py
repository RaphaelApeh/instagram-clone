from django.contrib import admin
from django.utils.html import format_html

from .models import Profile,Post,Comment,PasswordReset

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','active']

class CommentAdmin(admin.TabularInline):
    model = Comment
    can_delete = True

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentAdmin]
    list_display = ['name','user','display_image',]
    fields = ['user','name','image','display_image','likes','slug','favourite','active','timestamp']
    readonly_fields = ['timestamp','display_image',]

    def display_image(self,obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="500" />')
        else:
            return 'No Image Found'
    display_image.short_description = 'Image'
admin.site.register(Post,PostAdmin)
admin.site.register(PasswordReset)
admin.site.register(Profile,ProfileAdmin)