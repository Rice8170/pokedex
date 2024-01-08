
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Pokemon, PokemonCategory

class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Ingresa contraseña'
    }))
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Repite la contraseña'
    }))

    class Meta:
        model = User
        fields = [
            'username',
        ]
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingresa Usuario'}),
           
        }

        lables={
            'username': 'Usuario',
        }
    

class AuthFrom(AuthenticationForm):
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Ingresa usuario'
    }))

    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Ingresa contraseña'
    }))

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
        pokemon = Pokemon.objects.filter(name=name)

        # if pokemon.exists():
        #     print(pokemon.exists())
        #     raise ValidationError('Pokemon ya ha sido capturado')

        if not (name and name.isalpha()) :
            raise forms.ValidationError('El nombre debe ser alfabetico')
        return name
    


class PokemonCaregoryFrom(forms.ModelForm):
    class Meta:
        model = PokemonCategory
        fields = [
            'name'
        ]