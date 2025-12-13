from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("این کاربر قبلا ثبت نام کرده است")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "کلمه عبور و تکرار کلمه عبور مغایرت دارند"})
        return data

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    code = serializers.CharField(max_length=5, min_length=5)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("این کاربر ثبت‌نام نکرده است")
        return value

class ForgotPasswordCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    code = serializers.CharField(max_length=5, min_length=5)

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "کلمه عبور و تکرار کلمه عبور مغایرت دارند"})
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

