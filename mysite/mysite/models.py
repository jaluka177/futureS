from django.db import models



class Member(models.Model):
    member_id = models.AutoField(primary_key=True)  #AutoField
    member_name = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=12)
    type = models.CharField(max_length=3 , null=True)

    def __int__(self):
        return self.member_id
