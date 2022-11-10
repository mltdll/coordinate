from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="employees"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


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
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(Employee, related_name="tasks")

    def __str__(self) -> str:
        return f"[{self.priority}] {self.name}"
