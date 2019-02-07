from django.shortcuts import render
from django.urls import reverse_lazy
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (TemplateView,
                                  DetailView,
                                  ListView,
                                  CreateView)
from .models import ShopSearch, Product

from .scraping_emag import scrape_emag
from .scraping_Olx import scrape_olx
from .scraping_Bazar import scrape_bazar


def change_placeholders(form):
    '''Function that takes a form and changes its placeholders.'''

    form.fields['searched_product'].widget = forms.TextInput(attrs={'placeholder': 'Търсен продукт'})
    form.fields['minimum_price'].widget = forms.NumberInput(attrs={'placeholder': 'Минимална цена'})
    form.fields['maximum_price'].widget = forms.NumberInput(attrs={'placeholder': 'Максимална цена'})

    return form

class CustomCreateView(CreateView):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)

        form = change_placeholders(form)

        return form


class ResultsView(ListView):
    model = Product
    context_object_name = "search_results"
    template_name = "shops/results.html"


class EmagView(CustomCreateView):
    template_name = "shops/emag.html"
    model = ShopSearch
    success_url = reverse_lazy("shops:results")

    fields = ["searched_product", "minimum_price", "maximum_price"]


    def form_valid(self, form):
        # Deleting all previous Product objects
        Product.objects.all().delete()
        ShopSearch.objects.all().delete()

        super().form_valid(form)

        words_list = self.object.searched_product.split()
        # print(words_list)
        # print(self.object.minimum_price, ":", self.object.maximum_price)
        price_range = (int(self.object.minimum_price), int(self.object.maximum_price))
        suitable_items = scrape_emag(words_list, price_range)

        # print(suitable_items)

        for item, values in suitable_items.items():
            product = Product.objects.create(name=item, 
                                             price=values[0], 
                                             shop_search=form.instance, 
                                             product_url=values[1], 
                                             product_img=values[2])
        try:
                return super().form_valid(form)
        except:
            print("ERROR")
            return super().form_invalid(form)


    
class OlxView(CustomCreateView):
    template_name = "shops/olx.html"
    model = ShopSearch

    success_url = reverse_lazy("shops:results")

    fields = ["searched_product", "minimum_price", "maximum_price"]


    def form_valid(self, form):
        # Deleting all previous Product objects
        Product.objects.all().delete()
        ShopSearch.objects.all().delete()

        super().form_valid(form)

        words_list = self.object.searched_product.split()
        # print(words_list)
        # print(self.object.minimum_price, ":", self.object.maximum_price)
        price_range = (int(self.object.minimum_price), int(self.object.maximum_price))
        suitable_items = scrape_olx(words_list, price_range)

        # print(suitable_items)

        for item, values in suitable_items.items():
            product = Product.objects.create(name=item, 
                                             price=values[0], 
                                             shop_search=form.instance, 
                                             product_url=values[1], 
                                             product_img=values[2])
        try:
                return super().form_valid(form)
        except:
            print("ERROR")
            return super().form_invalid(form)

class BazarView(CustomCreateView):
    template_name = "shops/bazar.html"
    model = ShopSearch

    success_url = reverse_lazy("shops:results")

    fields = ["searched_product", "minimum_price", "maximum_price"]


    def form_valid(self, form):
        # Deleting all previous Product objects
        Product.objects.all().delete()
        ShopSearch.objects.all().delete()

        super().form_valid(form)

        words_list = self.object.searched_product.split()
        # print(words_list)
        # print(self.object.minimum_price, ":", self.object.maximum_price)
        price_range = (int(self.object.minimum_price), int(self.object.maximum_price))
        suitable_items = scrape_bazar(words_list, price_range)

        # print(suitable_items)

        for item, values in suitable_items.items():
            product = Product.objects.create(name=item, 
                                             price=values[0], 
                                             shop_search=form.instance, 
                                             product_url=values[1], 
                                             product_img=values[2])
        try:
                return super().form_valid(form)
        except:
            print("ERROR")
            return super().form_invalid(form)