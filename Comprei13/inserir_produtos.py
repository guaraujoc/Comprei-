import os
import django

# Configurar o Django para reconhecer o ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Comprei.settings')
django.setup()

from Loja.models import Product  # Substitua "app" pelo nome do seu aplicativo

# Lista de 50 produtos comuns de mercado com variações de marcas
produtos = [
    {'name': 'Arroz', 'description': 'Pacote de 1kg de arroz branco marca Tio João', 'price': 5.50},
    {'name': 'Arroz', 'description': 'Pacote de 1kg de arroz branco marca Prato Fino', 'price': 5.30},
    {'name': 'Feijão', 'description': 'Pacote de 1kg de feijão carioca marca Kicaldo', 'price': 8.00},
    {'name': 'Feijão', 'description': 'Pacote de 1kg de feijão carioca marca Caldo Nobre', 'price': 8.50},
    {'name': 'Açúcar', 'description': 'Pacote de 1kg de açúcar refinado marca União', 'price': 3.50},
    {'name': 'Açúcar', 'description': 'Pacote de 1kg de açúcar refinado marca Doçurinha', 'price': 3.20},
    {'name': 'Macarrão', 'description': 'Pacote de 500g de macarrão espaguete marca Galo', 'price': 4.50},
    {'name': 'Macarrão', 'description': 'Pacote de 500g de macarrão espaguete marca Renata', 'price': 4.70},
    {'name': 'Óleo de Soja', 'description': 'Garrafa de 900ml de óleo de soja marca Soya', 'price': 7.00},
    {'name': 'Óleo de Soja', 'description': 'Garrafa de 900ml de óleo de soja marca Liza', 'price': 6.80},
    {'name': 'Leite Integral', 'description': 'Caixa de 1L de leite integral marca Parmalat', 'price': 3.90},
    {'name': 'Leite Integral', 'description': 'Caixa de 1L de leite integral marca Italac', 'price': 3.80},
    {'name': 'Café', 'description': 'Pacote de 500g de café torrado e moído marca Pilão', 'price': 10.50},
    {'name': 'Café', 'description': 'Pacote de 500g de café torrado e moído marca Melitta', 'price': 11.20},
    {'name': 'Ovos', 'description': 'Cartela com 12 ovos brancos marca Ovos do Campo', 'price': 7.50},
    {'name': 'Ovos', 'description': 'Cartela com 30 ovos brancos marca Ovos Select', 'price': 15.50},
    {'name': 'Carne Bovina', 'description': '1kg de carne bovina (patinho) marca Friboi', 'price': 32.90},
    {'name': 'Carne Bovina', 'description': '1kg de carne bovina (alcatra) marca Friboi', 'price': 39.90},
    {'name': 'Frango', 'description': '1kg de peito de frango marca Sadia', 'price': 12.50},
    {'name': 'Frango', 'description': '1kg de peito de frango marca Perdigão', 'price': 12.30},
    {'name': 'Linguiça', 'description': '500g de linguiça toscana marca Perdigão', 'price': 15.50},
    {'name': 'Linguiça', 'description': '500g de linguiça toscana marca Seara', 'price': 16.00},
    {'name': 'Tomate', 'description': '1kg de tomate comum variedade Carmen', 'price': 6.50},
    {'name': 'Tomate', 'description': '1kg de tomate italiano variedade Debora', 'price': 7.20},
    {'name': 'Banana', 'description': '1kg de banana prata', 'price': 5.20},
    {'name': 'Banana', 'description': '1kg de banana nanica', 'price': 4.90},
    {'name': 'Chocolate', 'description': 'Barra de 170g de chocolate ao leite marca Nestlé', 'price': 7.50},
    {'name': 'Chocolate', 'description': 'Barra de 170g de chocolate ao leite marca Lacta', 'price': 7.80},
    {'name': 'Refrigerante', 'description': 'Garrafa de 2L de refrigerante de cola marca Coca-Cola', 'price': 6.90},
    {'name': 'Refrigerante', 'description': 'Garrafa de 2L de refrigerante de cola marca Pepsi', 'price': 6.70},
    {'name': 'Água Mineral', 'description': 'Garrafa de 1.5L de água mineral marca Crystal', 'price': 2.50},
    {'name': 'Água Mineral', 'description': 'Garrafa de 1.5L de água mineral marca Bonafont', 'price': 2.30},
    {'name': 'Cerveja', 'description': 'Garrafa de 600ml de cerveja pilsner marca Brahma', 'price': 4.80},
    {'name': 'Cerveja', 'description': 'Garrafa de 600ml de cerveja pilsner marca Skol', 'price': 4.70},
    {'name': 'Leite Condensado', 'description': 'Lata de 395g de leite condensado marca Nestlé', 'price': 5.70},
    {'name': 'Leite Condensado', 'description': 'Lata de 395g de leite condensado marca Italac', 'price': 5.40},
    {'name': 'Sabonete', 'description': 'Unidade de 90g de sabonete perfumado marca Dove', 'price': 1.50},
    {'name': 'Sabonete', 'description': 'Unidade de 90g de sabonete perfumado marca Lux', 'price': 1.40},
    {'name': 'Shampoo', 'description': 'Frasco de 350ml de shampoo marca Pantene', 'price': 9.50},
    {'name': 'Shampoo', 'description': 'Frasco de 350ml de shampoo marca Seda', 'price': 8.90},
    {'name': 'Condicionador', 'description': 'Frasco de 350ml de condicionador marca Pantene', 'price': 10.50},
    {'name': 'Condicionador', 'description': 'Frasco de 350ml de condicionador marca Dove', 'price': 10.00},
    {'name': 'Detergente', 'description': 'Frasco de 500ml de detergente marca Ypê', 'price': 2.50},
    {'name': 'Detergente', 'description': 'Frasco de 500ml de detergente marca Minuano', 'price': 2.30}
]
# Inserir os produtos no banco de dados
for produto in produtos:
    Product.objects.create(**produto)
    print(f"Produto {produto['name']} criado com sucesso!")
