from django import forms




#유저 데이터 입력 관련 폼(회원가입 시) -> credit을 빼놨음, 나중에 업뎃하는 곳에서는 바꿔나야 할 듯 ㅇㅇ
class UserForm(forms.Form):
    id = forms.CharField(max_length=100)
    name = forms.CharField(max_length=80)
    password = forms.CharField(max_length=80)
    #credit = forms.CharField(max_length=80)

# Login 입력 관련 폼    
class LoginForm(forms.Form):
    id = forms.CharField(max_length=100)
    password = forms.CharField(max_length=80)
    

class ServiceForm(forms.Form):
    uid = forms.CharField()    
    name = forms.CharField(max_length=80)
    des = forms.CharField(max_length=150)
    img = forms.ImageField(required = False)
    option = forms.CharField(max_length=10)
    maxval = forms.CharField()
    offeruser = forms.CharField(required=False)
   
    
    
