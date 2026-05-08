import reflex as rx
import hashlib
import secrets
import logging
from typing import TypedDict


class UserData(TypedDict):
    id: str
    name: str
    email: str
    password_hash: str
    salt: str
    role: str


MOCK_USERS_DB: dict[str, UserData] = {}


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()


class AuthState(rx.State):
    current_user_id: str = ""
    current_user_name: str = ""
    current_user_email: str = ""
    current_user_role: str = ""
    is_authenticated: bool = False
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    login_loading: bool = False
    reg_name: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_confirm_password: str = ""
    reg_role: str = "Member"
    reg_error: str = ""
    reg_loading: bool = False
    mobile_sidebar_open: bool = False
    settings_current_password: str = ""
    settings_new_password: str = ""
    settings_confirm_password: str = ""
    settings_error: str = ""
    settings_success: str = ""
    settings_loading: bool = False

    @rx.event
    def toggle_mobile_sidebar(self):
        self.mobile_sidebar_open = not self.mobile_sidebar_open

    @rx.event
    def set_settings_current_password(self, val: str):
        self.settings_current_password = val

    @rx.event
    def set_settings_new_password(self, val: str):
        self.settings_new_password = val

    @rx.event
    def set_settings_confirm_password(self, val: str):
        self.settings_confirm_password = val

    @rx.event
    async def change_password(self):
        self.settings_loading = True
        self.settings_error = ""
        self.settings_success = ""
        yield
        if len(self.settings_new_password) < 8:
            self.settings_error = "New password must be at least 8 characters."
            self.settings_loading = False
            return
        if self.settings_new_password != self.settings_confirm_password:
            self.settings_error = "Passwords do not match."
            self.settings_loading = False
            return
        self.settings_success = "Password updated successfully!"
        self.settings_loading = False
        self.settings_current_password = ""
        self.settings_new_password = ""
        self.settings_confirm_password = ""
        yield rx.toast("Password updated!")

    @rx.event
    def set_login_email(self, email: str):
        self.login_email = email

    @rx.event
    def set_login_password(self, password: str):
        self.login_password = password

    @rx.event
    def set_reg_name(self, name: str):
        self.reg_name = name

    @rx.event
    def set_reg_email(self, email: str):
        self.reg_email = email

    @rx.event
    def set_reg_password(self, password: str):
        self.reg_password = password

    @rx.event
    def set_reg_confirm_password(self, password: str):
        self.reg_confirm_password = password

    @rx.event
    def set_reg_role(self, role: str):
        self.reg_role = role

    @rx.event
    async def login(self):
        self.login_loading = True
        self.login_error = ""
        yield
        try:
            user = MOCK_USERS_DB.get(self.login_email)
            if not user:
                self.login_error = "Invalid email or password."
                self.login_loading = False
                return
            expected_hash = hash_password(self.login_password, user["salt"])
            if user["password_hash"] != expected_hash:
                self.login_error = "Invalid email or password."
                self.login_loading = False
                return
            self.current_user_id = user["id"]
            self.current_user_name = user["name"]
            self.current_user_email = user["email"]
            self.current_user_role = user["role"]
            self.is_authenticated = True
            self.login_loading = False
            yield rx.redirect("/dashboard")
            return
        except Exception as e:
            logging.exception(f"Login error: {e}")
            self.login_error = "An unexpected error occurred."
            self.login_loading = False

    @rx.event
    async def register(self):
        self.reg_loading = True
        self.reg_error = ""
        yield
        try:
            if not self.reg_name or len(self.reg_name) < 2:
                self.reg_error = "Name must be at least 2 characters."
                self.reg_loading = False
                return
            if not self.reg_email or "@" not in self.reg_email:
                self.reg_error = "Please enter a valid email."
                self.reg_loading = False
                return
            if len(self.reg_password) < 8:
                self.reg_error = "Password must be at least 8 characters."
                self.reg_loading = False
                return
            if self.reg_password != self.reg_confirm_password:
                self.reg_error = "Passwords do not match."
                self.reg_loading = False
                return
            if self.reg_email in MOCK_USERS_DB:
                self.reg_error = "Email is already registered."
                self.reg_loading = False
                return
            salt = secrets.token_hex(8)
            pwd_hash = hash_password(self.reg_password, salt)
            user_id = secrets.token_hex(4)
            MOCK_USERS_DB[self.reg_email] = {
                "id": user_id,
                "name": self.reg_name,
                "email": self.reg_email,
                "password_hash": pwd_hash,
                "salt": salt,
                "role": self.reg_role,
            }
            self.reg_loading = False
            yield rx.redirect("/login")
            return
        except Exception as e:
            logging.exception(f"Registration error: {e}")
            self.reg_error = "An unexpected error occurred."
            self.reg_loading = False

    @rx.event
    def logout(self):
        self.current_user_id = ""
        self.current_user_name = ""
        self.current_user_email = ""
        self.current_user_role = ""
        self.is_authenticated = False
        return rx.redirect("/login")

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")