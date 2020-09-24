from django.contrib.auth.hashers import PBKDF2PasswordHasher

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated


from core.models import Account
from core.serializers import AccountSerializer


def crypt_code(password):
    gerePass = PBKDF2PasswordHasher()
    passw = gerePass.encode(password, 'seasalt2')
    return passw


class AuthViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer, request, *args, **kwargs):
        return serializer.save(username=request.data["email"], password=crypt_code(request.data["password"]))
    
    def create(self, request, *args, **kwargs):
        if Account.objects.filter(name=request.data["name"], email=request.data["email"]).exists():
            return Response("Usuário já cadastrado.", status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request, *args, **kwargs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request, *args, **kwargs):

        # serializer = AccountSerializer(data=request.data)
        # serializer.is_valid()
        
        if not Account.objects.filter(email=request.data["email"]).exists():
            return Response("Usuário não encontrado.", status=status.HTTP_404_NOT_FOUND)
        
        user = Account.objects.get(email=request.data["email"])
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'email': token.user.email,
            'name': token.user.name,
            'id': token.user.id,
        }, status=status.HTTP_200_OK)

