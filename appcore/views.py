from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView


class MainPageView(TemplateView):
    template_name = 'layout.html'
