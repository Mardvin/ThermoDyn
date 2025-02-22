from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from thermo.forms import AddHomeForm
from thermo.function.heat_power import total_heat_energy
from thermo.models import Home

# Create your views here.

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_data_about_home'},
    {'title': "Войти", 'url_name': 'login'},
]

# left_menu = [
#     {'title': 'Результаты расчетов', 'url_name': 'result'},
#     {'title': 'Расчет тепловой мощности', 'url_name': 'heat_power'},
#     {'title': 'Расчет тепловых потерь', 'url_name': 'heat_losses'},
#     {'title': 'Расчет потерь через изоляцию', 'url_name': 'losses_insulation'},
# ]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        # 'left_menu': left_menu,
        'posts': data_db,
    }
    return render(request, 'thermo/index.html', context=data)


def add_data_about_home(request):
    return HttpResponse("Добавление данных о доме")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def about(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        # 'left_menu': left_menu,
    }
    return render(request, 'thermo/about.html', context=data)

# Проект:

def result_calculation(request):
    data = {
        'title': 'Результаты расчетов',
        'menu': menu,
        # 'left_menu': left_menu,
    }
    return render(request, 'thermo/result_claculations.html', context=data)


class HeatPower(CreateView):
    form_class = AddHomeForm
    template_name = 'thermo/result_claculations.html'
    success_url = reverse_lazy('heat_power')

    def get_context_data(self, **kwargs):
        context = super(HeatPower, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        # context['left_menu'] = left_menu
        context['posts'] = Home.objects.all()
        context['total_heat_energy'] = total_heat_energy()
        return context


    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdateHome(UpdateView):
    model = Home
    form_class = AddHomeForm
    template_name = 'thermo/result_claculations.html'
    success_url = reverse_lazy('heat_power')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        # context['left_menu'] = left_menu
        context['posts'] = Home.objects.all()
        return context


class DeleteHome(DeleteView):
    model = Home
    template_name = 'thermo/result_claculations.html'
    success_url = reverse_lazy('heat_power')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        # context['left_menu'] = left_menu
        context['posts'] = Home.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        """Переопределяем post, чтобы сразу удалять без подтверждения"""
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)




class ThermoHome(ListView):
    model = Home
    template_name = 'thermo/index.html'
    context_object_name = 'posts'

    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        # 'left_menu': left_menu,
    }
    # Можно применять этот вариант, он нужен для динамических элементов, а верхний для статических
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

def losses_insulation(request):
    data = {
        'title': 'Расчет потерь через изоляцию',
        'menu': menu,
        # 'left_menu': left_menu,
    }
    return render(request, 'thermo/result_claculations.html', context=data)


# def heat_power(request):
#     form = AddHomeForm()
#     if request.method == 'POST':
#         form = AddHomeForm(request.POST)
#         try:
#             if form.is_valid():
#                 form.save()
#         except Exception as e:
#             form.add_error(None, f'Ошибка добавления поста {e}')
#     post = Home.objects.all()
#     data = {
#         'title': 'Расчет тепловой мощности',
#         'menu': menu,
#         'left_menu': left_menu,
#         'posts': post,
#         'form': form,
#     }
#     return render(request, 'thermo/result_claculations.html', context=data)