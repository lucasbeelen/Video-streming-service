from django import forms
from .models import CustomUser, Review
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        required=True,
        label="Confirm Password"
    )
    birthday = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],  # Aceita DD/MM/YYYY e YYYY-MM-DD
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ("username", 'first_name', 'last_name', 'email', 'cpf', 'birthday', 'password',)
        help_texts = {
            'username': None,  # Remove o help_text do username
        }
        widgets = {
            'password': forms.PasswordInput(),  # Definindo o campo 'password' como input de senha
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")
    
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if CustomUser.objects.filter(cpf=cpf).exists():
            raise ValidationError("Este CPF já está em uso.")
        return cpf 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escreva sua review...'}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }
        labels = {
            'rating': 'Nota',
        }
