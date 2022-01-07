from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('', views.getUsers, name='getUsers'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('forgotpassword/', views.forgotPassword, name='forgotPassword'),
    path('register/', views.registerUser, name='registerUser'),
    path('<str:pk>/', views.getUserByID, name='getUserById'),
    path('profile/update/', views.updateUserProfile, name='updateUserProfile'),
    path('delete/<str:pk>/', views.deleteUser, name='deleteUser')
]
