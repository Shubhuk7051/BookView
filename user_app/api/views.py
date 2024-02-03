from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication


from user_app.api.serializers import RegistrationSerializer
from readers_app.api.permissions import IsAuthenticatedUser


class LogoutView(APIView):
    
    permission_class=[IsAuthenticatedUser]
    authentication_classes = [TokenAuthentication]
    
    
    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
    
@api_view(['POST',])
def registrationview(request):
    
    if request.method=='POST':
        serializer=RegistrationSerializer(data=request.data)
        
        data={}
        
        if serializer.is_valid():
            account=serializer.save()
            
            data['response'] = "Resgistration Successful"
            data['username'] = account.username
            data['email'] = account.email
            
            token=Token.objects.get(user=account).key
            data['token'] = token
            
        else:
            data=serializer.errors
            
        return Response(data, status=status.HTTP_201_CREATED)
             
            

        