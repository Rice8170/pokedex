from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import render,HttpResponse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.db import IntegrityError
from django.views.generic import ListView
from django import forms
from django.views.generic.edit import FormView, CreateView
from .forms import PokemonFrom
from .models import Pokemon, PokemonCategory
import json

# Create your views here.

class Index(ListView):
    model = Pokemon
    template_name = 'index.html'
    queryset = Pokemon.objects.filter(softDelete=0)

 

class Signin(LoginView):
    template_name = "signin.html"
    form_class = AuthenticationForm
    

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.get_success_url()
        else:
            return super(Signin,self).dispatch(request, *args, **kwargs)
    
    def get_redirect_url(self) -> str:
        
        return reverse_lazy('pokemonList')
    
    def get_form(self, form_class=None):
        form = super(Signin, self).get_form()

        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingresa usuario'})
        form.fields['password'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Ingresa contraseña'})
    
        form.fields['username'].label = 'Usuario'
        form.fields['password'].label = 'Contraseña'
        return form
    
    def form_valid(self, form):
        print(self.request.get_full_path)
        
        user = authenticate(self.request,username=self.request.POST['username'],password=self.request.POST['password'])
        
        login(self.request,user)
        return super().form_valid(form)
    


class Signup(CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.get_success_url()
        else:
            return super(Signup,self).dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super(Signup, self).get_form()

        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingresa usuario'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Ingresa contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confrima contraseña'})

        form.fields['username'].label = 'Usuario'
        form.fields['password1'].label = 'Contraseña'
        form.fields['password2'].label = 'Confirma Contrasña'
        return form
        

    def form_valid(self, form):
        print("Form Valido")
        self.object = form.save()
        print(self.object)
        login(self.request, self.object)
        return super(Signup,self).form_valid(form)
    

@login_required
def signout(request):
    logout(request)
    return redirect('index')

@login_required
def pokemonList(request):
    pokemons = Pokemon.objects.filter(user=request.user, softDelete=0)
    
    return render(request,'pokemonList.html',{
        'pokemons':pokemons,  
    })


class PokemonCreate(LoginRequiredMixin, CreateView):
    template_name = "pokemonCreate.html"
    form_class = PokemonFrom
    success_url = reverse_lazy('pokemonList')
    login_url = "/signin/"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        print("Form Valido")
        print(self.request.user)
        form.instance.user = self.request.user
        self.object = form.save()
        
        self.object.category.set(self.request.POST.getlist('category'))
        print(self.object)
        messages.success(self.request, "Pokemon capturado")
        
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)

        return super(PokemonCreate,self).form_invalid(form)    
    

def pokemonGet(request):
    pokemons = Pokemon.objects.filter(user=request.user, softDelete=0)
    return render(request,'pokemonList.html',{
        'pokemons':pokemons
    })

@login_required
def pokemonEdit(request, pokemonId):
    
    try:
       
        pokemon = Pokemon.objects.filter(user=request.user, softDelete=0).prefetch_related('category').get(id=pokemonId)
        
        if request.method == 'GET':
            form = PokemonFrom(instance=pokemon)
            return render(request, 'pokemonEdit.html',{'form':form})
        else:
            
            form = PokemonFrom(request.POST, request.FILES, instance=pokemon)
           
            if form.has_changed:
                
                print('forr with changes')
                
                    # if fieldName == 'category':
                    #     pokemon[fieldName].set(request.POST.getlist(fieldName))

                form.save()

                pokemon.save(force_update=True)
                messages.add_message(request, level=messages.SUCCESS, message="Pokemon actualizado")
                return redirect('pokemonList')
           
            postCaregories = request.POST.getlist('category')
            pokemon.category.set(postCaregories)  
         
            return redirect('pokemonDetail', pokemonId)
    except ObjectDoesNotExist:
        messages.add_message(request,level=messages.ERROR, message="Pokemon no encontrado")
        return redirect('pokemonDetail', pokemonId)

@login_required
def pokemonDelete(request, pokemonId):

    try:
        pokemon = Pokemon.objects.filter(user=request.user, softDelete=0).get(id=pokemonId)
        pokemon.softDelete = 1
        pokemon.save()
        # messages.add_message(request,level=messages.SUCCESS, message="Pokemin eliminado")
        
        messages.success(request,"El pokemon fue enviado con el doctor Oak")
        return redirect('pokemonList')
    except ObjectDoesNotExist:
        messages.add_message(request,level=messages.ERROR, message="El pokemon no se puede eliminar")
        return redirect('pokemonDetail', pokemonId)


@login_required
def pokemonDetail(request, pokemonId):
    try:
        pokemon = Pokemon.objects.filter(user=request.user,softDelete=0).get(id=pokemonId)
        form = PokemonFrom(instance=pokemon)
        return render(request, 'pokemonDetail.html',{
            'pokemon': pokemon,
            'form':form
        })
    except ObjectDoesNotExist:
        messages.add_message(request, level=messages.ERROR, message="Pokemon no encontrado")
        return redirect('pokemonList')