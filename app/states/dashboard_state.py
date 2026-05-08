import reflex as rx
from app.states.auth_state import AuthState
import logging
from sqlmodel import text
from datetime import datetime


class DashboardState(AuthState):
    total_projects: int = 0
    total_tasks: int = 0
    completed_tasks: int = 0
    overdue_tasks: int = 0
    in_progress_tasks: int = 0
    recent_activities: list[dict[str, str]] = []
    task_distribution: dict[str, int] = {
        "todo": 0,
        "in_progress": 0,
        "review": 0,
        "done": 0,
    }

    @rx.var
    def progress_percentage(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return round(self.completed_tasks / self.total_tasks * 100, 1)

    @rx.event
    async def load_dashboard_data(self):
        if not self.is_authenticated:
            return
        try:
            async with rx.asession() as session:
                pass
            self.total_projects = 12
            self.total_tasks = 64
            self.completed_tasks = 30
            self.overdue_tasks = 3
            self.in_progress_tasks = 15
            self.task_distribution = {
                "todo": 10,
                "in_progress": 15,
                "review": 9,
                "done": 30,
            }
            self.recent_activities = [
                {
                    "action": "completed task",
                    "project_name": "Website Redesign",
                    "user_name": "Alice",
                    "timestamp": "2 hours ago",
                    "type": "completed",
                },
                {
                    "action": "created project",
                    "project_name": "Mobile App",
                    "user_name": "Bob",
                    "timestamp": "5 hours ago",
                    "type": "created",
                },
            ]
        except Exception as e:
            logging.exception(f"Error loading dashboard data: {e}")