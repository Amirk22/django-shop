from rest_framework import serializers

from core.models import Banner, Slider, ListFooter


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'

class ListFooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListFooter
        fields = '__all__'


