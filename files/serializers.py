# turn python object into JSON
from rest_framework import serializers
from .models import File
from django.contrib.auth.models import User

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        
    def create(self, validated_data):
        # return File.objects.create(user=self.context['request'].user, **validated_data)
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('passworkd',)
        read_only_fields = ('id',)
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user
        
            
