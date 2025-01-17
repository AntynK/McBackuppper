from pathlib import Path

import flet as ft

from data.settings import Settings
from data.dialogs.dialog import Dialog
from data.path_utils import is_mc_folder, get_top_dir
from data.controls.path_field import PathField
from data.controls.select_language_dropdown import SelectLanguageDropdown
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.DIALOGS)


class ChangeSettings(Dialog):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page=page, title=_("Settings"))
        self.backups_folder_field = PathField(label=_("Backups folder"), page=page)
        self.mc_folder_field = PathField(label=_("Minecraft folder"), page=page)
        self.pool_size_entry = ft.TextField(label=_("Pool size"))
        self.select_language_dropdown = SelectLanguageDropdown(label=_("Language"))

        self.content = ft.Column(
            [
                self.backups_folder_field,
                self.mc_folder_field,
                self.pool_size_entry,
                self.select_language_dropdown,
                ft.Text(_("NOTE: language will change after a restart"), weight=ft.FontWeight.BOLD)
            ]
        )

        self.actions = [
            ft.TextButton(_("Save"), on_click=self.save),
            ft.TextButton(_("Cancel"), on_click=self.close),
        ]

    def save(self, event=None) -> None:
        if not self._validate_backup_folder_path():
            return

        if not self._validate_mc_folder_path():
            return

        if not self._validate_pool_size():
            return

        Settings().update_language(self.select_language_dropdown.value)  # type: ignore

        self.close()

    def show(self, event=None) -> None:
        super().show(event)
        self._update_fields_value()
        self.update()

    def _update_fields_value(self):
        self.backups_folder_field.path = str(Settings().get_backup_folder())
        self.backups_folder_field.remove_error()

        self.mc_folder_field.path = str(Settings().get_mc_folder())
        self.backups_folder_field.remove_error()

        self.pool_size_entry.value = str(Settings().get_pool_size())
        self.pool_size_entry.error_text = ""

        self.select_language_dropdown.value = Settings().get_language()

    def _validate_backup_folder_path(self) -> bool:
        backup_folder = Path(self.backups_folder_field.path)  # type: ignore
        if not get_top_dir(backup_folder).is_dir():
            self.backups_folder_field.set_error(_("Wrong path"))
            return False

        Settings().update_backup_folder(backup_folder)
        self.backups_folder_field.remove_error()
        return True

    def _validate_mc_folder_path(self) -> bool:
        mc_folder = Path(self.mc_folder_field.path)  # type: ignore
        if not is_mc_folder(mc_folder):
            self.mc_folder_field.set_error(_("Wrong path"))
            return False
        Settings().update_mc_folder(mc_folder)
        self.mc_folder_field.remove_error()
        return True

    def _validate_pool_size(self) -> bool:
        try:
            pool_size = int(self.pool_size_entry.value)  # type: ignore
            if pool_size <= 0:
                raise ValueError()
        except ValueError:
            self.pool_size_entry.error_text = _("Wrong size")
            self.pool_size_entry.update()
            return False
        self.pool_size_entry.error_text = ""
        self.pool_size_entry.update()
        Settings().update_pool_size(pool_size)
        return True
