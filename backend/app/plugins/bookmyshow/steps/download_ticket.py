from __future__ import annotations

from app.plugins.bookmyshow.steps.base_step import BaseBookMyShowStep


class DownloadTicketStep(BaseBookMyShowStep):

    @property
    def name(self) -> str:
        return "download_ticket"

    @property
    def success_message(self) -> str:
        return "Ticket downloaded successfully."