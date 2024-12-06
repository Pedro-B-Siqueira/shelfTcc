
from django.urls import path
from .views import (main_page, login_view, login_funcionario, cadastro,
                    produto_delete, produto_update, main_funcio, listar_funcionarios,
                    listar_produtos, listar_produtos_func, cadastrar_funcionario,
                    editar_funcionario, excluir_funcionario, produto_retirar,saida_estoque,
                    historico_produtos, criar_solicitacao, listar_solicitacoes,
                    atualizar_solicitacao, status_solicitacoes, gestao_solicitacao, relatorio_movimentacoes,
                    historico_produtos_funcio)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('cadastro/', cadastro, name='cadastro'),

    path('cadastrar_funcio/', cadastrar_funcionario, name='cadastrar_funcio'),

    path('listar_funcio/', listar_funcionarios, name='listar_funcio'),

    path('editar/<int:id>/', editar_funcionario, name='editar_funcionario'),

    path('excluir/<int:id>/', excluir_funcionario, name='excluir_funcionario'),

    path('listar_prod/', listar_produtos, name='listar_produtos'),

    path('listar_prodfuncio/', listar_produtos_func, name='listar_produtos_func'),

    path('login/', login_view, name='login'),

    path('', login_funcionario, name='login_funcio'),

    path('main/', main_page, name='main_page'),

    path('main_funcio', main_funcio, name='main_funcio'),

    path('editar_prod/<str:id>/', produto_update, name='produto_update'),

    path('excluir_prod/<str:id>/', produto_delete, name='produto_delete'),

    path('saida_estoque/', saida_estoque, name='saida_estoque'),

    path('produto_retirar/<int:id>/', produto_retirar, name='produto_retirar'),

    path('historico_produtos/', historico_produtos, name='historico_produtos'),

    path('historico_produtos_funcio/', historico_produtos_funcio, name='historico_produtos_funcio'),

    path('produto/solicitar/<int:id>/', criar_solicitacao, name='criar_solicitacao'),

    path('solicitacoes/', listar_solicitacoes, name='listar_solicitacoes'),

    path('solicitacao/<int:id>/', atualizar_solicitacao, name='atualizar_solicitacao'),

    path('status/', status_solicitacoes, name='status_solicitacoes'),

    path('gestao/', gestao_solicitacao, name='gestao_solicitacoes'),

    path('relatorio/', relatorio_movimentacoes, name='relatorio_movimentacoes'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)