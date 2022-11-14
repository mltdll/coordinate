import pytest
from django.urls import reverse

from ..models import Employee, Task, TaskType, Position


@pytest.mark.parametrize(
    "model_instance, expected_output",
    [
        pytest.param(
            Position(name="Senior Java Developer"),
            "Senior Java Developer",
            id="`str(Position)` should equal to `Position.name`",
        ),
        pytest.param(
            Employee(
                username="user_1",
                password="7pJy2F0VGzg",
                first_name="User",
                last_name="One",
            ),
            "user_1 (User One)",
            id="`str(User)` should equal to "
            "`f'{User.username} ({User.first_name} {User.last_name})'`",
        ),
        pytest.param(
            TaskType(
                name="Regression testing",
            ),
            "Regression testing",
            id="`str(TaskType)` should equal to `TaskType.name`",
        ),
        pytest.param(
            Task(
                name="Do dishes",
                description="Wash dishes with soap",
                deadline="2022-01-01",
                is_completed="False",
                priority="Urgent",
                task_type=TaskType(name="Chores"),
            ),
            "Do dishes",
            id="`str(Task)` should equal to `Task.name`",
        ),
    ],
)
def test_str_methods(model_instance, expected_output):
    assert str(model_instance) == expected_output


@pytest.mark.parametrize(
    "employee_id",
    [
        pytest.param(1, id="should work for Employee with id 1"),
        pytest.param(3, id="should work for Employee with id other than 1"),
    ],
)
def test_employee_get_absolute_url(employee_id):
    employee = Employee(
        id=employee_id,
        username="user",
        password="7pJy2F0VGzg",
    )

    assert employee.get_absolute_url() == reverse(
        "task_manager:employee-detail", kwargs={"pk": employee_id}
    )
