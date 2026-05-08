import reflex as rx
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.pages.projects import projects_page
from app.pages.tasks import tasks_page
from app.pages.team import team_page
from app.pages.settings import settings_page
from app.states.auth_state import AuthState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(dashboard_page, route="/dashboard", on_load=AuthState.check_auth)
app.add_page(projects_page, route="/projects", on_load=AuthState.check_auth)
from app.states.task_state import TaskState

app.add_page(
    tasks_page,
    route="/tasks",
    on_load=[AuthState.check_auth, TaskState.load_all_tasks],
)
from app.states.team_state import TeamState

app.add_page(
    team_page,
    route="/team",
    on_load=[AuthState.check_auth, TeamState.load_team],
)
app.add_page(settings_page, route="/settings", on_load=AuthState.check_auth)
from app.pages.project_detail import project_detail_page
from app.states.project_state import ProjectState

app.add_page(
    project_detail_page,
    route="/projects/[project_id]",
    on_load=ProjectState.load_project_detail,
)


def index():
    return rx.el.div(rx.script("window.location.href = '/dashboard';"))


app.add_page(index, route="/")