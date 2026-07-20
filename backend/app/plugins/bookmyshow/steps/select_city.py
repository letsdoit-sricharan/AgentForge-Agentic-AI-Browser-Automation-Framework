# Step to select city
from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class SelectCityStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "select_city"

    @property
    def success_message(self) -> str:
        return "City selected successfully."