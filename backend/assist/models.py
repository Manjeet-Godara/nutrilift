from django.db import models
from django.utils import timezone
from accounts.models import Organization, User
from roster.models import Student, Guardian

class Application(models.Model):
    class Source(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        PARENT  = "PARENT", "Parent"

    class Status(models.TextChoices):
        APPLIED   = "APPLIED", "Applied"
        FORWARDED = "FORWARDED", "Forwarded to SAPA"
        # next sprints: APPROVED/REJECTED/CLOSED

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="applications")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="applications")
    guardian = models.ForeignKey(Guardian, on_delete=models.SET_NULL, null=True, blank=True, related_name="applications")

    source = models.CharField(max_length=16, choices=Source.choices, default=Source.PARENT)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.APPLIED)

    form_lang = models.CharField(max_length=12, default="en")
    form_data = models.JSONField(default=dict, blank=True)

    applied_at = models.DateTimeField(default=timezone.now)
    forwarded_at = models.DateTimeField(null=True, blank=True)
    forwarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="forwarded_applications")

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["student", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.student.full_name} – {self.status}"
