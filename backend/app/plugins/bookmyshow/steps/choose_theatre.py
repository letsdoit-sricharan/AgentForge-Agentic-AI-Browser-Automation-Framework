from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseTheatreStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "choose_theatre"

    @property
    def success_message(self) -> str:
        return "Theatre selected successfully."