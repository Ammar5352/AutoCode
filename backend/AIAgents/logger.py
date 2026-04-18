from __future__ import annotations

import json
import logging
import os
from logging.handlers import WatchedFileHandler
from datetime import datetime, timezone
from typing import Any, MutableMapping, Optional


def _safe_json(data: Any) -> str:
    if isinstance(data, str):
        return data
    try:
        return json.dumps(data, ensure_ascii=False, default=str)
    except Exception:
        return str(data)


class SimpleLogger:
    def __init__(
        self,
        name: str = "autocode",
        log_dir: str = "/home/ammar/logdrive/logs/autocode",
        log_file: str = "autocode.log",
    ) -> None:
        self._logger = logging.getLogger(name)
        self._file_logging_enabled = False
        if not self._logger.handlers:
            formatter = logging.Formatter("%(message)s")

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

            try:
                effective_dir = os.getenv("AUTOCODE_LOG_DIR", log_dir)
                os.makedirs(effective_dir, exist_ok=True)
                file_path = os.path.join(effective_dir, log_file)
                file_handler = WatchedFileHandler(file_path)
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
                self._file_logging_enabled = True
            except Exception:
                # If the filesystem isn't writable, we still keep stdout logging.
                self._file_logging_enabled = False
        self._logger.setLevel(logging.INFO)

    def logit(
        self,
        logtype: str,
        prefix: str,
        data: Any,
        state: Optional[MutableMapping[str, Any]] = None,
    ) -> None:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        msg = f"{ts} | {logtype.upper()} -> {prefix} -> {_safe_json(data)}"
        level = logtype.upper()
        if level == "ERROR":
            self._logger.error(msg)
        elif level == "WARNING" or level == "WARN":
            self._logger.warning(msg)
        else:
            self._logger.info(msg)

        if state is not None:
            logs = state.get("logs")
            if not isinstance(logs, list):
                logs = []
                state["logs"] = logs
            logs.append({"ts": ts, "type": level, "prefix": prefix, "data": data})


logger = SimpleLogger()
