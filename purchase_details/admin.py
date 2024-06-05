from django.contrib import admin

from .models import Product,WeeklyDeal,DailyDeal,Purchase,Bill

admin.site.register([Product,
                     WeeklyDeal,
                     DailyDeal,
                     Purchase,
                     Bill])
