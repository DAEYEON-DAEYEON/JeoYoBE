import json
from django.shortcuts import render, redirect
# Create your views here.


from django.http import JsonResponse
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
from ..serializers import UserSerializer, ServiceSerializer, AuctionSerializer
from ..models import User,Service,Auction
from django.views import View
from ..forms import UserForm, LoginForm, ServiceForm



class IndexView(View):
    def get(self, request):
        
        #product랑 service 최신순으로 각각 5개씩 가져오기
        products = Service.objects.filter(option = 0).order_by('-date')[:5]
        services = Service.objects.filter(option = 1).order_by('-date')[:5]
        
        for i in products:
            print(i)
        
        print("--------")
        
        for i in services:
            print(i)

        return render(request, 'index_2.html', {'products': products, 'services': services}) #임시수정
    
class Login(View):
    def get(self, request):
        return render(request, 'user/login.html')
    
class Logout(View):
    #로그아웃(세션 빼앗기)
    def get(self, request):
        dataid = request.GET.get('id')
        
        if User.objects.filter(id=dataid).exists():
            request.session['id'] = None
            request.session['name'] = None
            
            return redirect('/')  #임시수정
    
class Register(View):
    def get(self, request):
        return render(request, 'user/register.html')
    
class Create(View):
    def get(self, request):
        op = request.GET.get('op')
        data = {'op': op}
        return render(request, 'proser/create.html', data)


class List(View):
    def get(self, request):
        dataoption = request.GET.get('op')
        results = []
        queryset = Service.objects.filter(option = dataoption).order_by('serviceend','-usecredit', '-id').all()
        for i in queryset:
            results.append(
                {
                    'sid': i.id,
                    'uid': i.uid.id,
                    'name': i.name,
                    'des': i.des,
                    'img': i.img,
                    'option': i.option,
                    'offeruser': i.offeruser,
                    'maxval': i.maxval,
                    'date': i.date,
                    'serviceend': i.serviceend,
                    'usecredit': i.usecredit
                }
            )
            
        data = {'list': results, 'op':dataoption}
        # print(data)
        
        return render(request, 'proser/list.html', data)
    
# 상세보기
class Detail(View):
    def get(self, request):
        
        dataid = request.GET.get('sid')
        
        if Service.objects.filter(id=dataid).exists():
            servicedata = Service.objects.get(id=dataid)
            
            results = []
        
            # 내림차순으로 모델 정렬한것을 쿼리셋에 넣기
            queryset = Auction.objects.filter(sid = servicedata).all().order_by('-offerprice')
            # print(queryset[0].sid.name)

            for i in queryset:
                results.append(
                {
                    'aid': i.id,
                    'sid': i.sid.id,
                    'des': i.des if i.des else "",
                    'buyer': i.buyer.id,
                    'offerprice': i.offerprice,
                    'date': i.date,
                }
            )
            
            servicedata_dict = {
                #uid는 User 객체라서, 거 안에 있는 id로 접근해줘야 한다 ㅇㅇ
                'sid': servicedata.id,
                'uid': servicedata.uid.id,
                'name': servicedata.name,
                'img': servicedata.img,
                'des': servicedata.des,
                'op': servicedata.option,
                'offeruser': servicedata.offeruser,
                'maxval': servicedata.maxval,
                'date': servicedata.date,
                'serviceend': servicedata.serviceend,
                'usecredit': servicedata.usecredit,
                'auctions': results
            }
            
        data = servicedata_dict
            
        return render(request, 'proser/detail.html', data)
        


class Mypage(View):
    def get(self, request):
        userId = request.GET.get('uid')
        
        # 유저정보
        userdata = User.objects.get(id=userId)
        userdata_dict = {
            'id': userdata.id,
            'name': userdata.name,
            'credit': userdata.credit
        }
        
        # 내가 판매하는 물건
        products = []
        queryset = Service.objects.filter(uid = userId, serviceend = False, option="0").all()
        
        for i in queryset:
            products.append(
                {
                    'sid': i.id,
                    'uid': i.uid.id,
                    'name': i.name,
                    'des': i.des,
                    'img': i.img,
                    'option': i.option,
                    'offeruser': i.offeruser,
                    'maxval': i.maxval,
                    'date': i.date,
                    'serviceend': i.serviceend,
                    'usecredit': i.usecredit,
                }
            )
            
        auctions = []
        temauctions = Auction.objects.filter(buyer=userId, sid__serviceend = False)
        for i in temauctions:
            auctions.append(
                {
                    'sid': i.sid.id,
                    'name': i.sid.name,
                    'offerprice': i.offerprice,
                    'maxval': i.sid.maxval,
                }
            )
            
        done = []
        dones = Service.objects.filter(uid = userId, serviceend = True).all()
        for i in dones:
            done.append(
                {
                    'sid': i.id,
                    'uid': i.uid.id,
                    'name': i.name,
                    'maxval': i.maxval,
                    'usecredit': i.usecredit,
                }
            )
        

        data = {
            'user': userdata,
            'pro' : products,
            'auc' : auctions,
            'done': done
        }
        return render(request, 'user/mypage.html', data)