from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager






class UserManager(BaseUserManager):
    def _create_user(self, name, login,password=None, **extra_fields):
        user = self.model(name=name, login=self.normalize_email(login),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('access', False)
        return self._create_user(name,login, password, **extra_fields)

    def create_superuser(self, name,login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('access', True)

        return self._create_user(name, login, password, **extra_fields)




class User_mon(AbstractBaseUser):
    REGION_CHOICES = (
        ('Чуйская', 'Чуйская'),
        ('Иссык-кульская', 'Иссык-кульская'),
        ('Нарынская', 'Нарынская'),
        ('Джалал-Абадская', 'Джалал-Абадская'),
        ('Баткенская', 'Баткенская'),
        ('Ошская', 'Ошская'),
        ('Таласская', 'Таласская')
    )
    name = models.CharField(max_length=100, null=True,verbose_name = 'Имя')
    surname = models.CharField(max_length=100, null=True,verbose_name = 'Фамилия')
    login = models.CharField(max_length=200, null=True,blank=True, unique=True,verbose_name = 'логин')
    password = models.CharField(max_length=200, null=True,verbose_name = 'пароль')
    date_reg = models.DateTimeField(auto_now_add=True, null= True,verbose_name = 'Дата  регистрации')
    is_staff = models.BooleanField(default=False,verbose_name = 'Права на админа')
    access = models.BooleanField(default=False ,verbose_name = 'Доступ к оплатам')
    is_active = models.BooleanField(default=False,verbose_name = 'Доступ к авторизации')
    balance = models.PositiveBigIntegerField(default=0, null=True ,verbose_name = 'Баланс')
    avail_balance = models.BigIntegerField(default=0, null=True ,verbose_name = 'Сумма оплат')
    region = models.CharField(max_length=100, choices=REGION_CHOICES,default='Чуйская',verbose_name = 'Регион')
    refill = models.BigIntegerField(default=0, null=True ,verbose_name = 'Пополнение баланса')
    write_off = models.BigIntegerField(default=0, null=True ,verbose_name = 'Списание баланса')
    comment = models.TextField(blank=True)



    objects = UserManager()
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name']
    class Meta:
         verbose_name = 'Пользователь'
         verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.surname} {self.name}"

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff



class Pays(models.Model):
    number_payment = models.CharField(max_length=100, null=True)
    date_payment = models.CharField(verbose_name = 'Дата',max_length=100, null=True)
    accept_payment = models.CharField(max_length=100, null=True)
    ls_abon = models.CharField(max_length=100, null=True,verbose_name = 'Лицевой счет')
    money = models.CharField(max_length=30, null=True ,verbose_name = 'Сумма')
    status_payment = models.CharField(max_length=100, null=True,verbose_name = 'Статус  оплаты')
    user = models.ForeignKey(verbose_name = 'Монтажник',
        to=User_mon,
        on_delete=models.CASCADE,
        related_name='user_id'
    )
    annulment = models.BooleanField(default=False, verbose_name = 'Аннулирование')
    comment = models.TextField(blank=True,verbose_name='Комментарии')
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
         verbose_name = 'История  платежа'
         verbose_name_plural = 'История  платежей'
 
    def __str__(self) -> str:
        return self.status_payment





class Comment(models.Model):
    user2 = models.ForeignKey(verbose_name = 'Монтажник',
        to=User_mon,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(null=True, verbose_name='Комментарии')
    type_pay = models.CharField(max_length=30, null=True, verbose_name = 'Тип платежа')
    old_balance = models.BigIntegerField(default=0, null=True,verbose_name = 'До пололнения ')
    new_balance = models.BigIntegerField(default=0, null=True, verbose_name = 'Пополненная сумма')
    mont_balance  = models.PositiveBigIntegerField(default=0, null=True ,verbose_name = 'Баланс')
    old_avail_balance= models.BigIntegerField(default=0, null=True,verbose_name = 'До списания')
    new_avail_balance = models.BigIntegerField(default=0, null=True, verbose_name = 'Списание')
    mont_avail_balance  = models.BigIntegerField(default=0, null=True ,verbose_name = 'Сумма оплат')    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         verbose_name = 'Операции платежей'
         verbose_name_plural = 'Операции платежей'

    def __str__(self):
        return str(self.old_balance) 


