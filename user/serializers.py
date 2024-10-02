from django.contrib.auth import get_user_model , authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'username']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data):
        #create and return user with encrypted pass
        user = User.objects.create_user(**validated_data)
        return user

    def update(self,instance,validated_data):
        #update and return user profile
        password = validated_data.pop('password',None)
        user = super().update(instance,validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, data):
        #validate and authenticate the user
        email= data['email']
        password= data['password']
        user= authenticate(
            request= self.context.get('request'),
            username= email,
            password= password
        )

        if not user:
            msg = _('unable to authenticate with those given credentials.')
            raise serializers.ValidationError(msg, code='autherization')

        data['user']= user
        return data

