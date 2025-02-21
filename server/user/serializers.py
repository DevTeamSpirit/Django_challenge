from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import get_eth_balance


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password", "password2", "wallet_address")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            wallet_address = self.validated_data["wallet_address"]
        )

        print(f"wallet address is : {user.wallet_address}")

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})
        
        if user.wallet_address:
            try:
                balance = get_eth_balance(user.wallet_address)
                print(balance)
            except Exception as e:
                raise serializers.ValidationError({'wallet address': str(e)})
        else:
            raise serializers.ValidationError({'wallet address': 'No wallet address provided'})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    eth_balance = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "first_name", "last_name", "eth_balance")

    def get_eth_balance(self, obj):
        return get_eth_balance(obj.wallet_address)