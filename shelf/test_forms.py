from django.test import TestCase
from shelf.forms import ProductForm, FuncionarioForm

class ProductFormTest(TestCase):
    def test_valid_product_form(self):
        form_data = {
            'id': 'PROD3',
            'nome': 'Produto Form Teste',
            'descrição': 'Teste de formulário de produto',
            'preço': 15.0,
            'quantidade': 8
}
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_product_form(self):
        form_data = {
            'id': '',
'nome': '',
'descrição': '',
'preço': -10.0,
'quantidade': -5
}
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

class FuncionarioFormTest(TestCase):
    def test_valid_funcionario_form(self):
        form_data = {
'nome': 'Carlos Mendes',
'telefone': '456123789',
'cpf': '456.123.789-10',
'email': 'carlos@example.com',
'senha': 'senha789'
}
        form = FuncionarioForm(data=form_data)
        self.assertTrue(form.is_valid())