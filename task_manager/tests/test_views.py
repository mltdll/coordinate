import pytest
from django.urls import reverse
from django.utils.http import urlencode
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from ..models import TaskType


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
