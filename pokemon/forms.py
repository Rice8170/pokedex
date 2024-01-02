
from django import forms
from .models import Pokemon, PokemonCategory
from django.core.exceptions import ValidationError

class PokemonFrom(forms.ModelForm):
    category:forms.ModelMultipleChoiceField(queryset=PokemonCategory.objects.all())
    class Meta:
        model = Pokemon
        fields = [
            'name',
            'category',
            'weight',
            'height',
            'color',
            'pokemonImage'
        ]

        widgets={
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del pokemon'}),
            'category':forms.SelectMultiple(attrs={'class':'form-select'}),
            'color':forms.Select(attrs={'class':'form-select'}),
            'weight':forms.NumberInput(attrs={'class':'form-control'}),
            'height':forms.NumberInput(attrs={'class':'form-control'}),
            'pokemonImage': forms.ClearableFileInput(attrs={'class':'form-control', 'placeholder':'URL de imagen'}),
        }

    

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not (name and name.isalpha()) :
            raise forms.ValidationError('El nombre debe ser alfabetico')
        return name
    
 
    
        


class PokemonCaregoryFrom(forms.ModelForm):
    class Meta:
        model = PokemonCategory
        fields = [
            'name'
        ]