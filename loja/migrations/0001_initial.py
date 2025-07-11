# Generated by Django 5.2.3 on 2025-06-27 19:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, null=True)),
                ('preço', models.DecimalField(decimal_places=2, max_digits=7)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='')),
                ('descricao', models.TextField(blank=True, null=True)),
                ('descricao_longa', models.TextField(blank=True, null=True)),
                ('caracteristicas', models.TextField(blank=True, null=True)),
                ('categoria', models.CharField(choices=[('eletronicos', 'Eletrônicos'), ('roupas', 'Roupas'), ('livros', 'Livros'), ('acessorios', 'Acessórios'), ('outros', 'Outros')], default='outros', max_length=50)),
                ('estoque', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200)),
                ('cpf_cnpj', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('rg', models.CharField(blank=True, max_length=20, null=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('genero', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=20, null=True)),
                ('telefone_celular', models.CharField(blank=True, max_length=20, null=True)),
                ('telefone_fixo', models.CharField(blank=True, max_length=20, null=True)),
                ('rua', models.CharField(blank=True, max_length=255, null=True)),
                ('numero', models.CharField(blank=True, max_length=10, null=True)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(blank=True, max_length=2, null=True)),
                ('cep', models.CharField(blank=True, max_length=10, null=True)),
                ('preferencias', models.TextField(blank=True, null=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('completo', models.BooleanField(default=False, null=True)),
                ('id_transação', models.CharField(max_length=200, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.customer')),
            ],
        ),
        migrations.CreateModel(
            name='EndereçoEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereço', models.CharField(max_length=200, null=True)),
                ('cidade', models.CharField(max_length=200, null=True)),
                ('estado', models.CharField(max_length=200, null=True)),
                ('cep', models.CharField(max_length=200, null=True)),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.customer')),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(blank=True, default=0, null=True)),
                ('data_adicionado', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.pedido')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.produto')),
            ],
        ),
        migrations.CreateModel(
            name='ImagemProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imagens_produtos/')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens_extra', to='loja.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comentario', models.TextField(blank=True, null=True)),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.customer')),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loja.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='loja.produto')),
            ],
            options={
                'unique_together': {('cliente', 'produto')},
            },
        ),
    ]
