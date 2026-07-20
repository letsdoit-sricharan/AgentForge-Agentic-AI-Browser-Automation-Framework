from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class SelectMovieStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "select_movie"

    @property
    def success_message(self) -> str:
        return "Movie selected successfully."