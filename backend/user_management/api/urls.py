
from django.urls import path,include
from . views import getRoutes,UserSignup,Login,UserDetails,UserList
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', getRoutes),
    path('token/', Login.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',UserSignup.as_view(),name='signup'),
    path('user_details/<int:id>/',UserDetails.as_view(),name='user_details'),
    path('user_list/',UserList.as_view(),name='user_list'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 