from dataclasses import dataclass, field
from typing import List, Protocol

#протокол интерактивных объектов
class Interactable(Protocol):
    def interact(self) -> str:
        ...

#объект персонажа 
@dataclass
class Character:
    name: str
    sympathy_points: int = 0
    status: str = "Нейтрально"

    def interact(self) -> str:
        """Полиморфный метод для взаимодействия с персонажем"""
        return f"Вы общаетесь с персонажем {self.name}. Уровень симпатии: {self.sympathy_points}."


@dataclass
class GameItem:
    name: str
    description: str

    def interact(self) -> str:
        """Полиморфный метод для взаимодействия с предметом"""
        return f"Вы осматриваете предмет '{self.name}': {self.description}"


#Класс Сцены
@dataclass
class Scene:
    scene_id: int
    text: str
    choice_1: str
    next_scene_1: int
    choice_2: str
    next_scene_2: int


#класс игровой сессии
class GameSession:
    def __init__(self, player_name: str):
        self.player_name: str = player_name
        self.current_scene_id: int = 1
        self.inventory: List[str] = []
        self.characters: List[Character] = []
        self.scenes: List[Scene] = []

    def add_scene(self, scene: Scene) -> None:
        self.scenes.append(scene)

    def add_character(self, character: Character) -> None:
        self.characters.append(character)

    #АЛГОРИТМ ПОИСКА
    def search_scene_by_keyword(self, keyword: str) -> List[Scene]:
        """
        Линейный поиск сцен по ключевому слову в тексте.
        Сложность по времени: O(N), где N — количество сцен.
        Сложность по памяти: O(K), где K — количество найденных сцен.
        """
        results = []
        for scene in self.scenes:
            if keyword.lower() in scene.text.lower():
                results.append(scene)
        return results

    #АЛГОРИТМ СОРТИРОВКИ
    def sort_characters_by_sympathy(self) -> List[Character]:
        """
        Сортировка персонажей пузырьком (Bubble Sort) по очкам симпатии (по убыванию).
        Написана вручную, без использования встроенного .sort().
        Сложность по времени: O(N^2), где N — количество персонажей.
        """
        #копия списка
        chars = list(self.characters)
        n = len(chars)
        for i in range(n):
            for j in range(0, n - i - 1):
                if chars[j].sympathy_points < chars[j + 1].sympathy_points:
                    
                    chars[j], chars[j + 1] = chars[j + 1], chars[j]
        return chars