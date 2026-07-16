from django.contrib import admin
from .models import Repository

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "language",
        "stars"
    )

    search_fields = (
        "name",
        "full_name",
    )
