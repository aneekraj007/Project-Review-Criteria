import reflex as rx
from app.components.sidebar import layout
from app.states.auth_state import AuthState


def settings_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Profile Information",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            AuthState.current_user_name[:2].upper(),
                            class_name="w-20 h-20 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-2xl mb-4",
                        ),
                        rx.el.p(
                            AuthState.current_user_name,
                            class_name="font-bold text-gray-900 text-lg",
                        ),
                        rx.el.p(
                            AuthState.current_user_email,
                            class_name="text-gray-500 text-sm mb-4",
                        ),
                        rx.el.span(
                            AuthState.current_user_role,
                            class_name="px-4 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold uppercase tracking-wider",
                        ),
                        class_name="flex flex-col items-center border border-gray-100 rounded-xl p-8 bg-gray-50",
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Change Password",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.cond(
                        AuthState.settings_error != "",
                        rx.el.div(
                            AuthState.settings_error,
                            class_name="bg-rose-50 text-rose-600 text-sm p-3 rounded-lg border border-rose-100 mb-4",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AuthState.settings_success != "",
                        rx.el.div(
                            AuthState.settings_success,
                            class_name="bg-emerald-50 text-emerald-600 text-sm p-3 rounded-lg border border-emerald-100 mb-4",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Current Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AuthState.set_settings_current_password.debounce(
                                300
                            ),
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-indigo-600 outline-none",
                        ),
                        rx.el.label(
                            "New Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AuthState.set_settings_new_password.debounce(
                                300
                            ),
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-indigo-600 outline-none",
                        ),
                        rx.el.label(
                            "Confirm New Password",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            type="password",
                            placeholder="••••••••",
                            on_change=AuthState.set_settings_confirm_password.debounce(
                                300
                            ),
                            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg mb-6 focus:ring-2 focus:ring-indigo-600 outline-none",
                        ),
                        rx.el.button(
                            rx.cond(
                                AuthState.settings_loading,
                                "Updating...",
                                "Update Password",
                            ),
                            on_click=AuthState.change_password,
                            class_name="w-full bg-indigo-600 text-white font-medium py-2.5 rounded-lg hover:bg-indigo-700 transition-colors",
                        ),
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
            )
        ),
        "Settings",
    )