from django.urls import path
from . import views
urlpatterns=[
    path('login/',views.login,name="login"),
    path('tela_inicial/',views.tela_inicial,name="tela_inicial"),
    path('cadastro/',views.cadastro,name="cadastro"),
    path('esqueci_senha/',views.esqueci_senha,name="esqueci_senha"),
    path('enviar_email/', views.enviar_email, name="enviar_email"),
    path('sitecompras/',views.dashboard,name="dashboard"),
    path('adicionar_item/', views.adicionar_item, name='adicionar_item'),
    path('adicionar_produto/', views.adicionar_produto, name='adicionar_produto'),
    path('buscar_produtos/', views.buscar_produtos, name='buscar_produtos'),
    path('excluir_item/<int:item_id>/', views.excluir_item, name='excluir_item'),
    path('criar_lista_compras', views.criar_lista_compras, name='criar_lista_compras'),
    path('get_itens_lista/<int:lista_id>/', views.get_itens_lista, name='get_itens_lista'),
    path('marcar_produto_como_comprado/<int:lista_id>/<int:produto_id>/', views.marcar_produto_como_comprado, name='marcar_produto_como_comprado'),
    path('receitas/', views.listar_receitas, name='listar_receitas'),
    path('adicionar_receita/', views.adicionar_receita, name='adicionar_receita'),
    path('excluir_receita/<int:receita_id>/', views.excluir_receita, name='excluir_receita'),
    path('adicionar_ingredientes_lista/<int:receita_id>/<int:lista_id>/', views.adicionar_ingredientes_lista, name='adicionar_ingredientes_lista'),
    path('',views.tela_inicial,name="tela_inicial"),
    path('csrf/',views.csrf, name='csrf'),
    path('get_user/', views.get_user, name='get_user')
]
    