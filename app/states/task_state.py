import reflex as rx
from app.states.auth_state import AuthState
import logging


class TaskState(AuthState):
    all_tasks: list[dict[str, str]] = []
    search_query: str = ""
    status_filter: str = "all"
    priority_filter: str = "all"
    sort_by: str = "newest"
    show_create_task_modal: bool = False
    show_edit_task_modal: bool = False
    show_delete_task_modal: bool = False
    task_title: str = ""
    task_description: str = ""
    task_status: str = "todo"
    task_priority: str = "medium"
    task_assignee_id: str = ""
    task_project_id: str = ""
    task_due_date: str = ""
    task_error: str = ""
    editing_task_id: str = ""
    deleting_task_id: str = ""
    available_projects: list[dict[str, str]] = []
    available_users: list[dict[str, str]] = []

    @rx.var
    def filtered_tasks(self) -> list[dict[str, str]]:
        res = self.all_tasks
        if self.search_query:
            res = [
                t
                for t in res
                if self.search_query.lower() in str(t.get("title", "")).lower()
            ]
        if self.status_filter != "all":
            res = [t for t in res if t.get("status") == self.status_filter]
        if self.priority_filter != "all":
            res = [t for t in res if t.get("priority") == self.priority_filter]
        return res

    @rx.event
    async def load_all_tasks(self):
        if not self.is_authenticated:
            return
        if not self.all_tasks:
            self.all_tasks = [
                {
                    "id": "1",
                    "title": "Setup database schemas",
                    "status": "done",
                    "priority": "critical",
                    "project_name": "Website Redesign",
                    "assignee_name": "Alice",
                    "due_date": "2024-01-01",
                },
                {
                    "id": "2",
                    "title": "Design authentication flow",
                    "status": "in_progress",
                    "priority": "high",
                    "project_name": "Mobile App Launch",
                    "assignee_name": "Bob",
                    "due_date": "2024-02-01",
                },
            ]

    @rx.event
    async def load_task_form_data(self):
        self.available_projects = [
            {"id": "1", "name": "Website Redesign"},
            {"id": "2", "name": "Mobile App Launch"},
        ]
        self.available_users = [
            {"id": "u1", "name": "Alice"},
            {"id": "u2", "name": "Bob"},
        ]

    @rx.event
    async def open_create_task_modal(self):
        self.task_title = ""
        self.task_description = ""
        self.task_status = "todo"
        self.task_priority = "medium"
        self.task_assignee_id = ""
        self.task_project_id = ""
        self.task_due_date = ""
        self.task_error = ""
        self.show_create_task_modal = True
        yield TaskState.load_task_form_data

    @rx.event
    async def create_task(self):
        self.task_error = ""
        if not self.task_title or len(self.task_title.strip()) < 3:
            self.task_error = "Task title must be at least 3 characters."
            return
        if not self.task_project_id:
            self.task_error = "Please select a project."
            return
        import secrets

        self.all_tasks.append(
            {
                "id": secrets.token_hex(8),
                "title": self.task_title.strip(),
                "description": self.task_description.strip(),
                "status": self.task_status,
                "priority": self.task_priority,
                "project_id": self.task_project_id,
                "project_name": next(
                    (
                        p["name"]
                        for p in self.available_projects
                        if p["id"] == self.task_project_id
                    ),
                    "Unknown",
                ),
                "assignee_name": next(
                    (
                        u["name"]
                        for u in self.available_users
                        if u["id"] == self.task_assignee_id
                    ),
                    "",
                ),
                "due_date": self.task_due_date,
            }
        )
        self.show_create_task_modal = False
        yield rx.toast("Task created successfully!")

    @rx.event
    def open_edit_task_modal(self, task: dict):
        self.editing_task_id = str(task.get("id", ""))
        self.task_title = str(task.get("title", ""))
        self.task_description = str(task.get("description", ""))
        self.task_status = str(task.get("status", "todo"))
        self.task_priority = str(task.get("priority", "medium"))
        self.task_project_id = str(task.get("project_id", ""))
        self.task_assignee_id = str(task.get("assignee_id", ""))
        self.task_due_date = str(task.get("due_date", ""))
        self.task_error = ""
        self.show_edit_task_modal = True

    @rx.event
    async def update_task(self):
        self.task_error = ""
        if not self.task_title or len(self.task_title.strip()) < 3:
            self.task_error = "Task title must be at least 3 characters."
            return
        for t in self.all_tasks:
            if t.get("id") == self.editing_task_id:
                t["title"] = self.task_title.strip()
                t["description"] = self.task_description.strip()
                t["status"] = self.task_status
                t["priority"] = self.task_priority
                t["due_date"] = self.task_due_date
                break
        self.show_edit_task_modal = False
        yield rx.toast("Task updated successfully!")

    @rx.event
    def open_delete_task_modal(self, task_id: str):
        self.deleting_task_id = task_id
        self.show_delete_task_modal = True

    @rx.event
    async def delete_task(self):
        self.all_tasks = [
            t for t in self.all_tasks if t.get("id") != self.deleting_task_id
        ]
        self.show_delete_task_modal = False
        yield rx.toast("Task deleted successfully!")

    @rx.event
    async def update_task_status(self, task_id: str, new_status: str):
        for t in self.all_tasks:
            if t.get("id") == task_id:
                t["status"] = new_status
                break
        yield rx.toast(f"Task moved to {new_status.replace('_', ' ').title()}")

    @rx.event
    def close_task_modals(self):
        self.show_create_task_modal = False
        self.show_edit_task_modal = False
        self.show_delete_task_modal = False