import json
import os
from settings import SAVE_FILE

DEFAULT_SAVE_DATA = {
    "level": 1,
    "score": 0,
    "highscore": 0,
    "max_level": 1,
    "total_games": 0,
    "foods_eaten": 0,
    "best_combo": 0,
    "last_score": 0,
    "last_level": 1,
    "last_combo": 0,
}

class SaveSystem:
    @staticmethod
    def save_game(data):
        try:
            os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error guardando: {e}")

    @staticmethod
    def load_game():
        if not os.path.exists(SAVE_FILE):
            return DEFAULT_SAVE_DATA.copy()
        
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                merged = DEFAULT_SAVE_DATA.copy()
                if isinstance(data, dict):
                    merged.update(data)
                return merged
        except Exception as e:
            print(f"Error cargando: {e}")
            return DEFAULT_SAVE_DATA.copy()

    @staticmethod
    def update_highscore(new_score):
        data = SaveSystem.load_game()
        if new_score > data.get("highscore", 0):
            data["highscore"] = new_score
            SaveSystem.save_game(data)
            return True
        return False

    @staticmethod
    def record_run(score, level, best_combo, foods_eaten):
        data = SaveSystem.load_game()
        data["total_games"] = data.get("total_games", 0) + 1
        data["last_score"] = score
        data["last_level"] = level
        data["last_combo"] = best_combo
        data["score"] = score
        data["level"] = level
        data["foods_eaten"] = data.get("foods_eaten", 0) + foods_eaten
        data["max_level"] = max(data.get("max_level", 1), level)
        data["best_combo"] = max(data.get("best_combo", 0), best_combo)
        data["highscore"] = max(data.get("highscore", 0), score)
        SaveSystem.save_game(data)
        return data
