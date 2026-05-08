import reflex as rx
from app.states.auth_state import AuthState


def nav_item(icon: str, label: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-5 h-5 mr-3"),
        rx.el.span(label, class_name="font-medium"),
        href=href,
        class_name="flex items-center px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors mb-1",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "circle_check", class_name="w-8 h-8 text-indigo-600 mr-2"
                ),
                rx.el.span(
                    "TaskFlow", class_name="text-xl font-bold text-gray-900"
                ),
                class_name="flex items-center px-6 py-6 border-b border-gray-100",
            ),
            rx.el.nav(
                nav_item("layout-dashboard", "Dashboard", "/dashboard"),
                nav_item("folder", "Projects", "/projects"),
                nav_item("square_check", "Tasks", "/tasks"),
                rx.cond(
                    (AuthState.current_user_role == "Admin")
                    | (AuthState.current_user_role == "Manager"),
                    nav_item("users", "Team", "/team"),
                    rx.fragment(),
                ),
                nav_item("settings", "Settings", "/settings"),
                class_name="flex-1 px-4 py-6 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        AuthState.current_user_name[:2].upper(),
                        class_name="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-sm",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AuthState.current_user_name,
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.span(
                            AuthState.current_user_role,
                            class_name=rx.cond(
                                AuthState.current_user_role == "Admin",
                                "text-xs px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 font-medium",
                                rx.cond(
                                    AuthState.current_user_role == "Manager",
                                    "text-xs px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 font-medium",
                                    "text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium",
                                ),
                            ),
                        ),
                        class_name="ml-3 flex-1 overflow-hidden",
                    ),
                    class_name="flex items-center mb-4",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-4 h-4 mr-2"),
                    "Sign out",
                    on_click=AuthState.logout,
                    class_name="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-gray-600 bg-gray-50 rounded-lg hover:bg-rose-50 hover:text-rose-600 transition-colors",
                ),
                class_name="p-4 border-t border-gray-100",
            ),
            class_name="flex flex-col h-full bg-white border-r border-gray-200",
        ),
        class_name="w-64 h-screen fixed top-0 left-0 flex-shrink-0 z-20 hidden md:block",
    )


def mobile_sidebar() -> rx.Component:
    return rx.cond(
        AuthState.mobile_sidebar_open,
        rx.el.div(
            rx.el.div(
                on_click=AuthState.toggle_mobile_sidebar,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 md:hidden",
            ),
            rx.el.aside(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "circle_check",
                            class_name="w-8 h-8 text-indigo-600 mr-2",
                        ),
                        rx.el.span(
                            "TaskFlow",
                            class_name="text-xl font-bold text-gray-900",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="w-6 h-6 text-gray-500"),
                        on_click=AuthState.toggle_mobile_sidebar,
                    ),
                    class_name="flex items-center justify-between px-6 py-6 border-b border-gray-100",
                ),
                rx.el.nav(
                    nav_item("layout-dashboard", "Dashboard", "/dashboard"),
                    nav_item("folder", "Projects", "/projects"),
                    nav_item("square_check", "Tasks", "/tasks"),
                    rx.cond(
                        (AuthState.current_user_role == "Admin")
                        | (AuthState.current_user_role == "Manager"),
                        nav_item("users", "Team", "/team"),
                        rx.fragment(),
                    ),
                    nav_item("settings", "Settings", "/settings"),
                    class_name="flex-1 px-4 py-6 overflow-y-auto",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("log-out", class_name="w-4 h-4 mr-2"),
                        "Sign out",
                        on_click=AuthState.logout,
                        class_name="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-gray-600 bg-gray-50 rounded-lg hover:bg-rose-50 hover:text-rose-600 transition-colors",
                    ),
                    class_name="p-4 border-t border-gray-100",
                ),
                class_name="w-64 h-screen fixed top-0 left-0 flex-col bg-white border-r border-gray-200 z-50 flex md:hidden",
            ),
        ),
        rx.fragment(),
    )


def layout(content: rx.Component, title: str) -> rx.Component:
    return rx.el.div(
        sidebar(),
        mobile_sidebar(),
        rx.el.main(
            rx.el.header(
                rx.el.div(
                    rx.el.button(
                        rx.icon("menu", class_name="w-6 h-6 text-gray-600"),
                        on_click=AuthState.toggle_mobile_sidebar,
                        class_name="mr-4 md:hidden",
                    ),
                    rx.el.h1(
                        title, class_name="text-2xl font-bold text-gray-900"
                    ),
                    class_name="flex items-center",
                ),
                class_name="bg-white border-b border-gray-200 px-6 py-5 flex items-center justify-between sticky top-0 z-10",
            ),
            rx.el.div(content, class_name="p-6 md:p-8"),
            class_name="flex-1 md:ml-64 min-h-screen bg-gray-50 flex-col",
        ),
        class_name="flex min-h-screen font-['Inter']",
    )