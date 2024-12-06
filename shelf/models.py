from django.db import models
from django.utils.timezone import now

class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=100)
    descrição = models.TextField()
    imagem = models.ImageField(upload_to='products/', null=True, blank=True)
    preço = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    date_created = models.DateTimeField(default=now)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome}"

class ProductHistory(models.Model):
    produto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="historico")
    quantidade_retirada = models.IntegerField()
    data_retirada = models.DateTimeField(default=now)

    def __str__(self):
        return f"Retirada: {self.produto.nome} ({self.quantidade_retirada} unidades)"


class ProductRequest(models.Model):
    produto = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    destinatario = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[('Pendente', 'Pendente'), ('Aceita', 'Aceita'), ('Negada', 'Negada')],
        default='Pendente'
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitação para {self.produto.nome} - {self.quantidade}"
