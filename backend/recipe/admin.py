from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time', 'total_favorites')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author__username', 'author__email')

    def total_favorites(self, obj):
        return obj.favorited_by.count()
    total_favorites.short_description = 'Total Favorites'
