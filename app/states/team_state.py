import reflex as rx
import logging
from sqlmodel import text
from app.states.auth_state import AuthState


class TeamState(AuthState):
    team_members: list[dict[str, str]] = []
    member_count: int = 0

    @rx.event
    async def load_team(self):
        if not self.is_authenticated:
            return
        try:
            async with rx.asession() as session:
                pass
            self.team_members = [
                {
                    "name": "Alice Admin",
                    "email": "alice@example.com",
                    "role": "Admin",
                    "initials": "AA",
                },
                {
                    "name": "Bob Manager",
                    "email": "bob@example.com",
                    "role": "Manager",
                    "initials": "BM",
                },
                {
                    "name": "Charlie Member",
                    "email": "charlie@example.com",
                    "role": "Member",
                    "initials": "CM",
                },
            ]
            self.member_count = len(self.team_members)
        except Exception as e:
            logging.exception(f"Error loading team data: {e}")