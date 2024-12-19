from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import ShoppingList, Item, User, Product, ShoppingListProduct, Recipe, Ingredient
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
import logging
import json
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def csrf(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})
@csrf_exempt
def cadastro(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            email = data.get('email')
            senha = data.get('password')
            confirmacao_senha = data.get('confirm_password')

            # Verificar se as senhas coincidem
            if senha != confirmacao_senha:
                return JsonResponse({'success': False, 'message': 'As senhas não coincidem.'}, status=400)
            
            # Verificar se o usuário já existe
            usuario_existente = User.objects.filter(name=nome).exists()
            email_existente = User.objects.filter(email=email).exists()
            
            if usuario_existente:
                return JsonResponse({'success': False, 'message': 'Nome de usuário já está cadastrado'}, status=400)
            
            if email_existente:
                return JsonResponse({'success': False, 'message': 'Email já está cadastrado'}, status=400)
            
            # Criar o novo usuário
            Usuario = User(name=nome, email=email, password=senha)
            Usuario.save()
            Usuario.create_default_shopping_list()
            
            return JsonResponse({'success': True, 'message': 'Cadastro realizado com sucesso!'}, status=201)
        except Exception as e:
            return JsonResponse({"success": False, "message": "Erro no servidor!", "error": str(e)}, status=500)
    
    return JsonResponse({"success": False, "message": "Método não permitido!"}, status=405)

def tela_inicial(request):
    return render(request,'exemplosite.html')
    #return HttpResponse('Estou no inserir')

@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'tela_login.html')
    
    elif request.method == "POST":
        # Pegando os dados do formulário
        data = json.loads(request.body)
        nome = data.get('nome')
        senha = data.get('password')


        try:
            # Verificar se o usuário existe no banco de dados
            usuario = User.objects.get(name=nome)
            request.session['user_id'] = usuario.id

            if usuario.password == senha:
                # Usuário autenticado com sucesso, redirecionar para a tela do aplicativo
                return JsonResponse({"message": "Login realizado com sucesso!"}, status=200)
            else:
                return JsonResponse({"message": "Credenciais inválidas!"}, status=401)        
        except Exception as e:
            return JsonResponse({"message": "Erro no servidor!", "error": str(e)}, status=500)

def esqueci_senha(request):
    """Exibe a página para o usuário digitar o e-mail para recuperação de senha."""
    return render(request, 'esqueci_senha.html')

def tela_inicial(request):
    """Exibe a página para o usuário digitar o e-mail para recuperação de senha."""
    return render(request, 'tela_inicial.html')

def enviar_email(request):
    """Recebe o e-mail do formulário e processa a solicitação de redefinição de senha."""
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            usuario = User.objects.get(email=email)
            # Aqui você poderia enviar o e-mail de recuperação
            return HttpResponse(f'Instruções para redefinir sua senha foram enviadas para {email}.')
        except User.DoesNotExist:
            return HttpResponse('E-mail não encontrado.')    

def get_user(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return render(request, 'tela_login.html')  # Redireciona para login se não estiver logado

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, 'tela_login.html')  # Redireciona para login se o usuário não for encontrado

def dashboard(request):
    """Exibe o painel principal com as listas de compras, histórico e informações do usuário."""
    user = get_user(request)

    # Criar uma lista de compras padrão se não houver nenhuma
    if not user.shopping_lists.exists():
        user.create_default_shopping_list()
    # Obtendo as listas de compras e itens do usuário autenticado
    shopping_lists = ShoppingList.objects.filter(user=user).prefetch_related('items')

    # Obtendo o histórico de compras (simulando como listas anteriores)
    purchase_history = ShoppingList.objects.filter(user=user)

    # Dados do usuário
    user_info = {
        'name': user.name,
        'email': user.email
    }

    # Contexto a ser enviado ao template
    context = {
        'user_name': user.name,  # Nome do usuário autenticado
        'user_email': user.email,  # Email do usuário autenticado
        'shopping_lists': shopping_lists,  # Listas de compras
        'purchase_history': purchase_history,  # Histórico de compras
    }
    #print(context)
    return render(request, 'tela_sitecompras.html', context)

        
def adicionar_item(request):
    """Função para adicionar um item à lista de compras."""
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        shopping_list_id = request.POST.get('shopping_list_id')
        
        try:
            # Verifica se a lista de compras existe
            shopping_list = ShoppingList.objects.get(id=shopping_list_id)
            
            # Adiciona o item à lista de compras
            Item.objects.create(name=item_name, shopping_list=shopping_list)
            
        except ShoppingList.DoesNotExist:
            return HttpResponse('A lista de compras não foi encontrada.')
        
    return redirect('dashboard')


def buscar_produtos(request):
    """Pesquisa produtos na base de dados."""
    if request.method == 'GET':
        query = request.GET.get('query', '')
        produtos = Product.objects.filter(name__icontains=query)  # Pesquisar produtos por nome
        produtos_data = [{'id': produto.id, 'name': produto.name, 'description': produto.description} for produto in produtos]
        return JsonResponse({'produtos': produtos_data})



#def adicionar_produto(request):
#    if request.method == 'POST':
#        produto_id = request.POST.get('produto_id')
#        lista_id = request.POST.get('lista_id')
#
#        try:
#            shopping_list = ShoppingList.objects.get(id=lista_id)
#            produto = Product.objects.get(id=produto_id)
#            item = Item.objects.create(name=produto.name, shopping_list=shopping_list, purchased=False)
#            
#            return JsonResponse({
#                'success': True,
#                'item': {
#                    'id': item.id,
#                    'name': item.name,
#                    'purchased': item.purchased
#                },
#                'message': 'Produto adicionado à lista com sucesso!'
#            })
#        except (ShoppingList.DoesNotExist, Product.DoesNotExist) as e:
#            return JsonResponse({'success': False, 'message': 'Erro ao adicionar o produto.'})
#

@csrf_exempt
def get_user(request):
    """Retorna os dados do usuário logado"""
    user_id = request.session.get('user_id')
    
    if not user_id:
        return JsonResponse({'message': 'Usuário não autenticado'}, status=401)

    try:
        user = User.objects.get(id=user_id)
        shopping_lists = ShoppingList.objects.filter(user=user)
        shopping_lists_data = [{'id': lista.id, 'name': lista.name} for lista in shopping_lists]
        user_data = {'id': user.id, 'name': user.name, 'email': user.email, 'shopping_lists': shopping_lists_data}
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Usuário não encontrado'}, status=404)


@csrf_exempt
def adicionar_produto(request):
    """Adiciona um produto à lista de compras"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')  # Agora recebemos o ID do produto
            lista_id = data.get('lista_id')
            quantidade = int(data.get('quantity', 1))
            
            shopping_list = ShoppingList.objects.get(id=lista_id)

            # Buscando o produto por ID, não pelo nome
            produto = Product.objects.get(id=produto_id)
            
            shopping_list_product, created = ShoppingListProduct.objects.update_or_create(
                shopping_list=shopping_list,
                product=produto,
                defaults={'quantity': quantidade, 'price': produto.price}
            )

            message = 'Produto adicionado com sucesso!' if created else 'Produto atualizado na lista de compras.'
            
            return JsonResponse({'success': True, 'message': message})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Produto não encontrado.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro ao adicionar o produto: {str(e)}'})
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})

def excluir_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        return JsonResponse({"success": True})
    except Item.DoesNotExist:
        return JsonResponse({"success": False})

# @login_required TODO: ENTENDER PQ ISSO N TA FUNCIONANDO
def criar_lista_compras(request):
    if request.method == 'POST':
        nome_lista = request.POST.get('nome')
        user = get_user(request)
        if nome_lista:
            nova_lista = ShoppingList.objects.create(name=nome_lista, user=user)  # Agora usando request.user
            nova_lista.save()
            return JsonResponse({'success': True, 'message': 'Lista de compras criada com sucesso!', 'lista_id': nova_lista.id})
        else:
            return JsonResponse({'success': False, 'message': 'Nome da lista não pode ser vazio.'})
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})


def get_itens_lista(request, lista_id):
    """ Retorna os produtos de uma lista de compras específica. """
    try:
        shopping_list = ShoppingList.objects.get(id=lista_id)
        produtos = ShoppingListProduct.objects.filter(shopping_list=shopping_list).select_related('product')
        produtos_json = [
            {
                'id': produto.product.id,
                'name': produto.product.name,
                'purchased': False,  # Se você quiser considerar o produto como 'purchased', ajuste isso.
                'quantity': produto.quantity,
                'price': float(produto.price) if produto.price else None
            } 
            for produto in produtos
        ]
        return JsonResponse({'success': True, 'itens': produtos_json})
    except ShoppingList.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Lista não encontrada'}, status=404)

def marcar_produto_como_comprado(request, lista_id, produto_id):
    """ Marca um produto como comprado ou pendente. """
    if request.method == 'POST':
        try:
            produto_lista = ShoppingListProduct.objects.get(shopping_list_id=lista_id, product_id=produto_id)
            produto_lista.purchased = not produto_lista.purchased  # Alterna o status
            produto_lista.save()
            
            return JsonResponse({'success': True, 'purchased': produto_lista.purchased})
        except ShoppingListProduct.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Produto não encontrado'}, status=404)
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)


def listar_receitas(request):
    """ Lista todas as receitas """
    receitas = Recipe.objects.all()
    return render(request, 'receitas.html', {'receitas': receitas})

def adicionar_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST.get('name')
        preparo = request.POST.get('preparation')

        if not nome_receita or not preparo:
            return JsonResponse({'success': False, 'error': 'Preencha todos os campos!'})
        
        nova_receita = Recipe.objects.create(name=nome_receita, preparation=preparo)
        
        nomes_ingredientes = request.POST.getlist('ingredient_name[]')
        quantidades_ingredientes = request.POST.getlist('ingredient_quantity[]')

        for nome, quantidade in zip(nomes_ingredientes, quantidades_ingredientes):
            if nome and quantidade:
                produto, _ = Product.objects.get_or_create(name=nome.strip())
                Ingredient.objects.create(
                    recipe=nova_receita,
                    product=produto,
                    quantity=quantidade.strip()
                )

        return JsonResponse({'success': True, 'receita': {'name': nova_receita.name}})
    else:
        return render(request, 'tela_sitecompras.html')
    
def excluir_receita(request, receita_id):
    """ Exclui uma receita """
    receita = get_object_or_404(Recipe, id=receita_id)
    receita.delete()
    return redirect('listar_receitas')

def adicionar_ingredientes_lista(request, receita_id, lista_id):
    """ Adiciona todos os ingredientes de uma receita na lista de compras """
    try:
        receita = Recipe.objects.get(id=receita_id)
        shopping_list = ShoppingList.objects.get(id=lista_id)
        
        for ingrediente in receita.ingredients.all():
            produto, _ = Product.objects.get_or_create(name=ingrediente.name)
            ShoppingListProduct.objects.create(
                shopping_list=shopping_list,
                product=produto,
                quantity=1  # Você pode definir uma quantidade padrão ou ajustar conforme o contexto
            )
        
        return JsonResponse({'success': True, 'message': 'Ingredientes adicionados à lista de compras.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})