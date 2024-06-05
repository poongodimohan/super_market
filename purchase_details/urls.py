from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, WeeklyDealViewSet, DailyDealViewSet, BillViewSet,PurchaseViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('weekly-deals', WeeklyDealViewSet)
router.register('daily-deals', DailyDealViewSet)
router.register('purchases', PurchaseViewSet)
router.register('bills', BillViewSet)

urlpatterns = [
    
    path('', include(router.urls)),
]
