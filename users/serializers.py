from django.contrib.auth.models import User

from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'password_mismatch': 'passwords do not match',
    }

    password = serializers.CharField(write_only=True)
    retype_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'retype_password'
        )

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('retype_password'):
            self.fail('password_mismatch')
        else:
            return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        return user

