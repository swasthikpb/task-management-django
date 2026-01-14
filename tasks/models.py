from django.db import models
from django.conf import settings

class Task(models.Model):

    STATUS_CHOICES = (
        ('PENDING','Pending'),
        ('IN_PROGRESS','In_Progress'),
        ('COMPLETED', 'Completed')
    )

    title = models.CharField(max_length=20)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    due_date  = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default= 'PENDIND')
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title