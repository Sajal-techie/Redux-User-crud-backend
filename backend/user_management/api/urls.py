
from django.urls import path,include
from . views import getRoutes,MyTokenObtainPairView,UserSignup,Login
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
 


urlpatterns = [
    path('', getRoutes),
    path('token/', Login.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',UserSignup.as_view(),name='signup')
]
