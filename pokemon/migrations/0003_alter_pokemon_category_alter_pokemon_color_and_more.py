# Generated by Django 5.0 on 2024-01-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0002_alter_pokemon_pokemonimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='category',
            field=models.ManyToManyField(to='pokemon.pokemoncategory', verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='color',
            field=models.CharField(choices=[('1', 'Rojo'), ('2', 'Amarillo'), ('3', 'Azul'), ('4', 'Naranja'), ('5', 'Verde'), ('6', 'Morado')], max_length=1, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='dateCapture',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de captura'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='height',
            field=models.FloatField(verbose_name='Altura'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='pokemonImage',
            field=models.ImageField(blank=True, null=True, upload_to='PokemonImages', verbose_name='Imagén'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='weight',
            field=models.FloatField(verbose_name='Peso'),
        ),
    ]
