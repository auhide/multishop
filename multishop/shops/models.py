from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError



class ShopSearch(models.Model):
    searched_product = models.CharField(max_length=150)
    minimum_price = models.PositiveIntegerField(default="Minimum", 
                                           validators=[MinValueValidator(1)])
    maximum_price = models.PositiveIntegerField(default="Maximum", 
                                           validators=[MinValueValidator(1)])
    def __str__(self):
        return self.searched_product

    def clean(self):

        if self.minimum_price >= self.maximum_price:
            raise ValidationError("The Maximum price has to be more than the Minimum!")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    shop_search = models.ForeignKey(ShopSearch, on_delete=models.CASCADE)
    product_url = models.URLField(max_length=250, default="#")
    product_img = models.URLField(max_length=250, default="#")

    class Meta:
        '''Ordering each product by its price (lower to higher)'''
        ordering = ["price"]

    def __str__(self):
        return self.name + ": " + str(self.price)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)