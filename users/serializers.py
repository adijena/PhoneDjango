from rest_framework import serializers
from .models import User, UserGlobal, Contact
import jwt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class UserGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGlobal
        fields = ['name', 'phone_number', 'email', 'spam']

class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    phone_number = serializers.CharField(max_length=15)

    class Meta:
        model = Contact
        fields = ['user', 'name', 'phone_number', 'email']
