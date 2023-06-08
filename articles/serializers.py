from rest_framework import serializers
from articles.models import Articles



class ArticlesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Articles
        fields = "__all__"



class ArticlesCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)

    def get_user(self, obj):
        return {'username': obj.user.username, 'pk': obj.user.pk}

    class Meta:
        model = Articles
        fields = ["pk", "user", "category", "content","select_day",
                "image", "check_type",
                "created_at", "updated_at"]


class ArticlePutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articles
        fields = ["category", "select_day", "content","check_type", "image"]



