from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    '''Serializer to get and update a user's details.'''

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']
        

class CreateAccountSerializer(serializers.ModelSerializer):
    ''' Serializer to create new user '''

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ['id']        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        '''Account creation validation function'''

        if data['password'] != data['password2']:
            raise serializers.ValidationError({'error': 'Your passwords do not match'}, code=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'}, code=status.HTTP_400_BAD_REQUEST)
        
        validate_password(data['password'])
        
        return data
    
    def create(self, validated_data):
        '''Account creation function'''
        
        password = validated_data.get('password')
        validated_data.pop('password2')

        account = User.objects.create(**validated_data)
        account.set_password(raw_password=password)
        account.save()
        
        Token.objects.create(user=account)
        
        return account
    

class LoginSerializer(serializers.Serializer):
    '''Serializer to log in a user.'''

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, data):
        '''Authentication validation function'''

        user = authenticate(email=data['email'], password=data['password'])

        if user is None:
            raise serializers.ValidationError({'error': 'Invalid credentials'}, code=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_verified:
            raise serializers.ValidationError({'error': 'Email is not verified'}, code=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            raise serializers.ValidationError({'error': 'This user is not active'}, code=status.HTTP_400_BAD_REQUEST)
        
        token = Token.objects.get_or_create(user=user)
        
        data['message'] = f'Welcome {data["email"]}'
        data['token'] = token[0].key

        return data


class UserDetailsSerializer(serializers.ModelSerializer):
    '''Serializer to get and update a user's details.'''

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'is_verified', 'is_active']
    
    def update(self, instance, validated_data):
        '''Update details function'''

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
    

class ChangePasswordSerializer(serializers.Serializer):
    '''Serializer to change user password.'''

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        old_password = data.get('password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        user = authenticate(email=email, password=old_password)
        current_user = self.context['request'].user

        if user is None or user.email != current_user.email:
            raise serializers.ValidationError({'error': 'Invalid credentials'}, code=status.HTTP_400_BAD_REQUEST)
        if old_password == new_password:
            raise serializers.ValidationError({'error': 'New password cannot be the same as old password.'}, code=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            raise serializers.ValidationError({'error': 'New password and confirm password must match.'}, code=status.HTTP_400_BAD_REQUEST)
        
        validate_password(new_password)
        return data
    
    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()

        return instance
