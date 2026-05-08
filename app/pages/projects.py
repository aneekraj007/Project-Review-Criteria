import reflex as rx
from app.components.sidebar import layout
from app.states.project_state import ProjectState


def render_project_card(project: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                project.get("name", "").to_string(),
                href=f"/projects/{project.get('id', '')}",
                class_name="font-bold text-lg text-gray-900 hover:text-indigo-600",
            ),
            rx.el.span(
                project.get("status", "").to_string().replace("_", " ").title(),
                class_name=rx.match(
                    project.get("status", ""),
                    (
                        "active",
                        "px-2 py-1 rounded-full bg-emerald-100 text-emerald-700 text-xs font-medium",
                    ),
                    (
                        "on_hold",
                        "px-2 py-1 rounded-full bg-amber-100 text-amber-700 text-xs font-medium",
                    ),
                    "px-2 py-1 rounded-full bg-gray-100 text-gray-700 text-xs font-medium",
                ),
            ),
            class_name="flex items-start justify-between mb-2",
        ),
        rx.el.p(
            project.get("description", "").to_string(),
            class_name="text-gray-500 text-sm line-clamp-2 mb-4 h-10",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    project.get("completed_tasks", 0).to_string(),
                    "/",
                    project.get("task_count", 0).to_string(),
                    " tasks",
                    class_name="text-xs text-gray-500 font-medium",
                ),
                class_name="flex flex-col gap-1 w-full mr-4",
            ),
            rx.el.div(
                rx.icon("calendar", class_name="w-4 h-4 text-gray-400 mr-1"),
                rx.el.span(
                    project.get("due_date", "").to_string(),
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex items-center whitespace-nowrap",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="w-4 h-4"),
                on_click=ProjectState.open_edit_modal(project),
                class_name="text-gray-400 hover:text-indigo-600 p-2",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                on_click=ProjectState.open_delete_modal(
                    project.get("id", "").to_string()
                ),
                class_name="text-gray-400 hover:text-rose-600 p-2",
            ),
            class_name="flex items-center justify-end mt-4 pt-4 border-t border-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-all",
    )


def create_edit_modal() -> rx.Component:
    return rx.cond(
        ProjectState.show_create_modal | ProjectState.show_edit_modal,
        rx.el.div(
            rx.el.div(
                on_click=ProjectState.close_modals,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
            ),
            rx.el.div(
                rx.el.h2(
                    rx.cond(
                        ProjectState.show_create_modal,
                        "Create New Project",
                        "Edit Project",
                    ),
                    class_name="text-xl font-bold text-gray-900 mb-4",
                ),
                rx.cond(
                    ProjectState.form_error != "",
                    rx.el.div(
                        ProjectState.form_error,
                        class_name="bg-rose-50 text-rose-600 p-3 rounded-lg text-sm mb-4",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.label(
                        "Name",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        on_change=ProjectState.set_form_name,
                        class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 mb-4",
                        default_value=ProjectState.form_name,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Description",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.textarea(
                        on_change=ProjectState.set_form_description,
                        rows="3",
                        class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 mb-4",
                        default_value=ProjectState.form_description,
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Status",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("Active", value="active"),
                        rx.el.option("On Hold", value="on_hold"),
                        rx.el.option("Completed", value="completed"),
                        rx.el.option("Archived", value="archived"),
                        value=ProjectState.form_status,
                        on_change=ProjectState.set_form_status,
                        class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 mb-4 appearance-none",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Due Date",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ProjectState.set_form_due_date,
                        class_name="w-full px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 mb-6",
                        default_value=ProjectState.form_due_date,
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=ProjectState.close_modals,
                        class_name="px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium",
                    ),
                    rx.el.button(
                        rx.cond(
                            ProjectState.show_create_modal,
                            "Create Project",
                            "Update Project",
                        ),
                        on_click=rx.cond(
                            ProjectState.show_create_modal,
                            ProjectState.create_project,
                            ProjectState.update_project,
                        ),
                        class_name="px-4 py-2 text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg font-medium",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                class_name="bg-white rounded-2xl shadow-xl p-6 w-full max-w-lg mx-4 z-50 relative",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center",
        ),
        rx.fragment(),
    )


def delete_modal() -> rx.Component:
    return rx.cond(
        ProjectState.show_delete_modal,
        rx.el.div(
            rx.el.div(
                on_click=ProjectState.close_modals,
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
                    "Delete Project?",
                    class_name="text-xl font-bold text-gray-900 text-center mb-2",
                ),
                rx.el.p(
                    "Are you sure you want to delete this project? This action cannot be undone.",
                    class_name="text-gray-500 text-center mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=ProjectState.close_modals,
                        class_name="w-full px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium",
                    ),
                    rx.el.button(
                        "Delete",
                        on_click=ProjectState.delete_project,
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


def projects_page() -> rx.Component:
    return layout(
        rx.el.div(
            create_edit_modal(),
            delete_modal(),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search projects...",
                        on_change=ProjectState.set_search_query.debounce(300),
                        class_name="w-full sm:w-64 pl-10 pr-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500",
                    ),
                    class_name="relative",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("All", value="all"),
                        rx.el.option("Active", value="active"),
                        rx.el.option("On Hold", value="on_hold"),
                        rx.el.option("Completed", value="completed"),
                        on_change=ProjectState.set_status_filter,
                        class_name="px-3 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-indigo-500 appearance-none bg-white",
                    ),
                    rx.el.button(
                        "+ New Project",
                        on_click=ProjectState.open_create_modal,
                        class_name="bg-indigo-600 text-white rounded-lg px-4 py-2 font-medium hover:bg-indigo-700 transition-colors",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="flex items-center justify-between mb-6 flex-wrap gap-4",
            ),
            rx.cond(
                ProjectState.filtered_projects.length() > 0,
                rx.el.div(
                    rx.foreach(
                        ProjectState.filtered_projects, render_project_card
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.div(
                    rx.icon(
                        "folder-open",
                        class_name="w-16 h-16 text-gray-300 mx-auto mb-4",
                    ),
                    rx.el.h3(
                        "No projects yet",
                        class_name="text-lg font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Create your first project to get started.",
                        class_name="text-gray-500 mb-4",
                    ),
                    rx.el.button(
                        "+ New Project",
                        on_click=ProjectState.open_create_modal,
                        class_name="bg-indigo-600 text-white rounded-lg px-4 py-2 font-medium hover:bg-indigo-700",
                    ),
                    class_name="bg-white p-12 rounded-xl border border-gray-200 text-center",
                ),
            ),
        ),
        "Projects",
    )