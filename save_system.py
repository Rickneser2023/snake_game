import json
import os
from settings import SAVE_FILE

class SaveSystem:
    @staticmethod
    def save_game(data):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error guardando: {e}")

    @staticmethod
    def load_game():
        if not os.path.exists(SAVE_FILE):
            return {"level": 1, "score": 0, "highscore": 0}
        
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando: {e}")
            return {"level": 1, "score": 0, "highscore": 0}

    @staticmethod
    def update_highscore(new_score):
        data = SaveSystem.load_game()
        if new_score > data.get("highscore", 0):
            data["highscore"] = new_score
            SaveSystem.save_game(data)
            return True
        return False
