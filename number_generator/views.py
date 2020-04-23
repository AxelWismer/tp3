from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from generador_pseudoaliatorio import generador, tabla
# Create your views here.
# Forms
from .forms import UniformGeneratorForm, ExponentialGeneratorForm, NormalGeneratorForm, NumberTestForm,\
    PoissonGeneratorForm
import math


# Muestra los resultados de la tabla
def show_results(request, table):
    template_name = 'number_generator/show_results.html'
    return render(request, template_name, context={'table': table})


# View generica que crea el generador y la tabla
class TableRegister(generic.FormView):
    form_class = None
    template_name = None
    tester = None

    # Crea y configura el generador de acuerdo a los datos
    def creaate_generator(self, form):
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

    def create_table(self, form, data):
        # Creacion de la tabla
        table = self.tester(
            datos=data,
            num_intervalos=form.cleaned_data['interval_amount'],
            valor_minimo=form.cleaned_data['min_value'],
            valor_maximo=form.cleaned_data['max_value'],
            nivel_de_significancia=form.cleaned_data['probability'],
            decimals=form.cleaned_data['decimals'],
        )
        # Metodo de prueba de bondad
        test_type = form.cleaned_data['test_type']
        if test_type == 'AUTO':
            table.prueba_de_bondad()
        elif test_type == 'CHI':
            table.chi()
        else:
            table.komolgorov_smirnov()
        # Crea el grafico del histograma como archivo de imagen
        table.histogram(path='static/histograma.png')
        return table


class UniformRegister(TableRegister):
    form_class = UniformGeneratorForm
    template_name = 'number_generator/uniform_form.html'
    tester = tabla.Uniforme

    def form_valid(self, form):
        # Se crea el generador
        gen = self.creaate_generator(form)
        # Se generan los datos de acuerdo a los parametros
        data = gen.uniforme(
            a=form.cleaned_data['a_min'],
            b=form.cleaned_data['b_max'],
            n=form.cleaned_data['number_amount'],
        )
        # Se genera la tabla con los datos generados
        table = self.create_table(form, data)
        return show_results(self.request, table)


class ExponentialRegister(TableRegister):
    form_class = ExponentialGeneratorForm
    template_name = 'number_generator/exponential_form.html'
    tester = tabla.Exponencial

    def form_valid(self, form):
        # Se crea el generador
        gen = self.creaate_generator(form)
        # Se generan los datos de acuerdo a los parametros
        data = gen.exponencial(
            n=form.cleaned_data['number_amount'],
            lam=form.cleaned_data['lam'],
        )
        # Se genera la tabla con los datos generados
        table = self.create_table(form, data)
        return show_results(self.request, table)


class NormalRegister(TableRegister):
    form_class = NormalGeneratorForm
    template_name = 'number_generator/normal_form.html'
    tester = tabla.Normal

    def form_valid(self, form):
        # Se crea el generador
        gen = self.creaate_generator(form)
        # Se generan los datos de acuerdo a los parametros
        data = gen.normal(
            media=form.cleaned_data['media'],
            desviacion=form.cleaned_data['desviacion'],
            n=form.cleaned_data['number_amount'],
        )
        # Se genera la tabla con los datos generados
        table = self.create_table(form, data)
        return show_results(self.request, table)


class PoissonRegister(TableRegister):
    form_class = PoissonGeneratorForm
    template_name = 'number_generator/poisson_form.html'
    tester = tabla.Poisson

    def form_valid(self, form):
        # Se crea el generador
        gen = self.creaate_generator(form)
        # Se generan los datos de acuerdo a los parametros
        data = gen.poisson(
            n=form.cleaned_data['number_amount'],
            lam=form.cleaned_data['lam'],
        )
        # Se genera la tabla con los datos generados
        table = self.create_table(form, data)
        return show_results(self.request, table)

    def create_table(self, form, data):
        # Creacion de la tabla
        table = self.tester(
            datos=data,
            nivel_de_significancia=form.cleaned_data['probability'],
            decimals=form.cleaned_data['decimals'],
        )
        # Metodo de prueba de bondad
        test_type = form.cleaned_data['test_type']
        if test_type == 'AUTO':
            table.prueba_de_bondad()
        elif test_type == 'CHI':
            table.chi()
        else:
            table.komolgorov_smirnov()
        # Crea el grafico del histograma como archivo de imagen
        table.histogram(path='static/histograma.png')
        return table
