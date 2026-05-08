import reflex as rx
from app.states.auth_state import AuthState


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "circle_check",
                    class_name="w-12 h-12 text-indigo-600 mx-auto mb-4",
                ),
                rx.el.h2(
                    "Create an account",
                    class_name="text-2xl font-bold text-gray-900 text-center mb-2",
                ),
                rx.el.p(
                    "Join TaskFlow to manage your projects",
                    class_name="text-gray-500 text-center mb-8",
                ),
                rx.cond(
                    AuthState.reg_error != "",
                    rx.el.div(
                        AuthState.reg_error,
                        class_name="bg-rose-50 text-rose-600 text-sm p-3 rounded-lg border border-rose-100 mb-6 text-center",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="text",
                        placeholder="John Doe",
                        on_change=AuthState.set_reg_name.debounce(300),
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent outline-none transition-all mb-4",
                    ),
                    rx.el.label(
                        "Email address",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="email",
                        placeholder="you@example.com",
                        on_change=AuthState.set_reg_email.debounce(300),
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent outline-none transition-all mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Password",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="password",
                                placeholder="••••••••",
                                on_change=AuthState.set_reg_password.debounce(
                                    300
                                ),
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent outline-none transition-all",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Confirm Password",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="password",
                                placeholder="••••••••",
                                on_change=AuthState.set_reg_confirm_password.debounce(
                                    300
                                ),
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent outline-none transition-all",
                            ),
                            class_name="flex-1",
                        ),
                        class_name="flex gap-4 mb-4",
                    ),
                    rx.el.label(
                        "Role",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Admin", value="Admin"),
                            rx.el.option("Manager", value="Manager"),
                            rx.el.option("Member", value="Member"),
                            on_change=AuthState.set_reg_role,
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-600 focus:border-transparent outline-none transition-all appearance-none bg-white",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none",
                        ),
                        class_name="relative mb-6",
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.reg_loading,
                            "Creating account...",
                            "Create Account",
                        ),
                        on_click=AuthState.register,
                        class_name="w-full bg-indigo-600 text-white font-medium py-2.5 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm mb-6",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Already have an account? ",
                            class_name="text-gray-500 text-sm",
                        ),
                        rx.el.a(
                            "Sign in",
                            href="/login",
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