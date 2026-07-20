from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class SearchMovieStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "search_movie"

    @property
    def success_message(self) -> str:
        return "Movie searched successfully."