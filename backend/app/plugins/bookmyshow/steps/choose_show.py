from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseShowStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "choose_show"

    @property
    def success_message(self) -> str:
        return "Show selected successfully."