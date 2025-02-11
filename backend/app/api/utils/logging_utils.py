from emoji import emojize


class LogMessageEmojis:
    def __init__(self) -> None:
        self._emojis: dict[str, str] = {
            "incoming_request": emojize(":inbox_tray:"),
            "request_method": emojize(":stop_sign:"),
            "request_headers": emojize(":satellite:"),
            "request_body": emojize(":memo:"),
            "response": emojize(":outbox_tray:"),
            "process_time": emojize(":hourglass_done:"),
        }

    def get_emoji(self, key: str) -> str:
        if key in self._emojis:
            return self._emojis[key]
        else:
            raise KeyError(f"Emoji not found for key: {key}")

    def get_response_status_emoji(self, status_code: int) -> str:
        if 100 <= status_code < 200:
            return emojize(":double_exclamation_mark:")  # 1xx - Informational
        elif 200 <= status_code < 300:
            return emojize(":check_mark_button:")  # 2xx - Success
        elif 300 <= status_code < 400:
            return emojize(":right_arrow_curving_left:")  # 3xx - Redirection
        elif 400 <= status_code < 500:
            return emojize(":warning:")  # 4xx - Client error
        else:
            return emojize(":cross_mark:")  # 5xx - Server error
