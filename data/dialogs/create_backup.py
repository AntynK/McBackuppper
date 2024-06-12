from typing import Callable

import flet as ft

from data.backup_manager import Backup
from data.dialogs.dialog import Dialog
from data.controls.backup_entry import BackupEntry


class CreateBackupDialog(Dialog):
    def __init__(
        self, page: ft.Page, world_name: str, after_completion: Callable
    ) -> None:
        super().__init__(page=page, title="Create backup")
        self.backup_entry = BackupEntry(Backup(name=world_name))

        self.content = ft.Column([self.backup_entry], expand=True)

        self.actions = [
            ft.TextButton("Create", on_click=self.create),
            ft.TextButton("Cancel", on_click=self.close),
        ]
        self.after_completion = after_completion

    def create(self, event=None) -> None:
        self.after_completion(self.backup_entry.get_backup())
        self.close()
