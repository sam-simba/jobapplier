from rest_framework.serializers import ModelSerializer
from base.models import Job, Application

class jobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__' 

class applicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__' 
