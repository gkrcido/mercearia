from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Produtos
class Produto(models.Model):
    tipo = models.CharField(max_length=20)
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=20)
    validade = models.CharField(max_length=10)
    
    class Meta:
        abstract = True  

class Cereal(Produto):
    marca = models.CharField(max_length=10)
    

class Laticinio(Produto):
    marca = models.CharField(max_length=10)
   
class Hortifruti(Produto):
    data_entrada = models.CharField(max_length=10)
    tipo_fornecedor = models.CharField(max_length=10)

    class Meta:
        abstract = True  

class Fruta (Hortifruti):
    pass

class Legume(Hortifruti):
    pass

class Verdura(Hortifruti):
    pass


# Usuários
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("O nome de usuário é obrigatório.")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


