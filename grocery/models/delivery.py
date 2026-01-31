from django.db import models

class DeliverySlot(models.Model):
    slot_type = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning (9 AM - 12 PM)'),
            ('evening', 'Evening (5 PM - 8 PM)'),
        ]
    )
    delivery_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_orders = models.PositiveIntegerField(default=50)
    current_orders = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)


    class Meta:
        ordering = ['delivery_date', 'start_time']

    @property
    def is_full(self):
        return self.current_orders >= self.max_orders

    def __str__(self):
        return f"{self.slot_type.capitalize()} - {self.delivery_date}"