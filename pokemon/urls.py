
from django.urls import path
from . import views
from .views import PokemonCreate

urlpatterns = [    
    path('list/',views.pokemonList, name='pokemonList'),
    path('create/',PokemonCreate.as_view(), name='pokemonCreate'),
    path('get/',views.pokemonGet, name='pokemonGet'),
    path('deteail/<int:pokemonId>',views.pokemonDetail, name='pokemonDetail'),
    path('edit/<int:pokemonId>',views.pokemonEdit, name='pokemonEdit'),
    path('delete/<int:pokemonId>',views.pokemonDelete, name='pokemonDelete'),
]
