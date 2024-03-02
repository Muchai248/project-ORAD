# serializers.py
from rest_framework import serializers
from database.models import CustomUser, Document, QCDocument,Site

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email','password', 'is_active', 'date_joined']

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ['title','file', 'uploaded_at' ]


class QCDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCDocument
        fields = ['id', 'document', 'uploaded_at']

class SiteSerializer(serializers.ModelSerializer):
    documents = QCDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Site
        fields = ['name']
        

# class DocumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Document
#         fields = ('id', 'title', 'documents', 'uploaded_at')