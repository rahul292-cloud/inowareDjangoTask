from rest_framework import serializers
from django.contrib.auth.models import User
from dashboard.models import RegisterUser
import re


class RegisterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='name')
    userName = serializers.CharField(label='userName')

    email = serializers.EmailField(label='Email Address')

    password = serializers.CharField(label='password')
    photo = serializers.FileField(label='photo')

    def validate_password(self, value):

        """Validates that a password is as least 8 characters long and has at least
            2 digits and 1 Upper case letter.
            """
        msg = 'Note: password is as least 8 characters long and has at least 2 digits and 1 Upper case letter'
        min_length = 8

        if len(value) < min_length:
            raise serializers.ValidationError('Password must be at least {0} characters '
                                              'long.'.format(min_length) + msg)

        # check for 2 digits
        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits.' + msg)

        # check for uppercase letter
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter.' + msg)

        return value

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):

            return value
        raise serializers.ValidationError("invalid Email id")

    def validate_userName(self, value):
        data = self.get_initial()
        userName = data.get("userName")

        username_qs = User.objects.filter(username=userName)
        if username_qs.exists():
            raise serializers.ValidationError("username already exists")
        else:
            return value



    def create(self, validated_data):

        user = RegisterUser.objects.create(
            userName=validated_data['userName'],
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            photo=validated_data['photo']
        )

        return validated_data

    class Meta:
        model = RegisterUser
        fields = ('name', 'userName', 'photo', 'email', 'password')


class userDetailsSerializers(serializers.ModelSerializer):
    photo = serializers.FileField(label='photo')
    class Meta:
        model=RegisterUser
        fields=('name', 'photo')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()

        return instance

