import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlencode
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from ..models import TaskType, Position, Task


@pytest.mark.parametrize(
    "url",
    {
        pytest.param(
            reverse("task_manager:index"),
            id="index page should not be accessible for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-type-list"),
            id="TaskType list page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-type-create"),
            id="TaskType creation page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-type-update", args=[1]),
            id="TaskType update page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-type-delete", args=[1]),
            id="TaskType delete page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:position-list"),
            id="Position list page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:position-create"),
            id="Position creation page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:position-update", args=[1]),
            id="Position update page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:position-delete", args=[1]),
            id="Position delete page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-list"),
            id="Task list page should not be accessible for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-detail", args=[1]),
            id="Task detail page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-update", args=[1]),
            id="Task update page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-delete", args=[1]),
            id="Task delete page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:task-create"),
            id="Task create page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:toggle-task-assign", args=[1]),
            id="Task assignment view should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:employee-list"),
            id="Employee list page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:employee-detail", args=[1]),
            id="Employee detail page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:employee-create"),
            id="Employee create page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:employee-update", args=[1]),
            id="Employee update page should not be accessible "
            "for unauthorized users",
        ),
        pytest.param(
            reverse("task_manager:employee-delete", args=[1]),
            id="Employee delete page should not be accessible "
            "for unauthorized users",
        ),
    },
)
def test_login_required(url, client):
    """
    Test that all the private views redirect unauthenticated users with
    correct `next` parameter
    """
    response = client.get(url)

    assertRedirects(
        response,
        f"{reverse('login')}?{urlencode({'next': url})}",
        status_code=302,
    )


class TestTaskTypeViews:
    @pytest.mark.django_db
    def test_task_type_list(self, task_type_data, employee_client):
        response = employee_client.get(reverse("task_manager:task-type-list"))
        task_types = TaskType.objects.all()

        assert response.status_code == 200
        assert list(response.context["task_type_list"]) == list(task_types)

    @pytest.mark.django_db
    def test_task_type_template(self, employee_client):
        response = employee_client.get(reverse("task_manager:task-type-list"))

        assertTemplateUsed(response, "task_manager/task_type_list.html")

    @pytest.mark.django_db
    def test_create_task_type(self, employee_client):
        form_data = {"name": "Test1"}

        response = employee_client.post(
            reverse("task_manager:task-type-create"), data=form_data
        )

        assert response.status_code == 302
        assert TaskType.objects.filter(name=form_data["name"]).exists()

    @pytest.mark.django_db
    def test_update_task_type(self, employee_client, task_type_data):
        form_data = {"name": "Extra task"}
        entry_id = 1

        response = employee_client.post(
            reverse("task_manager:task-type-update", args=[entry_id]),
            data=form_data,
        )

        task_type = TaskType.objects.get(pk=entry_id)

        assert response.status_code == 302
        assert task_type.name == form_data["name"]

    @pytest.mark.django_db
    def test_delete_task_type(self, employee_client, task_type_data):
        entry_id = 1

        response = employee_client.post(
            reverse("task_manager:task-type-delete", args=[entry_id])
        )

        assert response.status_code == 302
        assert not TaskType.objects.filter(pk=entry_id).exists()

    @pytest.mark.django_db
    def test_search_task_type(self, employee_client, task_type_data):
        response = employee_client.get(
            reverse("task_manager:task-type-list") + "?name=y"
        )
        task_types = TaskType.objects.filter(name__icontains="y")

        assert list(response.context["task_type_list"]) == list(task_types)


class TestPositionViews:
    @pytest.mark.django_db
    def test_position_list(self, position_data, employee_client):
        response = employee_client.get(reverse("task_manager:position-list"))
        positions = Position.objects.all()

        assert response.status_code == 200
        assert list(response.context["position_list"]) == list(positions)

    @pytest.mark.django_db
    def test_position_template(self, employee_client):
        response = employee_client.get(reverse("task_manager:position-list"))

        assertTemplateUsed(response, "task_manager/position_list.html")

    @pytest.mark.django_db
    def test_create_position(self, employee_client):
        form_data = {"name": "Test1"}

        response = employee_client.post(
            reverse("task_manager:position-create"), data=form_data
        )

        assert response.status_code == 302
        assert Position.objects.filter(name=form_data["name"]).exists()

    @pytest.mark.django_db
    def test_update_position(self, employee_client, position_data):
        form_data = {"name": "Extra task"}
        entry_id = 1

        response = employee_client.post(
            reverse("task_manager:position-update", args=[entry_id]),
            data=form_data,
        )

        position = Position.objects.get(pk=entry_id)

        assert response.status_code == 302
        assert position.name == form_data["name"]

    @pytest.mark.django_db
    def test_delete_position(self, employee_client, position_data):
        entry_id = 3

        response = employee_client.post(
            reverse("task_manager:position-delete", args=[entry_id])
        )

        assert response.status_code == 302
        assert not Position.objects.filter(pk=entry_id).exists()

    @pytest.mark.django_db
    def test_search_position(self, employee_client, position_data):
        response = employee_client.get(
            reverse("task_manager:position-list") + "?name=a"
        )
        positions = Position.objects.filter(name__icontains="a")

        assert list(response.context["position_list"]) == list(positions)


class TestEmployeeViews:
    @pytest.mark.django_db
    def test_employee_list(self, employee_data, employee_client):
        response = employee_client.get(reverse("task_manager:employee-list"))
        employees = get_user_model().objects.all()

        assert response.status_code == 200
        assert list(response.context["employee_list"]) == list(employees)

    @pytest.mark.django_db
    def test_employee_detail(self, employee_data, employee_client):
        employee_id = 1

        response = employee_client.get(
            reverse("task_manager:employee-detail", args=[employee_id])
        )
        employee = get_user_model().objects.get(pk=employee_id)

        assert response.context_data["employee"] == employee

    @pytest.mark.django_db
    def test_employee_template(self, employee_client):
        response = employee_client.get(reverse("task_manager:employee-list"))

        assertTemplateUsed(response, "task_manager/employee_list.html")

    @pytest.mark.django_db
    def test_create_employee(self, employee_client):
        form_data = {
            "username": "test.user",
            "password1": "zLjyFH7qd1icr33e",
            "password2": "zLjyFH7qd1icr33e",
            "first_name": "Test",
            "last_name": "One",
            "position": 1,
        }

        response = employee_client.post(
            reverse("task_manager:employee-create"), data=form_data
        )

        employee = get_user_model().objects.get(username=form_data["username"])

        assert response.status_code == 302
        assert employee.position_id == form_data["position"]
        assert employee.first_name == form_data["first_name"]
        assert employee.last_name == form_data["last_name"]
        assert employee.check_password(form_data["password1"])

    @pytest.mark.django_db
    def test_update_employee(
        self, employee_data, employee_client, position_data
    ):
        form_data = {"position": 3}
        employee_id = 1

        response = employee_client.post(
            reverse("task_manager:employee-update", args=[employee_id]),
            data=form_data,
        )

        employee = get_user_model().objects.get(pk=employee_id)

        assert response.status_code == 302
        assert employee.position_id == form_data["position"]

    @pytest.mark.django_db
    def test_delete_employee(self, employee_client):
        employee_id = 1

        response = employee_client.post(
            reverse("task_manager:employee-delete", args=[employee_id])
        )

        assert response.status_code == 302
        assert not get_user_model().objects.filter(pk=employee_id).exists()

    @pytest.mark.django_db
    def test_search_employee(self, employee_client, employee_data):
        response = employee_client.get(
            reverse("task_manager:employee-list") + "?username=one"
        )
        employees = get_user_model().objects.filter(username__icontains="one")

        assert list(response.context["employee_list"]) == list(employees)


class TestTaskViews:
    @pytest.mark.django_db
    def test_task_list(self, task_data, employee_client):
        response = employee_client.get(reverse("task_manager:task-list"))
        tasks = Task.objects.all()

        assert response.status_code == 200
        assert list(response.context["task_list"]) == list(tasks)

        assertTemplateUsed(response, "task_manager/task_list.html")

    @pytest.mark.django_db
    def test_task_detail(self, task_data, employee_client):
        task_id = 1

        response = employee_client.get(
            reverse("task_manager:task-detail", args=[task_id])
        )
        task = Task.objects.get(pk=task_id)

        assert response.context_data["task"] == task

    @pytest.mark.django_db
    def test_task_type_template(self, employee_client):
        response = employee_client.get(reverse("task_manager:task-list"))

        assertTemplateUsed(response, "task_manager/task_list.html")

    @pytest.mark.django_db
    def test_create_task(self, task_type_data, employee_data, employee_client):
        form_data = {
            "name": "Test Task 12",
            "description": "description",
            "deadline": "2022-11-12",
            "is_completed": False,
            "priority": "ME",
            "task_type": 1,
            "assignees": [1, 2],
        }

        response = employee_client.post(
            reverse("task_manager:task-create"), data=form_data
        )

        assert response.status_code == 302

        task = Task.objects.get(name=form_data["name"])

        assert task.name == form_data["name"]
        assert task.task_type.id == form_data["task_type"]
        assert [employee.id for employee in task.assignees.all()] == form_data[
            "assignees"
        ]

    @pytest.mark.django_db
    def test_update_task(self, task_data, employee_client):
        form_data = {
            "name": "TT51",
            "description": "description",
            "deadline": "2322-01-04",
            "is_completed": True,
            "priority": "LO",
            "task_type": 1,
            "assignees": 2,
        }
        task_id = 1

        response = employee_client.post(
            reverse("task_manager:task-update", args=[task_id]), data=form_data
        )

        assert response.status_code == 302

        task = Task.objects.get(pk=task_id)

        assert task.name == form_data["name"]
        assert task.task_type.id == form_data["task_type"]
        assert task.assignees.get().id == form_data["assignees"]

    @pytest.mark.django_db
    def test_delete_task(self, task_data, employee_client):
        task_id = 1

        response = employee_client.post(
            reverse("task_manager:task-delete", args=[task_id])
        )

        assert response.status_code == 302
        assert not Task.objects.filter(pk=task_id).exists()

    @pytest.mark.django_db
    def test_search_tasks(self, task_data, employee_client):
        response = employee_client.get(
            reverse("task_manager:task-list") + "?name=fea"
        )
        tasks = Task.objects.filter(name__icontains="fea")

        assert list(response.context["task_list"]) == list(tasks)

    @pytest.mark.django_db
    def test_assign_to_task(self, task_data, employee_client):
        task_id = 1

        response_add = employee_client.get(
            reverse("task_manager:toggle-task-assign", args=[task_id])
        )

        task = Task.objects.prefetch_related("assignees").get(pk=task_id)
        user = response_add.wsgi_request.user

        assert response_add.status_code == 302
        assert user in task.assignees.all()

        # And now the other way, using the WET design principle.
        response_remove = employee_client.get(
            reverse("task_manager:toggle-task-assign", args=[task_id])
        )

        task.refresh_from_db()

        assert response_remove.status_code == 302
        assert user not in task.assignees.all()
