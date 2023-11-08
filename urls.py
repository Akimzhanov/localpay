from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, Token, check_pay, abon_pay, personal,pay_info
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()

router.register('user',UserViewSet,'user')

urlpatterns = [
    path('login/', Token.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check_pay/', check_pay, name='check_pay'),
    path('abon_pay/',abon_pay, name='abon_pay'),
    path('personal/',personal, name='personal'),
    path('pay_info/',pay_info, name='pay_info'), 
]
urlpatterns += router.urls


