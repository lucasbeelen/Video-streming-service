from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from content.models import Movie, Serie
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    cpf = models.CharField(unique=True,
                        max_length=11, 
                        validators=[
                        RegexValidator(
                        regex=r'^\d{11}$',  # Expressão regular para 11 dígitos numéricos
                        code='invalid_cpf'
                        )],              
    )
    birthday = models.DateField(auto_now=False, auto_now_add=False , blank=True, null=True)
    subscription_level = models.CharField(max_length=50, default='free')  
    parental_control_enabled = models.BooleanField(default=False)  
    recommendations = models.ManyToManyField('content.Movie', related_name='recommended_users', blank=True) 
        
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Defina um related_name único
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',  # Defina um related_name único
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )    

    def __str__(self):
        return self.username
    
    @property
    def age(self):
        today = date.today()
        # Calcular a idade
        age = today.year - self.birthday.year

        # Verificar se o aniversário ainda não passou neste ano
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1

        return age


class Bookmark(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id')  
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bookmark by {self.user} for {self.content_object}"
    
    
class WatchHistory(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id')  
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Watched by {self.user} for {self.content_object}"
    

class Review(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id')  # 'Content' seria um modelo que representa Movie ou Serie
    comment = models.TextField(max_length=500)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Avaliação de 1 a 5
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.content.title}'

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')