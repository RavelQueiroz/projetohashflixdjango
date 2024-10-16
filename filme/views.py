from audioop import reverse
from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CriarContaForm, FormHomepage

# Create your views here.
#def homepage(request):
    #return render(request, "homepage.html")

class HomePage(FormView):
    template_name = 'homepage.html'

    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #usuario logado - redirecionar home filmes
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) #redireciona para a homepage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)

        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

#def homefilme(request):
    #context = {}
    #lista_filmes = Filme.objects.all()
    #context['lista_filmes'] = lista_filmes
    #return render(request, "homefilmes.html", context)

class HomeFilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme
    #passa como object_list

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme

    #object 1 item do nosso modelo
    def get(self, request, *args, **kwargs):
        #descobrir qual filme ele ta acessando
        filme = self.get_object()
        # somar 1 nas visualizaçoes daquele filme
        filme.visualizacoes += 1
        #salvar
        filme.save()

        #adicionando o filme nos já assistidos
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) #redireciona o usuário para a ulr final

    def get_context_data(self, **kwargs):
        #SEMPRE QUE FOR MANDAR MAIS UMA LISTA PRO HTML, PRECISAMOS INDICAR A SUPER AQUI
        context = super(Detalhesfilme, self).get_context_data(**kwargs)

        # filtrar a minha tabela filmes pegando os filmes cuja categoria é igual a categoria do filme da página (object)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados

        return context

class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:

            object_list = Filme.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    #quais campos vai poder editar
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')


class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')