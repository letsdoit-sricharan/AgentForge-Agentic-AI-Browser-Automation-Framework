from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseDateStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "choose_date"

    @property
    def success_message(self) -> str:
        return "Show date selected successfully."