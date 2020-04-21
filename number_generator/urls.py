from django.urls import path
from .views import UniformRegister, ExponentialRegister

app_name = 'number_generator'

urlpatterns = [
    path('generate/uniform', UniformRegister.as_view(), name='generate_uniform'),
    path('generate/exponential', ExponentialRegister.as_view(), name='generate_exponential'),

]