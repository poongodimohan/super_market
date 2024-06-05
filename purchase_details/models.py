from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.CharField(max_length=255, blank=True, null=True)
    is_weekly_deal = models.BooleanField(default=False)
    is_daily_deal = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class WeeklyDeal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)

class DailyDeal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Reduce the product quantity
        self.product.quantity -= self.quantity
        self.product.save()

        # Apply discounts if applicable
        self.total_price = self.quantity * self.purchase_price
        if self.product.is_daily_deal:
            daily_deal = DailyDeal.objects.get(product=self.product)
            self.discount_applied = (self.purchase_price - daily_deal.discount_price) * self.quantity
            self.total_price = daily_deal.discount_price * self.quantity
        elif self.product.is_weekly_deal:
            weekly_deal = WeeklyDeal.objects.get(product=self.product)
            self.discount_applied = (self.purchase_price - weekly_deal.discount_price) * self.quantity
            self.total_price = weekly_deal.discount_price * self.quantity

        super().save(*args, **kwargs)

class Bill(models.Model):
    BILL_PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_quarter', 'Half Quarter'),
        ('three_quarter', 'Three Quarter'),
        ('yearly', 'Yearly'),
    ]

    period = models.CharField(max_length=20, choices=BILL_PERIOD_CHOICES)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=15, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    def calculate_final_amount(self):
        if self.total_amount >= 10000:
            self.discount = self.total_amount * 0.10
        elif self.total_amount >= 5000:
            self.discount = self.total_amount * 0.05
        self.final_amount = self.total_amount - self.discount

    def save(self, *args, **kwargs):
        self.calculate_final_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.period.capitalize()} Bill - {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}"
