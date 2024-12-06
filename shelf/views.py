from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from .forms import ProductForm, FuncionarioForm
from .models import Product, Funcionario, ProductRequest

from django.contrib.auth.models import User
from django.contrib import messages


from .models import ProductHistory
from django.http import HttpResponse
from itertools import chain

#Paginas principais
def main_page(requests):
    return render(requests, 'shelf/main.html')

def main_funcio(requests):
    return render(requests, 'shelf/main_funcio.html')

#Cadastro de Funcionários
def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_funcio')
    else:
        form = FuncionarioForm()
    return render(request, 'shelf/CadFuncio.html', {'form': form})


def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'shelf/listar_funcio.html', {'funcionarios': funcionarios})


def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, pk=id)

    if request.method == "POST":
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('listar_funcio')
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'shelf/editar_funcionario.html', {'form': form})


def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == "POST":
        funcionario.delete()
        return redirect('listar_funcio')  # Redirect after deletion

    return render(request, 'shelf/excluir_funcionario.html', {'funcionario': funcionario})

#Logins
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists and is a superuser
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                authenticated_user = authenticate(username=username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('main_page')  # Redirect to main page after successful login
                else:
                    # If authentication fails, add an error message
                    messages.error(request, '*Credenciais inválidas.')
            else:
                # Handle case when user is not a superuser
                messages.error(request, '*Apenas superusuários podem fazer login.')
        except User.DoesNotExist:
            # Handle case when user does not exist
            messages.error(request, '*Usuário não encontrado.')

    # Render the login template
    return render(request, 'shelf/login.html', {'form': AuthenticationForm()})


def login_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        try:
            funcionario = Funcionario.objects.get(nome=nome)
            if funcionario.senha == senha:
                # Redireciona após o login bem-sucedido
                return redirect('main_funcio')  # Substitua 'pagina_inicial' pelo nome da URL desejada
            else:
                error_message = "*Credenciais inválidas."
        except Funcionario.DoesNotExist:
            error_message = "*Funcionário não encontrado."

        return render(request, 'shelf/login_funcio.html', {'error_message': error_message})

    return render(request, 'shelf/login_funcio.html')

#Cadastro de Produtos
def cadastro(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProductForm()
    return render(request, 'shelf/CadProd.html', {'form': form})

def produto_update(request, id):
    produto = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=produto)  # Inclua request.FILES aqui
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')  # Redirecionar para a página de listagem
    else:
        form = ProductForm(instance=produto)

    return render(request, 'shelf/produto_form.html', {'form': form})

def produto_delete(request, id):
    produto = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')  # Redirecionar para a página de listagem
    return render(request, 'shelf/produto_confirm_delete.html', {'produto': produto})

def listar_produtos(request):
    search_term = request.GET.get('search', '')  # Obtém o termo de pesquisa, se houver
    if search_term:
        produtos = Product.objects.filter(nome__icontains=search_term)  # Filtra produtos pelo nome
    else:
        produtos = Product.objects.order_by('quantidade')  # Caso não haja pesquisa, retorna todos os produtos

    return render(request, 'shelf/listar_produtos.html', {'produtos': produtos})


def listar_produtos_func(request):
    produtos = Product.objects.all()
    return render(request, 'shelf/listar_produtos_func.html', {'produtos': produtos})


#Retirar Produto
def saida_estoque(request):
    search_term = request.GET.get('search', '')  # Obtém o termo de pesquisa, se houver
    if search_term:
        produtos = Product.objects.filter(nome__icontains=search_term)  # Filtra produtos pelo nome
    else:
        produtos = Product.objects.order_by('quantidade')  # Caso não haja pesquisa, retorna todos os produtos

    return render(request, 'shelf/saida_estoqueADM.html', {'produtos': produtos})


def produto_retirar(request, id):
    produto = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        quantidade_retirada = int(request.POST.get('quantidade', 0))

        if quantidade_retirada > produto.quantidade:
            return HttpResponse('Quantidade solicitada maior que a disponível no estoque.', status=400)

        # Atualiza a quantidade do produto no estoque
        produto.quantidade -= quantidade_retirada
        produto.save()

        # Registra no histórico
        ProductHistory.objects.create(
            produto=produto,
            quantidade_retirada=quantidade_retirada,
        )

        return redirect('saida_estoque')  # Redireciona para a página de listagem de produtos após a retirada

    return render(request, 'shelf/retirar_produtoADM.html', {'produto': produto})

#Histórico
def historico_produtos(request):
    # Consulta os registros do histórico ordenados pela data mais recente
    historico = ProductHistory.objects.select_related('produto').order_by('-data_retirada')
    return render(request, 'shelf/historico_produtos.html', {'historico': historico})

def historico_produtos_funcio(request):
    # Consulta os registros do histórico ordenados pela data mais recente
    historico = ProductHistory.objects.select_related('produto').order_by('-data_retirada')
    return render(request, 'shelf/historico_produtos_func.html', {'historico': historico})

def atualizar_solicitacao(request, id):
    solicitacao = get_object_or_404(ProductRequest, id=id)

    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'Aceitar':
            if solicitacao.quantidade <= solicitacao.produto.quantidade:
                # Atualiza o estoque
                solicitacao.produto.quantidade -= solicitacao.quantidade
                solicitacao.produto.save()

                # Registra no histórico
                ProductHistory.objects.create(
                    produto=solicitacao.produto,
                    quantidade_retirada=solicitacao.quantidade
                )

                # Atualiza o status da solicitação
                solicitacao.status = 'Aceita'
            else:
                return HttpResponse('Erro: Quantidade solicitada indisponível no estoque.', status=400)
        elif acao == 'Negar':
            solicitacao.status = 'Negada'

        solicitacao.save()
        return redirect('gestao_solicitacoes')  # Redireciona para a página de gestão de solicitações

    return render(request, 'shelf/solicitar_gestaoADM.html', {'solicitacao': solicitacao})


#Solicitação

def criar_solicitacao(request, id):
    produto = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 0))
        destinatario = request.POST.get('destinatario', '').strip()

        if quantidade > produto.quantidade:
            return HttpResponse('Quantidade solicitada maior que a disponível no estoque.', status=400)

        if not destinatario:
            return HttpResponse('Destinatário é obrigatório.', status=400)

        # Criação da solicitação
        ProductRequest.objects.create(
            produto=produto,
            quantidade=quantidade,
            destinatario=destinatario
        )
        return redirect('listar_solicitacoes')

    return render(request, 'shelf/solicitar_produtoFUN.html', {'produto': produto})


def gestao_solicitacao(request):
    solicitacoes = ProductRequest.objects.filter(status='Pendente').order_by('-date_created')
    return render(request, 'shelf/solicitar_gestaoADM.html', {'solicitacoes': solicitacoes})

def listar_solicitacoes(request):
    solicitacoes = ProductRequest.objects.all().order_by('-date_created')
    return render(request, 'shelf/solicitar_statusFUN.html', {'solicitacoes': solicitacoes})

def status_solicitacoes(request):
    solicitacoes = ProductRequest.objects.all().order_by('-date_created')
    return render(request, 'shelf/solicitar_statusFUN.html', {'solicitacoes': solicitacoes})

#Relatório

def relatorio_movimentacoes(request):
    # Obter registros do histórico
    movimentacoes_historico = ProductHistory.objects.select_related('produto').order_by('-data_retirada')

    # Adicionar produtos cadastrados como "Entradas" com base no date_created
    produtos_cadastrados = Product.objects.filter(historico__isnull=True).order_by('-date_created')
    entradas_cadastradas = [
        {
            'tipo': 'Entrada',
            'produto': produto,
            'quantidade_retirada': produto.quantidade,
            'data_retirada': produto.date_created,
            'destinatario': 'Almoxarifado'
        }
        for produto in produtos_cadastrados
    ]

    # Combinar movimentações e entradas
    movimentacoes = list(chain(
        [{'tipo': 'Saída',
          'produto': mov.produto,
          'quantidade_retirada': mov.quantidade_retirada,
          'data_retirada': mov.data_retirada,
          'destinatario': ProductRequest.objects.filter(produto=mov.produto, quantidade=mov.quantidade_retirada).first().destinatario if ProductRequest.objects.filter(produto=mov.produto, quantidade=mov.quantidade_retirada).exists() else 'Administrador'}
         for mov in movimentacoes_historico],
        entradas_cadastradas
    ))

    return render(request, 'shelf/relatorio.html', {'movimentacoes': movimentacoes})
