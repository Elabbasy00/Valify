from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout
from business_logic.exceptions.exceptions import NotFound
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from .logic import authenticate_user


class UserRegister(APIView):
    '''
        Create User with password & public key
        return user private key 
    '''
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        data = request.data  # leave validation to serializer
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            _, privateKey = serializer.save()  # _ = user obj
            return Response({"private_key": privateKey}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = (SessionAuthentication,)

    def post(self, request, format=None):
        '''
            Logged User In 
            @params Email, Password
            validation -> serializer_class
            raise ->  user not found
        '''
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                user = authenticate_user(data)
                login(request, user)
                return Response({"user_id": user.id}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except NotFound as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format=None):
        logout(request)
        return Response({"Logged Out !"}, status=status.HTTP_200_OK)
