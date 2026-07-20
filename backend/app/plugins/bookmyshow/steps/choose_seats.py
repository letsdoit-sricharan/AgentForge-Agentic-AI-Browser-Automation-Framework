from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class ChooseSeatsStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "choose_seats"

    @property
    def success_message(self) -> str:
        return "Seats selected successfully."