import reflex as rx
from app.components.sidebar import layout
from app.states.team_state import TeamState


def member_card(member: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            member.get("initials", "").to_string(),
            class_name="w-16 h-16 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-xl mb-4",
        ),
        rx.el.h3(
            member.get("name", "").to_string(),
            class_name="font-bold text-gray-900 text-lg",
        ),
        rx.el.p(
            member.get("email", "").to_string(),
            class_name="text-sm text-gray-500 mb-4",
        ),
        rx.el.span(
            member.get("role", "").to_string(),
            class_name=rx.match(
                member.get("role", ""),
                (
                    "Admin",
                    "px-3 py-1 rounded-full bg-indigo-100 text-indigo-700 text-xs font-medium",
                ),
                (
                    "Manager",
                    "px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-xs font-medium",
                ),
                "px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-medium",
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all flex flex-col items-center text-center",
    )


def team_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Team", class_name="text-2xl font-bold text-gray-900"),
                rx.el.span(
                    f"{TeamState.member_count} Members",
                    class_name="ml-4 px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm font-medium",
                ),
                class_name="flex items-center mb-8",
            ),
            rx.cond(
                TeamState.team_members.length() > 0,
                rx.el.div(
                    rx.foreach(TeamState.team_members, member_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "No team members found.",
                        class_name="text-gray-500 font-medium",
                    ),
                    class_name="bg-white p-12 rounded-xl border border-gray-200 text-center",
                ),
            ),
        ),
        "Team Management",
    )