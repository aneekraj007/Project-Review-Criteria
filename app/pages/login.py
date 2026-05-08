import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "circle_check",
                    class_name="w-12 h-12 text-indigo-600 mx-auto mb-4",
                ),
                rx.el.h2(
                    "Welcome back to TaskFlow",
                    class_name="text-2xl font-bold text-gray-900 text-center mb-2",
                ),
                rx.el.p(
                    "Sign in to your account to continue",
                    class_name="text-gray-500 text-center mb-8",
                ),
                rx.cond(
                    AuthState.login_error != "",
                    rx.el.div(
                        AuthState.login_error,
                        class_name="bg-rose-50 text-rose-600 text-sm p-3 rounded-lg border border-rose-100 mb-6 text-center",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.label(
                        "Email address",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="email",
                        placeholder="you@example.com",
                        on_change=AuthState.set_login_email.debounce(300),
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent outline-none transition-all mb-4",
                    ),
                    rx.el.label(
                        "Password",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="••••••••",
                        on_change=AuthState.set_login_password.debounce(300),
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent outline-none transition-all mb-6",
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.login_loading, "Signing in...", "Sign in"
                        ),
                        on_click=AuthState.login,
                        class_name="w-full bg-indigo-600 text-white font-medium py-2.5 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm mb-6",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Don't have an account? ",
                            class_name="text-gray-500 text-sm",
                        ),
                        rx.el.a(
                            "Sign up",
                            href="/register",
                            class_name="text-indigo-600 text-sm font-medium hover:text-indigo-700",
                        ),
                        class_name="text-center",
                    ),
                    class_name="w-full",
                ),
                class_name="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 w-full max-w-md",
            ),
            class_name="w-full flex items-center justify-center p-4",
        ),
        class_name="min-h-screen bg-gray-50 flex items-center justify-center font-['Inter']",
    )