import reflex as rx
from app.components.sidebar import layout
from app.states.project_state import ProjectState


def render_kanban_task(task: dict, status: str) -> rx.Component:
    return rx.cond(
        task.get("status", "") == status,
        rx.el.div(
            rx.el.h4(
                task.get("title", "").to_string(),
                class_name="font-medium text-gray-900 mb-2",
            ),
            rx.el.div(
                rx.el.span(
                    task.get("priority", "")
                    .to_string()
                    .replace("_", " ")
                    .title(),
                    class_name=rx.match(
                        task.get("priority", ""),
                        (
                            "high",
                            "bg-orange-100 text-orange-700 px-2 py-0.5 rounded text-xs font-medium",
                        ),
                        (
                            "critical",
                            "bg-rose-100 text-rose-700 px-2 py-0.5 rounded text-xs font-medium",
                        ),
                        (
                            "medium",
                            "bg-amber-100 text-amber-700 px-2 py-0.5 rounded text-xs font-medium",
                        ),
                        "bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-xs font-medium",
                    ),
                ),
                class_name="mb-3",
            ),
            rx.el.div(
                rx.el.span(
                    task.get("assignee", "").to_string(),
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex items-center justify-between",
            ),
            class_name="bg-white border border-gray-200 rounded-lg p-3 mb-3 shadow-sm hover:shadow-md transition-shadow cursor-grab",
        ),
        rx.fragment(),
    )


def kanban_column(title: str, status: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(title, class_name="font-bold text-gray-700"),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.div(
            rx.foreach(
                ProjectState.project_tasks,
                lambda t: render_kanban_task(t, status),
            ),
            class_name="space-y-3 min-h-[200px] flex-1",
        ),
        rx.el.button(
            "+ Add Task",
            class_name="w-full mt-3 py-2 text-sm font-medium text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors border border-transparent hover:border-indigo-100",
        ),
        class_name="bg-gray-50 p-4 rounded-xl border border-gray-200 min-w-[280px] flex-1 flex flex-col",
    )


def project_detail_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
                    "Back to Projects",
                    href="/projects",
                    class_name="flex items-center text-indigo-600 font-medium hover:text-indigo-800 mb-6 w-fit",
                ),
                rx.el.div(
                    rx.el.h1(
                        ProjectState.selected_project.get(
                            "name", "Loading..."
                        ).to_string(),
                        class_name="text-3xl font-bold text-gray-900",
                    ),
                    rx.el.span(
                        ProjectState.selected_project.get("status", "")
                        .to_string()
                        .replace("_", " ")
                        .title(),
                        class_name=rx.match(
                            ProjectState.selected_project.get("status", ""),
                            (
                                "active",
                                "ml-4 px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-sm font-medium",
                            ),
                            (
                                "on_hold",
                                "ml-4 px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-sm font-medium",
                            ),
                            "ml-4 px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-medium",
                        ),
                    ),
                    class_name="flex items-center mb-2",
                ),
                rx.el.p(
                    ProjectState.selected_project.get(
                        "description", ""
                    ).to_string(),
                    class_name="text-gray-600 max-w-3xl",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                kanban_column("To Do", "todo"),
                kanban_column("In Progress", "in_progress"),
                kanban_column("Review", "review"),
                kanban_column("Done", "done"),
                class_name="flex gap-6 overflow-x-auto pb-4",
            ),
        ),
        "Project Board",
    )