from django.db import models
from datetime import datetime,date

# Create your models here.
class Members(models.Model):
    name=models.CharField(max_length=12)
    phone=models.CharField(max_length=15)
    fee_amount=models.DecimalField(max_digits=10,decimal_places=2)
    fee_date=models.DateField(null=True,blank=True)
    picture=models.ImageField(upload_to='image/',blank=True,null=True)
    status_choices=[("active","Active"),("non active","Non Active")]
    status=models.CharField(choices=status_choices,default="active",max_length=10)
    def __str__(self):
        return self.name
class Payment(models.Model):
    member=models.ForeignKey(Members,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    payment_date=models.DateField(null=True,blank=True)
    status_choices=[("paid","Paid"),("due","Due")]
    status=models.CharField(choices=status_choices,default="paid",max_length=4)
    def __str__(self):
        return self.member


class GymReport(models.Model):
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    revenue=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return self.revenue