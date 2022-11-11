import pytest

from ..models import Employee, Position, Task, TaskType


@pytest.fixture
def task_type_data():
    data = [
        "Bug",
        "Feature request",
    ]

    for name in data:
        TaskType.objects.create(name=name)


@pytest.fixture
def position_data():
    data = [
        "Intern",
        "Senior Python Developer",
    ]

    for name in data:
        Position.objects.create(name=name)


@pytest.fixture
def employee_data(position_data):
    data = [
        {
            "username": "user_1",
            "password": "zLjyFH7qd1icr33e",
            "first_name": "User",
            "last_name": "One",
            "position_id": "1",
        },
        {
            "username": "user_2",
            "password": "xFRKQuyqRa4pAs2t",
            "first_name": "User",
            "last_name": "Two",
            "position_id": "2",
        },
        {
            "username": "user_3",
            "password": "ilV5uG1y7UEkSowR",
            "first_name": "User",
            "last_name": "Three",
            "position_id": "1",
        },
    ]

    for user_data in data:
        Employee.objects.create_user(**user_data)


@pytest.fixture
def task_data(task_type_data, employee_data):
    data = [
        (
            {
                "name": "Test bug 1",
                "description": "Test bug 1",
                "deadline": "2023-05-05",
                "is_completed": False,
                "priority": "Trivial",
                "task_type_id": 1,
            },
            1,
        ),
        (
            {
                "name": "Test feature 1",
                "description": "Test feature 1",
                "deadline": "2015-01-05",
                "is_completed": True,
                "priority": "High",
                "task_type_id": 2,
            },
            [2, 3],
        ),
        (
            {
                "name": "Test bug 2",
                "description": "Test bug 2",
                "deadline": "2022-12-01",
                "is_completed": False,
                "priority": "Urgent",
                "task_type_id": 1,
            },
            [1, 2, 3],
        ),
    ]

    for task_data, employee_ids in data:
        car = Task.objects.create(**task_data)
        car.drivers.set(employee_ids)


@pytest.fixture
def employee_client(client):
    employee = Employee.objects.create_user(
        username="test.client",
        password="zLjyFH7qd1icr33e",
        first_name="Client",
        last_name="Test",
        position=Position.objects.create(name="Test subject"),
    )
    client.force_login(employee)

    return client
