import csv
import json
import os
from typing import Generator, List
from models import Character, Scene


class DataStorage:
    @staticmethod
    def load_scenes_from_csv(file_path: str) -> List[Scene]:
        """
        Импортирует данные из CSV с помощью модуля csv (требование проекта).
        Преобразование: чтение -> проверка -> преобразование.
        """
        scenes = []
        if not os.path.exists(file_path):
            return scenes

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Проверка и преобразование типов 
                try:
                    scene_id = int(row["scene_id"])
                    text = row["text"]
                    choice_1 = row["choice_1"]
                    next_scene_1 = int(row["next_scene_1"])
                    choice_2 = row["choice_2"]
                    next_scene_2 = int(row["next_scene_2"])
                    
                    scene = Scene(
                        scene_id=scene_id,
                        text=text,
                        choice_1=choice_1,
                        next_scene_1=next_scene_1,
                        choice_2=choice_2,
                        next_scene_2=next_scene_2
                    )
                    scenes.append(scene)
                except (ValueError, KeyError) as e:
                    print(f"Ошибка при обработке строки CSV: {e}")
        return scenes

    @staticmethod
    def lazy_load_scenes(file_path: str) -> Generator[Scene, None, None]:
        """
        Генератор для ленивой обработки последовательности записей (требование проекта).
        Не загружает весь файл в память целиком, а выдает по одной сцене.
        """
        if not os.path.exists(file_path):
            return

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield Scene(
                    scene_id=int(row["scene_id"]),
                    text=row["text"],
                    choice_1=row["choice_1"],
                    next_scene_1=int(row["next_scene_1"]),
                    choice_2=row["choice_2"],
                    next_scene_2=int(row["next_scene_2"])
                )

    @staticmethod
    def save_game_to_json(file_path: str, session_data: dict) -> None:
        """
        Сохраняет текущее состояние в JSON с помощью модуля json (требование проекта).
        """
        with open(file_path, mode="w", encoding="utf-8") as file:
            json.dump(session_data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_game_from_json(file_path: str) -> dict:
        """
        Загружает сохраненное состояние из JSON после перезапуска.
        """
        if not os.path.exists(file_path):
            return {}
        
        with open(file_path, mode="r", encoding="utf-8") as file:
            return json.load(file)