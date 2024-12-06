from django.test import TestCase
from shelf.models import Product, Funcionario

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
id="PROD1",
nome="Produto Teste",
descrição="Descrição do produto teste",
preço=10.50,
quantidade=5
)
        self.assertEqual(product.nome, "Produto Teste")
        self.assertEqual(product.quantidade, 5)

class FuncionarioModelTest(TestCase):
    def test_create_funcionario(self):
        funcionario = Funcionario.objects.create(
nome="João Silva",
telefone="123456789",
cpf="123.456.789-00",
email="joao@example.com",
senha="senha123"
)
        self.assertEqual(funcionario.nome, "João Silva")
        self.assertEqual(funcionario.cpf, "123.456.789-00")