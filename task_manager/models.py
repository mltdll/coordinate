from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="employees"
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("task_manager:employee-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    URGENT = "UR"
    HIGH = "HI"
    MEDIUM = "ME"
    LOW = "LO"
    TRIVIAL = "TR"

    PRIORITY_CHOICES = [
        (URGENT, "Urgent"),
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
        (TRIVIAL, "Trivial"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="tasks"
    )

    class Meta:
        ordering = ["is_completed", "deadline"]

    def toggle_completed(self):
        self.is_completed = not self.is_completed
        self.save()

    def __str__(self) -> str:
        return f"{self.name}"
