from django.contrib import admin
from .models import *

class ChoiceInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Choice
    extra = 1


admin.site.register(BlogPost)
admin.site.register(Profile)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "pub_date", "active", "created_at"]
    search_fields = ["title", "about", "owner__username"]
    list_filter = ["active", 'created_at', 'pub_date']
    date_hierarchy = "pub_date"
    inlines = [ChoiceInline]


# Register your models here.
