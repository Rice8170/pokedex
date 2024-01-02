from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import render,HttpResponse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
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

 

# class Signup(FormView):
#     template_name = "signup.html"
#     form_class = UserCreationForm
#     success_url = reverse_lazy('pokemonList')

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return self.get_success_url()
#         else:
#             return super(Signup,self).dispatch(request, *args, **kwargs)
    

#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return super(Signup, self).form_valid(form)
    
class Signup(CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('pokemonList')

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
        login(self.request, form.get_user())
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        return render(self.request,self.template_name,context)
    

# def signup(request):
#     if request.method == 'GET':
#         return render(request, 'signup.html',{
#             'form': UserCreationForm
#         })
#     else:
#         if request.POST['password1'] == request.POST['password2']:
#             try:
#                 user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
#                 user.save()
#                 login(request,user)
#                 return redirect('pokemonList')
#             except IntegrityError:
#                 return render(request, 'signup.html',{
#                 'form': UserCreationForm,
#                 'error':{
#                     'title': 'Error de registro',
#                     'text': 'El usuario ya existe',
#                     'icon': 'error',
#                     'confirmButtonText': 'OK'
#                 }
#             })
#         else:
#             return render(request, 'signup.html',{
#                 'form': UserCreationForm,
#                 'error': 'La contraseña no coincide'
#             })

def signin(request):
    if request.method == 'GET':

        return render(request,'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request,'signin.html',{
                'error':{
                    'title': 'Error de autenticación',
                    'text': 'Usuario o contraseña incorrectos',
                    'icon': 'error',
                    'confirmButtonText': 'OK'
                }
            })
        else:
            login(request, user)
            return redirect('pokemonList')


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

@login_required
def pokemonCreate(request):
    if request.method == 'GET':
        return render(request,'pokemonCreate.html',{
            'form':PokemonFrom
        })
    else:
        # try:
        post = request.POST
        pokemon = Pokemon(user=request.user)
        
        form = PokemonFrom(post,request.FILES, instance=pokemon)
        
        if form.is_valid():
            pokemon = form.save(commit=False)
            pokemon.full_clean()
            pokemon.save()
            pokemon.category.set(post.getlist('category'))            
            
            return render(request,'pokemonCreate.html',{
                'form':PokemonFrom,
                "message":{
                    "title":"Nuvo pokemon consegido",
                    "text":"{} ha sido agregado a la colección". format(pokemon.name),
                    "icon":"success",
                    "confirmButtonText":"Ok"
                }
            })
        else:
            if "__all__" in form.errors:
                print(True)
                return render(request,'pokemonCreate.html',{
                    'form': PokemonFrom(),
                    "message":{
                        "title":"Pokemon no capturado",
                        "text":"Ya tienes el pokemon en tu coleccion" ,
                        "icon":"error",
                        "confirmButtonText":"Ok"
                    }
                })

            return render(request,'pokemonCreate.html',{
                'form':form
            })
        # except ValidationError as e:
        #     print('exepcion')
        #     return render(request,'pokemonCreate.html',{
        #         'form':form,
        #         'error':e.message_dict
        #     })
    
        
    

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