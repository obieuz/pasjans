import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional


class LeaderboardManager:
    DEFAULT_FILE_PATH = Path("leaderboard.json")
    MAX_ENTRIES = 10

    def __init__(self, filepath: Optional[Path] = None, max_entries: Optional[int] = None):
        self.filepath = filepath if filepath is not None else self.DEFAULT_FILE_PATH
        self.max_entries = max_entries if max_entries is not None else self.MAX_ENTRIES
        self.leaderboard_data: List[Dict] = self._load()

    def _load(self):
        if not self.filepath.exists():
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.leaderboard_data, f, indent=4, ensure_ascii=False)
        except IOError:
            print(f"Błąd: Nie można zapisać leaderboardu do pliku {self.filepath}")
            pass

    def get_scores(self) -> List[Dict]:
        return self._load()


    def add_score(self, nickname: str, moves: int, time_seconds: int) -> bool:
        new_score_entry = {
            "nickname": nickname,
            "moves": moves,
            "time_seconds": time_seconds,
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds')
        }
        self.leaderboard_data.append(new_score_entry)

        self.leaderboard_data.sort(key=lambda x: (x.get("moves", float('inf'))))

        self.leaderboard_data = self.leaderboard_data[:self.max_entries]

        self._save()

        return any(entry is new_score_entry for entry in self.leaderboard_data)

    @staticmethod
    def format_time(seconds: int) -> str:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"