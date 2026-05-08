import reflex as rx
from app.states.auth_state import AuthState
import logging


class ProjectState(AuthState):
    projects: list[dict[str, str | int]] = []
    search_query: str = ""
    status_filter: str = "all"
    view_mode: str = "grid"
    show_create_modal: bool = False
    show_edit_modal: bool = False
    show_delete_modal: bool = False
    form_name: str = ""
    form_description: str = ""
    form_status: str = "active"
    form_due_date: str = ""
    form_error: str = ""
    editing_project_id: str = ""
    deleting_project_id: str = ""
    selected_project: dict[str, str | int] = {}
    project_tasks: list[dict[str, str]] = []

    @rx.var
    def filtered_projects(self) -> list[dict[str, str | int]]:
        res = self.projects
        if self.search_query:
            res = [
                p
                for p in res
                if self.search_query.lower() in str(p.get("name", "")).lower()
            ]
        if self.status_filter != "all":
            res = [p for p in res if p.get("status") == self.status_filter]
        return res

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status

    @rx.event
    def set_view_mode(self, mode: str):
        self.view_mode = mode

    @rx.event
    def open_create_modal(self):
        self.form_name = ""
        self.form_description = ""
        self.form_status = "active"
        self.form_due_date = ""
        self.form_error = ""
        self.show_create_modal = True

    @rx.event
    def close_modals(self):
        self.show_create_modal = False
        self.show_edit_modal = False
        self.show_delete_modal = False

    @rx.event
    async def load_projects(self):
        self.projects = [
            {
                "id": "1",
                "name": "Website Redesign",
                "description": "Revamp the main corporate website.",
                "status": "active",
                "task_count": 12,
                "completed_tasks": 5,
                "due_date": "2024-12-01",
            },
            {
                "id": "2",
                "name": "Mobile App Launch",
                "description": "Prepare for iOS and Android release.",
                "status": "on_hold",
                "task_count": 24,
                "completed_tasks": 20,
                "due_date": "2024-10-15",
            },
        ]

    @rx.event
    async def load_project_detail(self):
        project_id = self.router.page.params.get("project_id", "")
        if project_id == "1":
            self.selected_project = {
                "id": "1",
                "name": "Website Redesign",
                "description": "Revamp the main corporate website.",
                "status": "active",
            }
            self.project_tasks = [
                {
                    "id": "t1",
                    "title": "Design mockups",
                    "status": "todo",
                    "priority": "high",
                    "assignee": "Alice",
                },
                {
                    "id": "t2",
                    "title": "Setup repo",
                    "status": "done",
                    "priority": "medium",
                    "assignee": "Bob",
                },
            ]

    @rx.event
    async def create_project(self):
        self.form_error = ""
        if not self.form_name or len(self.form_name.strip()) < 3:
            self.form_error = "Project name must be at least 3 characters."
            return
        import secrets

        self.projects.append(
            {
                "id": secrets.token_hex(8),
                "name": self.form_name.strip(),
                "description": self.form_description.strip(),
                "status": self.form_status,
                "due_date": self.form_due_date,
                "task_count": 0,
                "completed_tasks": 0,
            }
        )
        self.show_create_modal = False
        yield rx.toast("Project created successfully!")

    @rx.event
    def open_edit_modal(self, project: dict):
        self.editing_project_id = str(project.get("id", ""))
        self.form_name = str(project.get("name", ""))
        self.form_description = str(project.get("description", ""))
        self.form_status = str(project.get("status", "active"))
        self.form_due_date = str(project.get("due_date", ""))
        self.form_error = ""
        self.show_edit_modal = True

    @rx.event
    async def update_project(self):
        self.form_error = ""
        if not self.form_name or len(self.form_name.strip()) < 3:
            self.form_error = "Project name must be at least 3 characters."
            return
        for p in self.projects:
            if p.get("id") == self.editing_project_id:
                p["name"] = self.form_name.strip()
                p["description"] = self.form_description.strip()
                p["status"] = self.form_status
                p["due_date"] = self.form_due_date
                break
        self.show_edit_modal = False
        yield rx.toast("Project updated successfully!")

    @rx.event
    def open_delete_modal(self, project_id: str):
        self.deleting_project_id = project_id
        self.show_delete_modal = True

    @rx.event
    async def delete_project(self):
        self.projects = [
            p for p in self.projects if p.get("id") != self.deleting_project_id
        ]
        self.show_delete_modal = False
        yield rx.toast("Project deleted successfully!")