import reflex as rx
from app.components.sidebar import layout
from app.states.dashboard_state import DashboardState


def render_activity_item(activity: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=rx.match(
                    activity.get("type", ""),
                    ("completed", "w-2 h-2 rounded-full bg-emerald-500"),
                    ("created", "w-2 h-2 rounded-full bg-blue-500"),
                    "w-2 h-2 rounded-full bg-gray-400",
                )
            ),
            rx.el.p(
                rx.el.span(
                    activity.get("user_name", "").to_string(),
                    class_name="font-semibold text-gray-900",
                ),
                " ",
                activity.get("action", "").to_string(),
                " ",
                rx.el.span(
                    activity.get("project_name", "").to_string(),
                    class_name="font-medium text-indigo-600",
                ),
                class_name="ml-3 text-sm text-gray-600",
            ),
            class_name="flex items-center",
        ),
        rx.el.span(
            activity.get("timestamp", "").to_string(),
            class_name="text-xs text-gray-400",
        ),
        class_name="flex items-center justify-between py-3 border-b border-gray-100 last:border-0",
    )


def dashboard_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("folder", class_name="w-6 h-6 text-indigo-600"),
                        class_name="bg-indigo-50 p-3 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Active Projects",
                            class_name="text-gray-500 text-sm font-medium",
                        ),
                        rx.el.p(
                            DashboardState.total_projects,
                            class_name="text-2xl font-bold text-gray-900 mt-1",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "list-checks", class_name="w-6 h-6 text-blue-600"
                        ),
                        class_name="bg-blue-50 p-3 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Total Tasks",
                            class_name="text-gray-500 text-sm font-medium",
                        ),
                        rx.el.p(
                            DashboardState.total_tasks,
                            class_name="text-2xl font-bold text-gray-900 mt-1",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "circle-check",
                            class_name="w-6 h-6 text-emerald-600",
                        ),
                        class_name="bg-emerald-50 p-3 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Completed",
                            class_name="text-gray-500 text-sm font-medium",
                        ),
                        rx.el.p(
                            DashboardState.completed_tasks,
                            class_name="text-2xl font-bold text-emerald-600 mt-1",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "triangle_alert", class_name="w-6 h-6 text-rose-600"
                        ),
                        class_name="bg-rose-50 p-3 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Overdue",
                            class_name="text-gray-500 text-sm font-medium",
                        ),
                        rx.el.p(
                            DashboardState.overdue_tasks,
                            class_name="text-2xl font-bold text-rose-600 mt-1",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4",
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Task Overview",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "To Do",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.span(
                                DashboardState.task_distribution["todo"],
                                class_name="text-sm font-bold text-gray-900",
                            ),
                            class_name="flex justify-between mb-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-2 bg-gray-400 rounded-full",
                                style={
                                    "width": f"{DashboardState.task_distribution['todo'].to(float) / rx.cond(DashboardState.total_tasks > 0, DashboardState.total_tasks, 1).to(float) * 100}%"
                                },
                            ),
                            class_name="w-full bg-gray-100 rounded-full h-2",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "In Progress",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.span(
                                DashboardState.task_distribution["in_progress"],
                                class_name="text-sm font-bold text-gray-900",
                            ),
                            class_name="flex justify-between mb-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-2 bg-blue-500 rounded-full",
                                style={
                                    "width": f"{DashboardState.task_distribution['in_progress'].to(float) / rx.cond(DashboardState.total_tasks > 0, DashboardState.total_tasks, 1).to(float) * 100}%"
                                },
                            ),
                            class_name="w-full bg-gray-100 rounded-full h-2",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Review",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.span(
                                DashboardState.task_distribution["review"],
                                class_name="text-sm font-bold text-gray-900",
                            ),
                            class_name="flex justify-between mb-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-2 bg-amber-500 rounded-full",
                                style={
                                    "width": f"{DashboardState.task_distribution['review'].to(float) / rx.cond(DashboardState.total_tasks > 0, DashboardState.total_tasks, 1).to(float) * 100}%"
                                },
                            ),
                            class_name="w-full bg-gray-100 rounded-full h-2",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Done",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.span(
                                DashboardState.task_distribution["done"],
                                class_name="text-sm font-bold text-gray-900",
                            ),
                            class_name="flex justify-between mb-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-2 bg-emerald-500 rounded-full",
                                style={
                                    "width": f"{DashboardState.task_distribution['done'].to(float) / rx.cond(DashboardState.total_tasks > 0, DashboardState.total_tasks, 1).to(float) * 100}%"
                                },
                            ),
                            class_name="w-full bg-gray-100 rounded-full h-2",
                        ),
                    ),
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-200 mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Recent Activity",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.cond(
                    DashboardState.recent_activities.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            DashboardState.recent_activities,
                            render_activity_item,
                        )
                    ),
                    rx.el.div(
                        rx.icon(
                            "clock",
                            class_name="w-8 h-8 text-gray-300 mx-auto mb-2",
                        ),
                        rx.el.p(
                            "No recent activity yet.",
                            class_name="text-gray-500",
                        ),
                        class_name="text-center py-8",
                    ),
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-200",
            ),
        ),
        "Dashboard",
    )