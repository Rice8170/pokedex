
from django.urls import path
from . import views
from .views import PokemonCreate, PokemonEdit, PokemonDelete, PokemonDetail

urlpatterns = [    
    path('list/',views.pokemonList, name='pokemonList'),
    path('create/',PokemonCreate.as_view(), name='pokemonCreate'),
    path('get/',views.pokemonGet, name='pokemonGet'),
    path('deteail/<int:pokemonId>',PokemonDetail.as_view(), name='pokemonDetail'),
    path('edit/<int:pk>',PokemonEdit.as_view(), name='pokemonEdit'),
    path('delete/<int:pk>',PokemonDelete.as_view(), name='pokemonDelete'),
]
