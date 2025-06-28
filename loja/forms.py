from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class FormRegistro(UserCreationForm):
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Usuário'
    }))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Digite seu e-mail'
    }))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Digite sua senha'
    }))
    password2 = forms.CharField(label='Confirme a Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirme sua senha'
    }))

    cpf_cnpj = forms.CharField(label='CPF ou CNPJ', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '123.456.789-00 ou 12.345.678/0001-99'
    }))
    rg = forms.CharField(label='RG', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '12.345.678-9'
    }))
    data_nascimento = forms.DateField(label='Data de Nascimento', widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control'
    }))
    genero = forms.ChoiceField(label='Gênero', choices=[('', 'Selecione'), ('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
                               widget=forms.Select(attrs={'class': 'form-select'}))
    telefone_celular = forms.CharField(label='Telefone Celular', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '(00) 91234-5678'
    }))
    telefone_fixo = forms.CharField(label='Telefone Fixo', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '(00) 1234-5678'
    }))
    rua = forms.CharField(label='Rua', widget=forms.TextInput(attrs={'class': 'form-control'}))
    numero = forms.CharField(label='Número', widget=forms.TextInput(attrs={'class': 'form-control'}))
    complemento = forms.CharField(label='Complemento', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bairro = forms.CharField(label='Bairro', widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(label='Cidade', widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(label='Estado', max_length=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cep = forms.CharField(label='CEP', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}))
    preferencias = forms.CharField(label='Preferências/Observações', required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': 3, 'placeholder': 'Promoções, interesses...'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        if Customer.objects.filter(cpf_cnpj=cpf_cnpj).exists():
            raise forms.ValidationError('CPF/CNPJ já cadastrado.')
        return cpf_cnpj


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Cria o Customer com os dados extras
        Customer.objects.create(
            usuario=user,
            nome=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            cpf_cnpj=self.cleaned_data.get('cpf_cnpj'),
            rg=self.cleaned_data.get('rg'),
            data_nascimento=self.cleaned_data.get('data_nascimento'),
            genero=self.cleaned_data.get('genero'),
            telefone_celular=self.cleaned_data.get('telefone_celular'),
            telefone_fixo=self.cleaned_data.get('telefone_fixo'),
            rua=self.cleaned_data.get('rua'),
            numero=self.cleaned_data.get('numero'),
            complemento=self.cleaned_data.get('complemento'),
            bairro=self.cleaned_data.get('bairro'),
            cidade=self.cleaned_data.get('cidade'),
            estado=self.cleaned_data.get('estado'),
            cep=self.cleaned_data.get('cep'),
            preferencias=self.cleaned_data.get('preferencias'),
        )

        return user
