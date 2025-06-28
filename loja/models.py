from django.db import models
from django.contrib.auth.models import User
#User é um modelo simples de cadastro/login nativo do django, irá ser usado nesse exemplo
from django.utils.text import slugify

class Customer(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    #isso é, o usuario só pode ter 1 nome e 1 nome só pode pertencer a 1 usuario
    #null=True: permite que a descrição fique nula (NULL) no banco.
    #null=True: permite que a descrição fique nula (NULL) no banco.  
    nome = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    # Campos adicionais
    cpf_cnpj = models.CharField(max_length=20, unique=True, null=True, blank=True)
    rg = models.CharField(max_length=20, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], null=True, blank=True)

    telefone_celular = models.CharField(max_length=20, null=True, blank=True)
    telefone_fixo = models.CharField(max_length=20, null=True, blank=True)

    rua = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)

    preferencias = models.TextField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    


class Produto(models.Model):
    CATEGORIAS = [
        ('eletronicos', 'Eletrônicos'),
        ('roupas', 'Roupas'),
        ('livros', 'Livros'),
        ('acessorios', 'Acessórios'),
        ('outros', 'Outros'),
    ]
    nome = models.CharField(max_length=200, null=True)
    preço = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    # O campo 'digital' vai servir para diferenciar os tipos de produtos do site: físicos e digitais.
    # Esse campo é um booleano, ou seja, só pode ter os valores True ou False.
    # Se for False (valor padrão), o produto será tratado como físico (ex: camisa, livro impresso).
    # Se for True, será tratado como um produto digital (ex: eBook, software), o que pode mudar a lógica do envio, frete etc.
    imagem = models.ImageField(null=True, blank=True)
    #imagens carregadas 
    descricao = models.TextField(null=True, blank=True)
    #descricao_longa = models.TextField(null=True, blank=True)  # descrição detalhada
    caracteristicas = models.TextField(null=True, blank=True)  # características técnicas
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='outros')
    estoque = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug_unico = base_slug
            contador = 1
            while Produto.objects.filter(slug=slug_unico).exists():
                slug_unico = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug_unico
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    #essa config transforma resolve um problema de erro que daria caso deletasse uma só imagem de produto, então, para evitar, foi criado esse código
    @property
    #Isso transforma o método imagensurl() em um atributo acessível como se fosse um campo normal.
    def imagemURL(self):   
        try:
            url = self.imagem.url
            #Aqui ele tenta acessar a URL da imagem associada ao campo self.imagens.
        except:
            url = ''
            #Se não conseguir pegar a URL (talvez porque nenhuma imagem foi enviada), retorna uma string vazia ao invés de estourar erro.
        return url
    

    @property
    def media_avaliacao(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return round(sum([a.nota for a in avaliacoes]) / avaliacoes.count(), 1)
        return 0

    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()








class Pedido(models.Model):
    cliente = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    #on_delete=models.SET_NULL: se o cliente for deletado, o campo cliente da ordem fica NULL (não apaga a ordem).
    data_pedido = models.DateTimeField(auto_now_add=True)
    #Campo que guarda a data e hora em que o pedido foi criado.
    #auto_now_add=True significa que o Django automaticamente coloca a data/hora no momento em que a ordem é criada.
    completo = models.BooleanField(default=False, null=True, blank=False)
    '''
    Quando o campo completo está como False, significa que o pedido ainda está em andamento — o cliente pode estar adicionando produtos no carrinho, revisando, ou ainda não finalizou a compra.
    Quando complete fica True, quer dizer que o cliente finalizou o pedido, ou seja:
    Confirmou a compra,
    Fechou o carrinho,
    Não vai mais adicionar ou remover itens,
    O sistema pode agora processar o pagamento, entrega, etc.
    '''
    id_transação = models.CharField(max_length=200, null=True)
    #serve para marcar a compra com um identificador único quando ela é finalizada.
    #é util pra identificar uma transação no sistema, evitar duplicidade caso duas compras tenham o mesmo conteudo e permitir rastreio e integração com gateways de pagamento
        


    #Esse modelo todo guarda informações básicas de uma ordem de compra, ligando ela a um cliente, registrando quando foi feita, se está finalizada e o ID da transação para controle financeiro.


    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        pedidoitem = self.pedidoitem_set.filter(produto__isnull=False)
        total = sum([item.get_total for item in pedidoitem])
        return total

    @property
    def get_cart_items(self):
        pedidoitem = self.pedidoitem_set.filter(produto__isnull=False)
        total = sum(item.quantidade for item in pedidoitem)
        return total

    @property
    def envio(self):
        envio = False
        pedidoitens = self.pedidoitem_set.filter(produto__isnull=False)
        for i in pedidoitens:
            if not i.produto.digital:
                envio = True
        return envio



class PedidoItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, blank=True, null=True)
    #Indica qual produto foi adicionado ao pedido.
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    #Um Pedido é uma cesta de compras.
    #Cada item dentro da cesta é um PedidoItem.
    #Então você precisa dizer a qual pedido cada item pertence. Essa linha faz essa ligação entre o item e o pedido.
    quantidade = models.IntegerField(default=0, null=True, blank=True)
    #Quantas unidades do produto foram compradas/adicionadas.
    data_adicionado = models.DateTimeField(auto_now_add=True)
    #Salva automaticamente a data/hora em que esse item foi adicionado ao pedido.
    #Esse modelo liga um produto a um pedido, permitindo que um pedido tenha vários produtos diferentes, e que cada produto esteja em quantidades diferentes.


    #exemplo:
    '''
    Pedido #1 tem:

    2 unidades de Produto A

    1 unidade de Produto B

    Isso seria representado com dois objetos PedidoItem, um para cada produto.

    🔗 Visualmente:
    ID	Produto	 Pedido	Quantidade	Data
    1	Camiseta  #10	   2 	   2025-06-11 13:40
    2	Boné	  #10	   1	   2025-06-11 13:41
    '''


    #com essa função nós conseguimos calcular os valores totais de produtos no carrinho
    #por exemplo se um produto no carrinho for um certo valor e tiver certas unidades, aparecerá o valor equivalente aquelas unidades para o produto especifico
    #(claramente deve ser configurado no template também)
    @property
    def get_total(self):
        total = self.produto.preço * self.quantidade
        #preço do produto que esta interligado com essa função(PedidoItem) * quantidade
        return total





class EndereçoEnvio(models.Model):
    cliente = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    endereço = models.CharField(max_length=200, null=True)
    cidade = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=200, null=True)
    cep = models.CharField(max_length=200, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.endereço
    




class Avaliacao(models.Model):
    cliente = models.ForeignKey(Customer, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)  # opcional, mas ajuda a vincular
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cliente', 'produto')  # Só permite uma avaliação por cliente por produto

    def __str__(self):
        return f'{self.cliente.nome} avaliou {self.produto.nome} com nota {self.nota}'





class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens_extra')
    imagem = models.ImageField(upload_to='imagens_produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"
