from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from base.email import send_reset_password_email
import random
import string
from base.serializers import UserSerializer, UserSerializerWithToken


from base.models import NewUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
      data = super().validate(attrs)

      serializer = UserSerializerWithToken(self.user).data

      for k, v in serializer.items():
        data[k] = v

      return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
  data=request.data
  try:
    user = NewUser.objects.create(
      user_name = data['username'],
      email = data['email'],
      password = make_password(data['password'])
    )
    serializer = UserSerializerWithToken(user, many=False)
    
    return Response(serializer.data)
  except:
    message = {'detail':'User with this email or username already exist'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUsers(request):
  users = NewUser.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response({"user":serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserByID(request, pk):
  user = NewUser.objects.get(id=pk)
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
  user= request.user
  serializer = UserSerializerWithToken(user, many=False)
  data = request.data
  user.user_name = data['username']
  user.about = data['about']
  if data['password'] != '':
    user.password = make_password(data['password'])
  user.save()
  return Response(serializer.data)

@api_view(['POST'])
def forgotPassword(request):
  lower = string.ascii_lowercase
  upper = string.ascii_uppercase
  num = string.digits
  all = lower + upper + num
  temp = random.sample(all, 6)
  password = "".join(temp)
  print(password)
  email = request.data['email']
  try:
    user = NewUser.objects.get(email=email)
    user.password = make_password(password)
    user.save()
    send_reset_password_email(user.user_name, user.email, password) 
    message = {'detail':'Your new password has been sent your email'}
    return Response(message, status=status.HTTP_200_OK )
  except:
    message = {'detail':'User does not exist'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST )
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
  try:
    user = NewUser.objects.get(id=pk)
    user.delete()
    return Response('User was deleted successfully')
  except:
    message = {'detail':'User does not exist'}
    return Response(message, status=status.HTTP_400_BAD_REQUEST )
