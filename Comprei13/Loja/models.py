from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def create_shopping_list(self, name, description=""):
        """Cria uma lista de compras personalizada."""
        return ShoppingList.objects.create(name=name, description=description, user=self)

    def create_default_shopping_list(self):
        """Cria uma lista de compras padrão caso não exista nenhuma."""
        if not self.shopping_lists.exists():
            shopping_list = ShoppingList.objects.create(
                name="Minha Primeira Lista",
                description="Esta é uma lista de compras padrão.",
                user=self
            )
            shopping_list.add_item(name="Exemplo de Produto 1", purchased=False)
            shopping_list.add_item(name="Exemplo de Produto 2", purchased=False)


class ShoppingList(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Descrição opcional da lista
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shopping_lists")

    def __str__(self):
        return self.name

    def add_item(self, name, purchased=False):
        """Adiciona um item à lista de compras."""
        return Item.objects.create(name=name, purchased=purchased, shopping_list=self)


class Item(models.Model):
    name = models.CharField(max_length=100)
    purchased = models.BooleanField(default=False)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name

    def mark_as_purchased(self):
        """Marca o item como comprado."""
        self.purchased = True
        self.save()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Agora aceita valores nulos

    def __str__(self):
        return self.name



class ShoppingListProduct(models.Model):
    """ Tabela intermediária que relaciona uma lista de compras a vários produtos """
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantidade de produtos na lista
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Preço unitário do produto
    purchased = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['shopping_list', 'product'], name='unique_shopping_list_product')
        ]
    
    def __str__(self):
        return f'{self.shopping_list.name} - {self.product.name}'

from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    preparation = models.TextField(blank=True, null=True)  # Modo de preparo

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Relaciona o Ingrediente a um Produto
    quantity = models.CharField(max_length=50)  # Ex: "2 xícaras", "500ml", etc.

    def __str__(self):
        return f'{self.quantity} de {self.name}'
