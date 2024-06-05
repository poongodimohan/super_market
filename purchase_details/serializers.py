from rest_framework import serializers
from .models import Product, WeeklyDeal, DailyDeal, Purchase, Bill

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class WeeklyDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyDeal
        fields = '__all__'

class DailyDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyDeal
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
