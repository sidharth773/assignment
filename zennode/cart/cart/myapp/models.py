from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone=models.CharField(max_length=10,default='')

class Mycart(models.Model):
    costm=models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    product_a=models.IntegerField(verbose_name="Product A",default=0)
    product_b=models.IntegerField(verbose_name="Product B",default=0)
    product_c=models.IntegerField(verbose_name="Product C",default=0)
    price=models.IntegerField(verbose_name="Total Price",default=0)



