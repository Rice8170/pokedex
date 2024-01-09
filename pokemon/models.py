from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class PokemonCategory(models.Model):
    name=models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edicion")

    class Meta:
        verbose_name = "Categoria Pokemon"
        verbose_name_plural = "Categorias Pokemon"
    
    def __str__(self):
        return self.name


class Pokemon(models.Model):

    name = models.CharField(max_length=100,blank=False, verbose_name="Nombre")
    category = models.ManyToManyField(PokemonCategory, verbose_name="Tipo")
    weight = models.FloatField(verbose_name="Peso")
    height = models.FloatField(verbose_name="Altura")

    COLORS = (
        ('1','Rojo'),
        ('2','Amarillo'),
        ('3','Azul'),
        ('4','Naranja'),
        ('5','Verde'),
        ('6','Morado')
    )
    color = models.CharField(max_length=1, choices=COLORS, verbose_name="Color")
    dateCapture = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de captura")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    softDelete = models.BooleanField(default=True)
    pokemonImage = models.ImageField(upload_to="PokemonImages",null=True, blank=True, verbose_name="Imagén")

    
       
    def __str__(self):
        return self.name #+ '- by ' + self.user.username

