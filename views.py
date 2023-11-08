from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import api_view
from django.utils import timezone
from django.shortcuts import render, redirect
from rest_framework import permissions
from rest_framework import views
import requests
import asyncio 
from rest_framework import status

from datetime import datetime
import json
from bs4 import BeautifulSoup
from django.http import HttpResponse,  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import User_mon, Pays
from .serializers import UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class UserViewSet(ModelViewSet):
    queryset = User_mon.objects.all()
    serializer_class = UserSerializer

    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class Token(TokenObtainPairView):
    pass
  
    

async def check_ls(ls):
        url =f'' #ссылка на api локального платежа
        x = requests.post(url)
        x.encoding = 'utf-8'
        try:
            soup = BeautifulSoup(x.text, features="xml" )
            abon = soup.find('fio').string
            status = soup.find('result').string
            result = {
           'fio': abon,
           'status': status }

        except:
            soup = BeautifulSoup(x.text, features="xml" )
            comment = soup.find('comment').string
            status = soup.find('result').string

            result = {
           'comment': comment,
           'status': status }
        
        return  JsonResponse(result)





@csrf_exempt
def check_pay(request):
     if request.method == 'POST':
        post_data = request.POST.copy()
        ls = post_data.get('ls')
        a = asyncio.run(check_ls(ls))
        

        return HttpResponse(a)

     else:
        return HttpResponse(500)


async def abon_pay2(ls,money, login):
        mont_data = User_mon.objects.all().filter(login=login).first() 
        id = mont_data.id
        name = mont_data.name
        surname = mont_data.surname
        balance = mont_data.balance 
        region = mont_data.region
        avail_balance = mont_data.avail_balance
        password = mont_data.login
        access = mont_data.access



        ls = int(ls)
        moneys = float(money) 
        print(type(moneys))
        now = datetime.now()
        service_id_hydra = now.strftime("%Y%m%d%H%M%S")
        time = datetime.now()
        time = str(time)[:-4]
        txn_id=service_id_hydra+str(ls)
        if int(balance) < int(money) or access == False: 
            return HttpResponse('У вас недостаточно средств для оплаты или отсутствует доступ к оплате')
        else:
            urls = f'' #ссылка на api для пополнения счета у абонента
            x = requests.post(urls)
            x.encoding = 'utf-8'
            time2 = datetime.now()
            time2 = str(time2)[:-4]

           
            try:
                soup = BeautifulSoup(x.text, features="xml" )
                osmp_txn_id = soup.find('osmp_txn_id').string
                comment = soup.find('comment').string
                sum = soup.find('sum').string
                status = soup.find('result').string
                result = {
               'osmp_txn_id': osmp_txn_id,
               'sum': sum,
               'comment ':comment ,
               'status': status }
            except:
                soup = BeautifulSoup(x.text, features="xml" )
                osmp_txn_id = soup.find('osmp_txn_id').string
                sum = soup.find('sum').string
                status = soup.find('result').string
                result = {
               'osmp_txn_id': osmp_txn_id,
               'sum': sum,
               'status': status }

            if status == '0':
                b = 'Выполнен'
                a = Pays.objects.create(number_payment=osmp_txn_id, date_payment=time, accept_payment=time2, ls_abon=ls, money=sum, status_payment=b, user_id=id )
                a.save()
    
            x = str(sum)
            y = x[:-2]
            sum = int(y)
            if status == '0':
      
      
               balance2 = int(balance) - sum
               avail_balance2 = int(avail_balance) - sum
               mont_info_update = User_mon.objects.get(id=id)
               mont_info_update.balance = balance2
               mont_info_update.avail_balance = avail_balance2
               mont_info_update.save(update_fields=['balance', 'avail_balance'])





            return  JsonResponse(result)


@csrf_exempt
def abon_pay(request):
     if request.method == 'POST':
        post_data = request.POST.copy()
        ls = post_data.get('ls')
        money = post_data.get('money')
        login = post_data.get('login')
        a = asyncio.run(abon_pay2(ls, money, login))

        return HttpResponse(a)

     else:
        return HttpResponse(500)



async def personal_infa(login):
    mont_data = User_mon.objects.all().filter(login=login).first()
    name = mont_data.name
    surname = mont_data.surname
    balance = mont_data.balance 
    region = mont_data.region
  
    result = {
     'surname': surname,
     'name': name,
     'region': region ,
     'balance': balance 
}
    return  JsonResponse(result)



@csrf_exempt
def personal(request):
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        login = post_data['login']
        a = asyncio.run(personal_infa(login))

        return HttpResponse(a)

    else:
        return HttpResponse(500)


async def pay_check(login):
    user = User_mon.objects.all().filter(login=login).first()
    user_id = user.name
    format= '%Y-%m'
    time_pay = datetime.now().strftime(format)

    hystory = Pays.objects.all().filter(user_id=user)
    ls = hystory.values_list('accept_payment','ls_abon', 'money', 'status_payment')
    items = []
    test = 0
    for item in ls:
        data_check = item[0]
        if data_check[:7] == time_pay:
            test = test + 1
            print(test)
            items.append(item)


    result = {
    'data': items,
    'count': test
}
    return  JsonResponse(result)

@csrf_exempt
def pay_info(request):
    if request.method == 'POST':
        pay_data = request.POST.copy()
        login = pay_data['login']
        a = asyncio.run(pay_check(login))

        return HttpResponse(a)

    else:
        return HttpResponse(500)






async def personal_infa(login):
    mont_data = User_mon.objects.all().filter(login=login).first()
    name = mont_data.name
    surname = mont_data.surname
    balance = mont_data.balance 
    region = mont_data.region
  
    result = {
     'surname': surname,
     'name': name,
     'region': region ,
     'balance': balance 
}
    return  JsonResponse(result)





