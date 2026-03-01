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

    @classmethod
    def ensure_upcoming_slots(cls, days=7):
        """Generate delivery slots for the next `days` days and return a
        queryset of available slots.
        """
        from datetime import date, time, timedelta

        today = date.today()
        for i in range(days):
            slot_date = today + timedelta(days=i + 1)
            for slot_type, start, end in [
                ('morning', time(9, 0), time(12, 0)),
                ('evening', time(17, 0), time(20, 0)),
            ]:
                cls.objects.get_or_create(
                    delivery_date=slot_date,
                    slot_type=slot_type,
                    start_time=start,
                    defaults={
                        'end_time': end,
                        'max_orders': 50,
                        'is_available': True,
                    }
                )
        return cls.objects.filter(
            delivery_date__gte=today,
            is_available=True
        ).order_by('delivery_date', 'start_time')
