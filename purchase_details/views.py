from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, WeeklyDeal, DailyDeal, Purchase, Bill
from .serializers import (ProductSerializer, 
                          WeeklyDealSerializer,
                            DailyDealSerializer, 
                            PurchaseSerializer, 
                            BillSerializer)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class WeeklyDealViewSet(viewsets.ModelViewSet):
    queryset = WeeklyDeal.objects.all()
    serializer_class = WeeklyDealSerializer

class DailyDealViewSet(viewsets.ModelViewSet):
    queryset = DailyDeal.objects.all()
    serializer_class = DailyDealSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        serializer.save()
        # Adjust product quantity and total price within the save method of the Purchase model

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    @action(detail=False, methods=['post'])
    def generate_bill(self, request):
        period = request.data.get('period')
        total_amount = sum(purchase.total_price for purchase in Purchase.objects.all())
        bill = Bill.objects.create(period=period, total_amount=total_amount)
        bill.save()
        serializer = self.get_serializer(bill)
        return Response(serializer.data)
