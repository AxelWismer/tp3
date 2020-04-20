from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from generador_pseudoaliatorio import generador, tabla
# Create your views here.
# Forms
from .forms import UniformGeneratorForm, ExponentialPoissonGeneratorForm, NormalGeneratorForm, NumberTestForm
import math


# Crea y configura el generador de acuerdo a los datos
def creaate_generator(form):
    if form.cleaned_data['method'] == 'Ge':
        gen = generador.Generador(
            decimals=form.cleaned_data['decimals'],
            random=True
        )
    else:
        if form.cleaned_data['method'] == 'Mi':
            c = form.cleaned_data['c']
        else:
            c = 0
        # Se crea el generador con los datos del formulario
        gen = generador.Generador(
            x=form.cleaned_data['x'],
            c=c,
            a=form.cleaned_data['a'],
            m=form.cleaned_data['m'],
            k=form.cleaned_data['k'],
            g=form.cleaned_data['g'],
            decimals=form.cleaned_data['decimals'],
        )
    return gen

# Muestra los resultados de la tabla
def show_results(request, table):
    template_name = 'number_generator/show_results.html'
    return render(request, template_name, context={'table': table})


class UniformRegister(generic.FormView):
    form_class = UniformGeneratorForm
    template_name = 'number_generator/uniform_form.html'

    def form_valid(self, form):
        # Se crea el generador
        gen = creaate_generator(form)
        # Se generan los datos de acuerdo a la clasificacion
        data = gen.uniforme(
            a=form.cleaned_data['a_min'],
            b=form.cleaned_data['b_max'],
            n=form.cleaned_data['number_amount'],
        )
        # Prueba de chi
        table = tabla.Uniforme(
            datos=data,
            num_intervalos=form.cleaned_data['interval_amount'],
            valor_minimo=form.cleaned_data['min_value'],
            valor_maximo=form.cleaned_data['max_value'],
        )
        # Metodo de prueba de bondad
        test_type = form.cleaned_data['test_type']
        if test_type == 'AUTO':
            table.prueba_de_bondad()
        elif test_type == 'CHI':
            table.chi()
        else:
            table.komolgorov_smirnov()
        table.histogram(path='static/histograma.png')
        return show_results(self.request, table)
