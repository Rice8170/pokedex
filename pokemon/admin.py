from django.contrib import admin
from .models import Pokemon, PokemonCategory


class PokemonAdmin(admin.ModelAdmin):
    readonly_fields = ('dateCapture',)

# Register your models here.
admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonCategory)
