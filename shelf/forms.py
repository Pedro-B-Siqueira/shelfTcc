from django import forms
from .models import Product, Funcionario

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'nome', 'descrição', 'imagem', 'preço', 'quantidade']

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'telefone', 'cpf', 'email', 'senha']
        widgets = {
            'senha': forms.PasswordInput(render_value=True),
        }

