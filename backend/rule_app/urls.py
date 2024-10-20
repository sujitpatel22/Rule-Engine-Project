from django.urls import path
from . import views

urlpatterns = [
    path('create_rule/', views.create_rule, name='create_rule'),
    path('combine_rules/', views.combine_rules, name='combine_rules'),
    path('evaluate_rule/', views.evaluate_rule, name='evaluate_rule'),
]
