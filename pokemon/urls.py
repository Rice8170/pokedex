
from django.urls import path
from . import views
from .views import PokemonCreate, PokemonEdit, PokemonDelete, PokemonDetail, PokemonList, PokemonGet

urlpatterns = [    
    path('list/',PokemonList.as_view(), name='pokemonList'),
    path('create/',PokemonCreate.as_view(), name='pokemonCreate'),
    path('get/',PokemonGet.as_view(), name='pokemonGet'),
    path('deteail/<int:pokemonId>',PokemonDetail.as_view(), name='pokemonDetail'),
    path('edit/<int:pk>',PokemonEdit.as_view(), name='pokemonEdit'),
    path('delete/<int:pk>',PokemonDelete.as_view(), name='pokemonDelete'),
]
