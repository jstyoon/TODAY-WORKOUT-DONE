from rest_framework import serializers
from articles.models import Articles,Category,InSubCategory,OutSubCategory
from django.shortcuts import get_object_or_404
from .models import Comment
from datetime import date, timedelta



class ArticlesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Articles
        fields = "__all__"

class ArticleViewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    check_status_count = serializers.SerializerMethodField()
    def get_user(self, obj):
        return {'username': obj.user.username, 'id': obj.user.pk}
    
    def get_check_status_count(self, obj):
        check_count = Articles.objects.filter(check_status=True)
        return check_count.count()


    class Meta:
        model = Articles
        fields = ["user","id","category","check_status","check_status_count","select_day"]


#데이터 직렬화
class SubCategorySerializer(serializers.Field):
    def to_representation(self, value):
        return str(value)  #SubCategory 객체를 문자열로 변환하여 직렬화

    def to_internal_value(self, data):
        return data



class ArticlesCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.ChoiceField(choices=Category.categories)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)
    out_subcategory = SubCategorySerializer(required=False)
    in_subcategory = SubCategorySerializer(required=False)
    

    def validate_out_subcategory(self, value):
        out_subcategory_instance = get_object_or_404(OutSubCategory, out_sub_category=value)
        return out_subcategory_instance
    
    def validate_in_subcategory(self, value):
        in_subcategory_instance = get_object_or_404(InSubCategory, in_sub_category=value)
        return in_subcategory_instance
    
    def get_category(self, obj):
        return obj.category.category

    def validate_category(self, value):
        category_instance = get_object_or_404(Category, category=value)
        return category_instance
    

    def get_user(self, obj):
        return {'username': obj.user.username, 'pk': obj.user.pk}

    class Meta:
        model = Articles
        fields = ["user","category", "content","select_day","exercise_time",
                "image", "check_status", "is_private","in_subcategory",
                "out_subcategory","created_at", "updated_at", "likes", "like_count", "comment_count"]




class ArticlePutSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Category.categories)
    in_subcategory = SubCategorySerializer(required=False)
    out_subcategory = SubCategorySerializer(required=False)

    class Meta:
        model = Articles
        fields = ["category", "select_day", "content", "check_status", "image", "is_private", "in_subcategory", "out_subcategory","exercise_time"]

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        in_subcategory_data = validated_data.pop('in_subcategory', None)
        out_subcategory_data = validated_data.pop('out_subcategory', None)

        if category_data:
            category_instance, _ = Category.objects.get_or_create(category=category_data)
            instance.category = category_instance

        if in_subcategory_data:
            in_subcategory_instance, _ = InSubCategory.objects.get_or_create(in_sub_category=in_subcategory_data)
            instance.in_subcategory = in_subcategory_instance
        else:
            instance.in_subcategory = None 

        if out_subcategory_data:
            out_subcategory_instance, _ = OutSubCategory.objects.get_or_create(out_sub_category=out_subcategory_data)
            instance.out_subcategory = out_subcategory_instance
        else:
            instance.out_subcategory = None
            

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance








class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)
