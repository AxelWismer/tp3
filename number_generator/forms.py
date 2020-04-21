from django import forms
from crispy_forms.helper import FormHelper

class GeneratorForm(forms.Form):
    # Datos del generador
    x = forms.IntegerField(label='Semilla "X0"', initial=0, min_value=0)
    c = forms.IntegerField(label='Constante aditiva "c"', initial=0, min_value=0)
    a = forms.IntegerField(label='Constante multiplicativa "a"', initial=0, min_value=0)
    m = forms.IntegerField(label='Modulo "m"', initial=0, min_value=0)
    k = forms.IntegerField(label='Coeficiente "k" que modifica a "a"', initial=0, min_value=0)
    g = forms.IntegerField(label='Coeficiente "g" que modifica a "m"', initial=1, min_value=1)

    METHOD_CHOICES = (('Mi', 'Congruencial Mixto'), ('Mu', 'Congruencial Multiplicativo'), ('Ge', 'Generador del Lenguaje'))
    method = forms.ChoiceField(label='Metodo de calculo', choices=METHOD_CHOICES, initial=METHOD_CHOICES[0])
    decimals = forms.IntegerField(label='Cantidad de decimales', initial=4, min_value=0)

    def __init__(self, *args, **kwargs):
        super(GeneratorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False

class NumberTestForm(forms.Form):
    # Datos de la prueba
    number_amount = forms.IntegerField(label='Cantidad de numeros', initial=1, min_value=1)
    interval_amount = forms.IntegerField(label='Cantidad de intervalos', initial=1, min_value=1)
    TEST_TYPE_CHOICES = (('CHI', 'Chi Cuadrado'), ('KS', 'Kolmogorov-Smirnov'), ('AUTO', 'Automatico'))
    test_type = forms.ChoiceField(label="Tipo de prueba", choices=TEST_TYPE_CHOICES, initial=TEST_TYPE_CHOICES[2])
    # Valor minimos y maximos para la muestra que se consideran para generar los intervalos (opcionales)
    min_value = forms.IntegerField(label="Valor minimo", required=False)
    max_value = forms.IntegerField(label="Valor maximo", required=False)


class UniformGeneratorForm(GeneratorForm, NumberTestForm):
    a_min = forms.FloatField(label='Valor minimo "a"', initial=0)
    b_max = forms.FloatField(label='Valor maximo "b"', initial=1)


class ExponentialPoissonGeneratorForm(GeneratorForm, NumberTestForm):
    lam = forms.FloatField(label='Lambda λ', min_value=0)


class NormalGeneratorForm(GeneratorForm, NumberTestForm):
    media = forms.FloatField(label='Media μ')
    desviacion = forms.IntegerField(label='Desviacion estandar σ')



# class ChiForm(forms.ModelForm):
#     class Meta:
#         model = Data
#         fields = ('number_amount', 'interval_amount')
#
#     def __init__(self, *args, **kwargs):
#         super(ChiForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         # self.helper.form_show_labels = False
#         self.helper.form_tag = False
#
#
# class ChiMixForm(forms.ModelForm):
#     class Meta:
#         model = Data
#         fields = ('x', 'c', 'a', 'm', 'k', 'g', 'method', 'number_amount', 'interval_amount')
#
#     def __init__(self, *args, **kwargs):
#         super(ChiMixForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         # self.helper.form_show_labels = False
#         self.helper.form_tag = False