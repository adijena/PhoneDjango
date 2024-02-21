from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from .serializers import UserSerializer, UserGlobalSerializer, ContactSerializer
from .models import User, UserGlobal, Contact
import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_global_exists = UserGlobal.objects.filter(phone_number=phone_number).exists()

        if not user_global_exists:
            user_global_serializer = UserGlobalSerializer(data=request.data)
            user_global_serializer.is_valid(raise_exception=True)
            user_global_serializer.save()

        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        password = request.data['password']

        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')


        payload = {
            'phone_number': user.phone_number,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(phone_number=payload['phone_number']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class ContactView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        queryset = Contact.objects.all()
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)


class SearchNameView(APIView):
    def get(self, request):
        try:
            token = request.COOKIES.get('jwt')

            if not token:
                raise AuthenticationFailed('Unauthenticated!')

            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            search_query = request.query_params.get('value')

            if not search_query:
                return Response({'detail': 'search query is required'})
            
            start_with_contact = Contact.objects.filter(name__istartswith=search_query)
            contain_contact = Contact.objects.filter(name__icontains=search_query).exclude(name__istartswith=search_query)
            # Concatenate the two querysets
            contact_queryset = start_with_contact | contain_contact
            contact_data = ContactSerializer(contact_queryset, many=True).data


            start_with_global = UserGlobal.objects.filter(name__istartswith=search_query)
            contain_global = UserGlobal.objects.filter(name__icontains=search_query).exclude(name__istartswith=search_query)
            # Concatenate the two querysets
            global_queryset = start_with_global | contain_global
            global_data = ContactSerializer(global_queryset, many=True).data


            merged_data = []
            unique_numbers = set()

            for entry in contact_data:
                number = entry.get('phone_number')
                name = entry.get('name')
                if number not in unique_numbers:
                    merged_data.append({'phone_number': number, 'name': name})
                    unique_numbers.add(number)

            for entry in global_data:
                number = entry.get('phone_number')
                name = entry.get('name')
                if number not in unique_numbers:
                    merged_data.append({'phone_number': number, 'name': name})
                    unique_numbers.add(number)
                    
                    

            if merged_data:              
                return Response({'result':merged_data})
            else:
                return Response({'result': 'No matching data found'})

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except AuthenticationFailed as e:
            return Response({'detail': str(e)})



class SearchNumberView(APIView):
    def get(self, request):
        try:
            token = request.COOKIES.get('jwt')

            if not token:
                raise AuthenticationFailed('Unauthenticated!')

            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            search_query = request.query_params.get('value')

            if not search_query:
                return Response({'detail': 'search query is required'})
            
            start_with_contact = Contact.objects.filter(phone_number__istartswith=search_query)
            contain_contact = Contact.objects.filter(phone_number__icontains=search_query).exclude(phone_number__istartswith=search_query)
            # Concatenate the two querysets
            contact_queryset = start_with_contact | contain_contact
            contact_data = ContactSerializer(contact_queryset, many=True).data


            start_with_global = UserGlobal.objects.filter(phone_number__istartswith=search_query)
            contain_global = UserGlobal.objects.filter(phone_number__icontains=search_query).exclude(phone_number__istartswith=search_query)
            # Concatenate the two querysets
            global_queryset = start_with_global | contain_global
            global_data = ContactSerializer(global_queryset, many=True).data


            merged_data = []
            unique_numbers = set()

            for entry in contact_data:
                number = entry.get('phone_number')
                name = entry.get('name')
                if number not in unique_numbers:
                    merged_data.append({'phone_number': number, 'name': name})
                    unique_numbers.add(number)

            for entry in global_data:
                number = entry.get('phone_number')
                name = entry.get('name')
                if number not in unique_numbers:
                    merged_data.append({'phone_number': number, 'name': name})
                    unique_numbers.add(number)
                    

            if merged_data:              
                return Response({'result':merged_data})
            else:
                return Response({'result': 'No matching data found'})

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except AuthenticationFailed as e:
            return Response({'detail': str(e)})


class MarkSpamView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            number_to_mark = request.data.get('number', None)
            if not number_to_mark:
                return Response({'error': 'Number not provided'})
            user_global_instance = UserGlobal.objects.get(phone_number=number_to_mark)
            user_global_instance.increment_spam_count()
            return Response({'message': 'Number marked as spam successfully'})
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except AuthenticationFailed as e:
            return Response({'detail': str(e)})
        

