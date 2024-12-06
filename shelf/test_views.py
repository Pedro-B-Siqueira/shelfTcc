from django.test import TestCase
from django.urls import reverse
from shelf.models import Product, Funcionario

class ShelfViewsTest(TestCase):
    def test_main_page_view(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shelf/main.html')

    def test_cadastro_produto_view(self):
        response = self.client.post(reverse('cadastro'), {
            'id': 'PROD2',
            'nome': 'Produto Novo',
            'descrição': 'Descrição do produto',
            'preço': 20.0,
            'quantidade': 10
})
        self.assertEqual(response.status_code, 302) # Redirecionamento após sucesso
        self.assertTrue(Product.objects.filter(nome='Produto Novo').exists())

    def test_cadastrar_funcionario_view(self):
        response = self.client.post(reverse('cadastrar_funcio'), {
            'nome': 'Maria Souza',
            'telefone': '987654321',
            'cpf': '987.654.321-00',
            'email': 'maria@example.com',
            'senha': 'senha456'
})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Funcionario.objects.filter(nome='Maria Souza').exists())