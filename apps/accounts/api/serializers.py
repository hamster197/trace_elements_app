from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer


user_fields = ('pk',  'last_name', 'first_name',  'patronymic', 'email', 'phone', 'male', 'female',
          'date_of_birth', )

class UserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = user_fields

class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = user_fields + ('password',)



