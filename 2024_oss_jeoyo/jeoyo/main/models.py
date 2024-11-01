from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=100, primary_key = True)
    name = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    credit = models.IntegerField()
    
    def __str__(self):
        return self.name

class Service(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length= 80)
    des = models.CharField(max_length= 150)
    img = models.CharField(max_length=255)
    option = models.CharField(max_length= 10)
    offeruser = models.CharField(max_length= 80)
    maxval = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    serviceend = models.BooleanField(default=False)
    usecredit = models.IntegerField(default=0)

    #다른 클래스에서 User라는걸 불러왔을 때, 간단하게 나마 보여지는 정보(어노테이션, 디스크립션)
    def __str__(self):
        return self.name    


class Auction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    sid = models.ForeignKey(Service, on_delete=models.CASCADE)
    offerprice = models.IntegerField()
    des = models.CharField(max_length= 255, null=True)
    date = models.DateTimeField(auto_now_add=True)

    #다른 클래스에서 Auction이라는걸 불러왔을 때, 간단하게 나마 보여지는 정보(어노테이션, 디스크립션)
    #근데 이새끼 어드민 페이지에서만 볼 수 있는듯 이새끼떄문에 오류가 존나 나버려 ㅇㅇ
    # def __str__(self):
    #     return self.des
   