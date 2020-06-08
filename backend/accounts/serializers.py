from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='accounts:accounts-detail',
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['url', 'id', 'user', 'description', 'created_at', 'updated_at', 'is_manager', 'want_to_be_manager']
        read_only_fields = ['url','id','is_manager', 'created_at']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        ## This data variable will contain refresh and access tokens
        data = super().validate(attrs)
        ## You can add more User model's attributes like username,email etc. in the data dictionary like this.
        data['username'] = self.user.username
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['is_manager'] = self.user.profile.is_manager
        data['is_superuser'] = self.user.is_superuser
        data['want_to_be_manager'] = self.user.profile.want_to_be_manager
        return data
