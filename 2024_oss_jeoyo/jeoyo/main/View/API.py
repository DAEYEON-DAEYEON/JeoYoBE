import json
from django.shortcuts import render
# Create your views here.

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import UserSerializer, ServiceSerializer, AuctionSerializer
from ..models import User,Service,Auction
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from ..forms import UserForm, LoginForm, ServiceForm
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    
    
class UserAPI(APIView):
    def get(self, request):
        dataid = request.GET.get('id')
        
        if User.objects.filter(id=dataid).exists():
            userdata = User.objects.get(id=dataid)
            userdata_dict = {
                'id': userdata.id,
                'name': userdata.name,
                'password': userdata.password,
                'credit': userdata.credit
                # Add other fields as needed
            }
            return JsonResponse(userdata_dict, status=200)
            # serializer = UserSerializer(queryset, many=True)
            # queryset = User.objects.all()
            # print(queryset)
        else:
            HttpResponse("Failed", status=400)
    
    def put(self, request):
        dataid = request.POST.get('id')
        dataname = request.POST.get('name')
        datapassword = request.POST.get('password')
        datacredit = request.POST.get('credit')

        if User.objects.filter(id=dataid).exists():
            user = User.objects.get(id=dataid)
            user.name = dataname
            user.password = datapassword
            user.credit = datacredit
            user.save()
            
            return HttpResponse("Success", status=200)
        else:
            return HttpResponse("User not found", status=404)
    
    
class RegisterAPI(APIView):
        def post(self, request):
            form = UserForm(request.POST)
            
            if form.is_valid():
                dataid = form.cleaned_data['id']
                dataname = form.cleaned_data['name']
                datapassword = form.cleaned_data['password']
                #datacredit = form.cleaned_data['credit']

                # ID가 존재하는지 확인하고, 중복이라면 400으로 리젝시킴. 성공시에는 200반환
                if User.objects.filter(id=dataid).exists():
                    return HttpResponse("Duplicated. Fail", status=400)
                else:
                    User.objects.create(id = dataid, name=dataname, password=datapassword, credit= 0)
                    return HttpResponse("Success.", status=201) 
            else:
                return HttpResponse("Just Failed.", status=401)
            
            
class LoginAPI(APIView):
    
    #로그인(세션 부여)
    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            dataid = form.cleaned_data['id']
            datapassword = form.cleaned_data['password']
            
            if User.objects.filter(id=dataid).filter(password=datapassword).exists():
                UserObj = User.objects.get(id=dataid)
                request.session['id'] = UserObj.id
                request.session['name'] = UserObj.name
                return HttpResponse("Success.", status=200) 
            else:
                return HttpResponse("Failed.", status=400)
        else:
            return HttpResponse("Just Failed", status=201)
     

# class LogoutAPI(APIView):
#     #로그아웃(세션 빼앗기)
#     def get(self, request):
#         dataid = request.GET.get('id')
        
#         if User.objects.filter(id=dataid).exists():
#             request.session['id'] = None
#             request.session['name'] = None
            
#             return HttpResponse("Success", status = 200)
        
#         else: 
#             return HttpResponse("Failed", status = 400)
        

        
class ServiceListAPI(APIView):
    def get(self, request):
        dataoption = request.GET.get('option')
        print("들어가긴 함 ㅇㅇ")
        results = []
        queryset = Service.objects.filter(option = dataoption).order_by('-usecredit', '-id').all()
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
                    'usecredit': i.usecredit,
                }
            )
        
        #serializer = ServiceSerializer(queryset, many=True)
    
        return JsonResponse(results, safe=False, status = 200)
         
        
        
        
        
class ServiceAPI(APIView):
    def get(self, request):
        
        dataid = request.GET.get('sid')
        
        if Service.objects.filter(id=dataid).exists():
            servicedata = Service.objects.get(id=dataid)
            servicedata_dict = {
                #uid는 User 객체라서, 거 안에 있는 id로 접근해줘야 한다 ㅇㅇ
                'sid': servicedata.id,
                'uid': servicedata.uid.id,
                'name': servicedata.name,
                'img': servicedata.img,
                'des': servicedata.des,
                'option': servicedata.option,
                'offeruser': servicedata.offeruser,
                'maxval': servicedata.maxval,
                'date': servicedata.date,
                'serviceend': servicedata.serviceend,
                'usecredit': servicedata.usecredit,
                # Add other fields as needed
            }
            return JsonResponse(servicedata_dict, status=200)
        
        else:
            return HttpResponse("받는것 조차 실패", status = 400)
    
    #최초 제시 API
    def post(self, request):
        # if request in FILES: 
        form = ServiceForm(request.POST, request.FILES)
        # else:
        #     form = ServiceForm(request.POST)
        print("받긴 받음")
        
        if form.is_valid():
            print("유효성 ㅇㅇ")
            user_uuid = uuid.uuid4()  # 새로운 UUID 생성
            # file_content = form['img']
            # file_content = request.FILES['img']
            # names = list(file_content.name.split('.'))
            #print(names[1])
            dataname = form.cleaned_data['name']
            datades = form.cleaned_data['des']
            dataoption = form.cleaned_data['option']
            datamaxval = form.cleaned_data['maxval']
            datauid = form.cleaned_data['uid']
            dataofferuser = form.cleaned_data['offeruser']
            
            print(datauid)
            print(dataname)
            print(datades)
            
            saved_file_path = "null-img.png"
            print(request.FILES)
            if "img" in request.FILES:
                file_content = request.FILES['img']
                names = list(file_content.name.split('.'))
                #파일 경로 생성
                file_path = f'{user_uuid}.{names[1]}'
                # 저장. (리턴값: 저장된 파일 경로)
                saved_file_path = default_storage.save(file_path, ContentFile(file_content.read()))
            else:
                print("null이당")
            print(saved_file_path)
            
            tmpUser = User.objects.get(id = datauid)
            print(tmpUser)
            
            #해당 필드에 넣고 저장 끝~
            Service.objects.create(
                uid = tmpUser, 
                name=dataname,
                des = datades,
                img = saved_file_path,
                option = dataoption,
                maxval = datamaxval,
                offeruser = dataofferuser,
            )
           
            
            return HttpResponse("Success", status = 200)
        
        else:
            return HttpResponse("받는것 조차 실패", status = 400)
    
    #제시하기(구매자 입장에서 가격 제시)
    def put(self, request):
        
        datasid = request.POST.get('sid')  
        dataofferuserid = request.POST.get('offeruserid')
        datamaxval = request.POST.get('maxval')
        datades = request.POST.get('des')
        
        servicedata = Service.objects.get(id = datasid)
        tmpuser = User.objects.get(id = dataofferuserid)
        
        print(tmpuser)
        print(servicedata.maxval)
        
        # 제시하려는 금액이 여태까지 나온 maxval 보다 낮거나 같고 OR 현재 보유 크레딧이 제시한 credit 보다 낮을 때 반려 시킴 ㅇㅇ
        if int(servicedata.maxval) >= int(datamaxval):
            return HttpResponse("Low Maxval", status = 404)
        if int(tmpuser.credit) < int(datamaxval):
            return HttpResponse("Not Enough Credit", status = 405)
        
        else: 
            #Auction Row Create ㅇㅇ
            Auction.objects.create(buyer = tmpuser, sid = servicedata, offerprice = datamaxval, des = datades)
            servicedata.id = datasid
            servicedata.offeruser = dataofferuserid
            servicedata.maxval = datamaxval
            servicedata.save()
            return HttpResponse("Success", status = 200)
        
        
        
class AuctionListAPI(APIView):
    def get(self, request):
        datasid = request.GET.get('sid')
        # print(datasid)
        
        results = []
        
        # 내림차순으로 모델 정렬한것을 쿼리셋에 넣기
        queryset = Auction.objects.filter(sid = datasid).all().order_by('-offerprice')
        # print(queryset[0].sid.name)
        
        for i in queryset:
            results.append(
                {
                    'aid': i.id,
                    'sid': i.sid.id,
                    'des': i.des,
                    'buyer': i.buyer.id,
                    'offerprice': i.offerprice,
                    'date': i.date,
                }
            )
        return JsonResponse(results, safe=False, status = 200)
        
class ServiceEndAPI(APIView):
    def get(self, request):
        datasid = request.GET.get('sid')
        tmpService = Service.objects.get(pk = datasid)    
        tmpbuyUser = User.objects.get(id=tmpService.offeruser)
        tmpsellUser = User.objects.get(id=tmpService.uid)
        
        if int(tmpbuyUser.credit) >= int(tmpService.maxval):
            tmpbuyUser.credit -= int(tmpService.maxval)
            tmpsellUser.credit += int(tmpService.maxval)
            
            tmpbuyUser.save()
            tmpsellUser.save()
            
            # 서비스 종료됨
            tmpService.serviceend = True
            tmpService.save()
            return HttpResponse("Success", status = 200)
        else:
            print("잔액 부족. Reject")
            return HttpResponse("Failed. Not Enough Money", status = 400)
        

class SearchServiceByUidAPI(APIView):
    def get(self, request):
        datauid = request.GET.get('uid')
        
        results = []
        queryset = Service.objects.filter(uid = datauid, serviceend = False).all()
        
        print(queryset)
        
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
                    'usecredit': i.usecredit,
                }
            )
            
        return JsonResponse(results, safe=False, status = 200)
    
    
class UsecreditAPI(APIView):
    def get(self, request):
        datauid = request.GET.get('uid')
        datasid = request.GET.get('sid')
        
        tmpUser = User.objects.get(id = datauid)
        tmpService = Service.objects.get(id = datasid)
        
        
        if tmpUser.credit < 500:
            return HttpResponse("Not Enough Money", status = 404)
        else:
            tmpUser.credit -= 500
            tmpService.usecredit += 500
            
            tmpUser.save()
            tmpService.save()
            return HttpResponse("Success", status = 200)
        
        


