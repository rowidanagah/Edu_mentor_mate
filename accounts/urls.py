from django.urls import path ,include
from . import views
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
	path('register', views.UserRegister.as_view(), name='register'),
	# path('login', views.UserLogin.as_view(), name='login'),
	path('update', views.UpdateUser.as_view(), name='update'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
  path('user/<int:pk>/', views.get_specific_user, name='get_user'),
#  path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
path('dj-rest-auth/', include('dj_rest_auth.urls')),
 path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
 path('dj-rest-auth/registration/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent')
]	
