import pytest
from django.urls import reverse
from django.utils.http import urlencode
from pytest_django.asserts import assertRedirects


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
