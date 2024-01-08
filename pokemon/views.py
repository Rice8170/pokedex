from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q

from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponse as HttpResponse
from django.shortcuts import render,HttpResponse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.core import serializers
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.generic import ListView
from django.utils import timezone 
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView,SingleObjectMixin
from django import forms
from django.views.generic.edit import FormView, CreateView, UpdateView,DeleteView
from datetime import datetime
from .forms import PokemonFrom
from .models import Pokemon, PokemonCategory
import json

# Create your views here.

class Index(ListView):
    model = Pokemon
    template_name = 'index.html'

    def get_queryset(self):
        print( type(self.request.user))
        if self.request.user.is_anonymous:
            return Pokemon.objects.filter(softDelete=0)
        else:
            return Pokemon.objects.filter(softDelete=0, user=self.request.user)


class Signin(LoginView):
    template_name = "signin.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
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
    success_url = reverse_lazy('signin')

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
        user = form.save()
        
        
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

class PokemonList(LoginRequiredMixin,TemplateView):
    template_name = 'pokemonList.html'

class PokemonGet(LoginRequiredMixin,ListView):
    model = Pokemon

    def get_queryset(self, lenght, start, search, columnName, dir):

        querySet = {
            'recordsTotal': None,
            'recordsFiltered' : None
        }
        result = self.model.objects.filter(user=self.request.user,softDelete=0).prefetch_related('category').all()

        querySet['recordsTotal'] = result.count()
        print(search)
        if search:
            print("Haciendo Filtros")
            resultwithfilters = result.filter(
                Q(name__contains=search)|
                Q( height__contains=search)|
                Q(weight__contains=search)|
                Q(dateCapture__contains=search)
            )
        else:
            print("Sin filtros") 
            resultwithfilters = result

        if dir == "asc":
            resultwithfilters = resultwithfilters.order_by(columnName)
        else:
            resultwithfilters = resultwithfilters.order_by('-{}'.format(columnName))   
        
        querySet['recordsFiltered'] = resultwithfilters.count()
        
        resultwithfilters = resultwithfilters[int(start):int(lenght)+int(start)]

       
       
        pokemons = []

        for pokemon in resultwithfilters:

            pokemons.append({
                'id':pokemon.id,
                'name':pokemon.name,
                'category': [],
                'weight':pokemon.weight,
                'height':pokemon.height,
                'color':pokemon.get_color_display(),
                'dateCapture': pokemon.dateCapture.strftime('%A/%m/%Y %I:%M %p')
            })

            for category in pokemon.category.all():
                pokemons[-1]['category'].append(category.name)
                

        querySet['data'] = pokemons
       
        return querySet
    
    

    def post(self, request, *args, **kwargs):
        
        draw = request.POST.get('draw')
        start = request.POST.get('start')
        length = request.POST.get('length')
        search = request.POST.get('search[value]')
        order = request.POST.get('order[0][column]')
        columnName = request.POST.get('columns[{}][data]'.format(order))
        dir = request.POST.get('order[0][dir]')

        
        querySet  = self.get_queryset(lenght=length, start=start, search=search, columnName=columnName, dir=dir)

        print(querySet)

        return JsonResponse({
            'draw':draw,
            'recordsTotal':querySet['recordsTotal'],
            'recordsFiltered':querySet['recordsFiltered'],
            'data': querySet['data']
        })


    
    

class PokemonCreate(LoginRequiredMixin, CreateView):
    template_name = "pokemonCreate.html"
    form_class = PokemonFrom
    success_url = reverse_lazy('pokemonList')
   
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

class PokemonDetail(DetailView):
    model = Pokemon
    template_name = "pokemonDetail.html"
    pk_url_kwarg = "pokemonId"

    def get_context_data(self, **kwargs):

        pk = self.kwargs.get(self.pk_url_kwarg)
        pokemon = self.model.objects.filter(user=self.request.user, softDelete=0).get(id=pk)
        print(pokemon)
        form = PokemonFrom(instance=pokemon)
        context = super(PokemonDetail, self).get_context_data(**kwargs)
        context['form'] = form
        return context

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, softDelete=0)
    

class PokemonEdit(LoginRequiredMixin, UpdateView):
    model = Pokemon
    form_class = PokemonFrom
    template_name = "pokemonDetail.html"
    
    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        messages.success(self.request, "Pokemon actualizado")
        return reverse_lazy("pokemonDetail", args=[pk])
    
    
    # def form_valid(self, form):

    #     self.object = form.save()
    #     self.object.category.set(self.request.POST.getlist('category'))
    #     return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
       

class PokemonDelete(LoginRequiredMixin, DeleteView):
    model = Pokemon
    template_name = ""
    
    def get_success_url(self):
        return reverse_lazy("pokemonList")

    def post(self, request, pk , *args, **kwargs):
        object = Pokemon.objects.get(id=pk)
        object.softDelete = 1
        object.save()

        messages.success(self.request,"El pokemon fue enviado con el doctor Oak")

        return redirect(self.get_success_url())


