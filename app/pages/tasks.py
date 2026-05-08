import reflex as rx
from app.components.sidebar import layout
from app.states.task_state import TaskState


def render_task(task: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    task.get("title", "").to_string(),
                    class_name="text-lg font-bold text-gray-900",
                ),
                rx.el.span(
                    task.get("project_name", "").to_string(),
                    class_name="text-xs text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded ml-3 font-medium",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=TaskState.open_edit_task_modal(task),
                    class_name="text-gray-400 hover:text-indigo-600 p-2",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=TaskState.open_delete_task_modal(
                        task.get("id", "").to_string()
                    ),
                    class_name="text-gray-400 hover:text-rose-600 p-2",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-start mb-2",
        ),
        rx.el.div(
            rx.el.span(
                task.get("status", "").to_string().replace("_", " ").title(),
                class_name=rx.match(
                    task.get("status", ""),
                    (
                        "done",
                        "text-xs font-medium px-2 py-1 rounded-full bg-emerald-100 text-emerald-700 mr-2",
                    ),
                    (
                        "in_progress",
                        "text-xs font-medium px-2 py-1 rounded-full bg-blue-100 text-blue-700 mr-2",
                    ),
                    (
                        "review",
                        "text-xs font-medium px-2 py-1 rounded-full bg-amber-100 text-amber-700 mr-2",
                    ),
                    "text-xs font-medium px-2 py-1 rounded-full bg-gray-100 text-gray-700 mr-2",
                ),
            ),
            rx.el.span(
                task.get("priority", "").to_string().replace("_", " ").title(),
                class_name=rx.match(
                    task.get("priority", ""),
                    (
                        "critical",
                        "text-xs font-medium px-2 py-1 rounded-full bg-rose-100 text-rose-700 mr-2",
                    ),
                    (
                        "high",
                        "text-xs font-medium px-2 py-1 rounded-full bg-orange-100 text-orange-700 mr-2",
                    ),
                    (
                        "medium",
                        "text-xs font-medium px-2 py-1 rounded-full bg-amber-100 text-amber-700 mr-2",
                    ),
                    "text-xs font-medium px-2 py-1 rounded-full bg-slate-100 text-slate-700 mr-2",
                ),
            ),
            rx.el.div(
                rx.icon("user", class_name="w-3 h-3 text-gray-400 mr-1"),
                rx.el.span(
                    task.get("assignee_name", "").to_string(),
                    class_name="text-sm text-gray-500 mr-4",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.icon("calendar", class_name="w-3 h-3 text-gray-400 mr-1"),
                rx.el.span(
                    task.get("due_date", "").to_string(),
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex items-center",
            ),
            class_name="flex flex-wrap items-center mt-2",
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-200 shadow-sm mb-3 hover:shadow-md transition-shadow",
    )


def task_modal() -> rx.Component:
    return rx.cond(
        TaskState.show_create_task_modal | TaskState.show_edit_task_modal,
        rx.el.div(
            rx.el.div(
                on_click=TaskState.close_task_modals,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
            ),
            rx.el.div(
                rx.el.h2(
                    rx.cond(
                        TaskState.show_create_task_modal,
                        "Create New Task",
                        "Edit Task",
                    ),
                    class_name="text-xl font-bold text-gray-900 mb-4",
                ),
                rx.cond(
                    TaskState.task_error != "",
                    rx.el.div(
                        TaskState.task_error,
                        class_name="bg-rose-50 text-rose-600 p-3 rounded-lg text-sm mb-4",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.label(
                        "Title",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        on_change=TaskState.set_task_title,
                        class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 mb-4",
                        default_value=TaskState.task_title,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Description",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.textarea(
                        on_change=TaskState.set_task_description,
                        rows="3",
                        class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 mb-4",
                        default_value=TaskState.task_description,
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Project",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option(
                                "Select Project", value="", disabled=True
                            ),
                            rx.foreach(
                                TaskState.available_projects,
                                lambda p: rx.el.option(
                                    p.get("name", "").to_string(),
                                    value=p.get("id", "").to_string(),
                                ),
                            ),
                            value=TaskState.task_project_id,
                            on_change=TaskState.set_task_project_id,
                            class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 appearance-none bg-white",
                        ),
                        class_name="w-1/2",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Assignee",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Unassigned", value=""),
                            rx.foreach(
                                TaskState.available_users,
                                lambda u: rx.el.option(
                                    u.get("name", "").to_string(),
                                    value=u.get("id", "").to_string(),
                                ),
                            ),
                            value=TaskState.task_assignee_id,
                            on_change=TaskState.set_task_assignee_id,
                            class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 appearance-none bg-white",
                        ),
                        class_name="w-1/2",
                    ),
                    class_name="flex gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Status",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("To Do", value="todo"),
                            rx.el.option("In Progress", value="in_progress"),
                            rx.el.option("Review", value="review"),
                            rx.el.option("Done", value="done"),
                            value=TaskState.task_status,
                            on_change=TaskState.set_task_status,
                            class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 appearance-none bg-white",
                        ),
                        class_name="w-1/2",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Priority",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Low", value="low"),
                            rx.el.option("Medium", value="medium"),
                            rx.el.option("High", value="high"),
                            rx.el.option("Critical", value="critical"),
                            value=TaskState.task_priority,
                            on_change=TaskState.set_task_priority,
                            class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 appearance-none bg-white",
                        ),
                        class_name="w-1/2",
                    ),
                    class_name="flex gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Due Date",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=TaskState.set_task_due_date,
                        class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 mb-6",
                        default_value=TaskState.task_due_date,
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=TaskState.close_task_modals,
                        class_name="px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium",
                    ),
                    rx.el.button(
                        rx.cond(
                            TaskState.show_create_task_modal,
                            "Create Task",
                            "Update Task",
                        ),
                        on_click=rx.cond(
                            TaskState.show_create_task_modal,
                            TaskState.create_task,
                            TaskState.update_task,
                        ),
                        class_name="px-4 py-2 text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg font-medium",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                class_name="bg-white rounded-2xl shadow-xl p-6 w-full max-w-lg mx-4 z-50 relative max-h-[90vh] overflow-y-auto",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center",
        ),
        rx.fragment(),
    )


def delete_task_modal() -> rx.Component:
    return rx.cond(
        TaskState.show_delete_task_modal,
        rx.el.div(
            rx.el.div(
                on_click=TaskState.close_task_modals,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "triangle_alert", class_name="w-12 h-12 text-rose-600"
                    ),
                    class_name="flex justify-center mb-4",
                ),
                rx.el.h2(
                    "Delete Task?",
                    class_name="text-xl font-bold text-gray-900 text-center mb-2",
                ),
                rx.el.p(
                    "Are you sure you want to delete this task? This action cannot be undone.",
                    class_name="text-gray-500 text-center mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=TaskState.close_task_modals,
                        class_name="w-full px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium",
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=TaskState.delete_task,
                        class_name="w-full px-4 py-2 text-white bg-rose-600 hover:bg-rose-700 rounded-lg font-medium",
                    ),
                    class_name="flex gap-3",
                ),
                class_name="bg-white rounded-2xl shadow-xl p-6 w-full max-w-sm mx-4 z-50 relative",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center",
        ),
        rx.fragment(),
    )


def tasks_page() -> rx.Component:
    return layout(
        rx.el.div(
            task_modal(),
            delete_task_modal(),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search tasks...",
                        on_change=TaskState.set_search_query.debounce(300),
                        class_name="w-full sm:w-64 pl-10 pr-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500",
                    ),
                    class_name="relative",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("All Statuses", value="all"),
                        rx.el.option("To Do", value="todo"),
                        rx.el.option("In Progress", value="in_progress"),
                        rx.el.option("Review", value="review"),
                        rx.el.option("Done", value="done"),
                        on_change=TaskState.set_status_filter,
                        class_name="px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 appearance-none bg-white",
                    ),
                    rx.el.select(
                        rx.el.option("All Priorities", value="all"),
                        rx.el.option("Low", value="low"),
                        rx.el.option("Medium", value="medium"),
                        rx.el.option("High", value="high"),
                        rx.el.option("Critical", value="critical"),
                        on_change=TaskState.set_priority_filter,
                        class_name="px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 appearance-none bg-white",
                    ),
                    rx.el.button(
                        "+ New Task",
                        on_click=TaskState.open_create_task_modal,
                        class_name="bg-indigo-600 text-white rounded-lg px-4 py-2 font-medium hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="flex items-center justify-between mb-6 flex-wrap gap-4",
            ),
            rx.cond(
                TaskState.filtered_tasks.length() > 0,
                rx.el.div(
                    rx.foreach(TaskState.filtered_tasks, render_task),
                    class_name="space-y-3",
                ),
                rx.el.div(
                    rx.icon(
                        "message_circle_check",
                        class_name="w-16 h-16 text-gray-300 mx-auto mb-4",
                    ),
                    rx.el.h3(
                        "No tasks found",
                        class_name="text-lg font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "You're all caught up! Create a new task to get started.",
                        class_name="text-gray-500 mb-4",
                    ),
                    rx.el.button(
                        "+ New Task",
                        on_click=TaskState.open_create_task_modal,
                        class_name="bg-indigo-600 text-white rounded-lg px-4 py-2 font-medium hover:bg-indigo-700",
                    ),
                    class_name="bg-white p-12 rounded-xl border border-gray-200 text-center",
                ),
            ),
        ),
        "Tasks",
    )