import os
from models import GameSession, Character
from storage import DataStorage
from ui import ConsoleUI

def main():
    ConsoleUI.show_welcome()
    
    # Запрос имени игрока
    player_name = input("Введите имя вашего главного героя: ").strip() or "Странник"
    session = GameSession(player_name)
    
    
    if not os.path.exists("data"):
        os.makedirs("data")
        
    # Пути к файлам данных
    csv_path = "data/scenes.csv"
    json_path = "data/save.json"
    
    # сцены из CSV 
    scenes = DataStorage.load_scenes_from_csv(csv_path)
    if scenes:
        for scene in scenes:
            session.add_scene(scene)
        print(f"[Успех] Загружено сцен из CSV: {len(scenes)}")
    else:
        print(f"[Внимание] Файл {csv_path} не найден или пуст. Создайте его для полноценной игры.")
        
    
    session.add_character(Character("Эльза", 12, "Дружелюбна"))
    session.add_character(Character("Страж ворот", 3, "Настороже"))
    session.add_character(Character("Таинственный незнакомец", 25, "Интригует"))

   
    saved_data = DataStorage.load_game_from_json(json_path)
    if saved_data:
        choice_load = input("Найдено сохранение игры. Хотите загрузить прогресс? (y/n): ").strip().lower()
        if choice_load == 'y':
            session.current_scene_id = saved_data.get("current_scene_id", 1)
            session.inventory = saved_data.get("inventory", [])
            print("[Успех] Прогресс успешно восстановлен из JSON!")

    # Главный цикл программы
    while True:
        action = ConsoleUI.main_menu()
        
        if action == "1":
            # Игровой процесс
            current_scene = None
            for s in session.scenes:
                if s.scene_id == session.current_scene_id:
                    current_scene = s
                    break
            
            if not current_scene:
                print(f"\n[Ошибка] Сцена с ID {session.current_scene_id} не найдена в базе данных!")
                print("Попробуйте добавить сцены в файл scenes.csv или выберите другой пункт.")
                continue
            
            print(f"\n--- СЦЕНА #{current_scene.scene_id} ---")
            print(current_scene.text)
            print(f"  [1] {current_scene.choice_1}")
            print(f"  [2] {current_scene.choice_2}")
            
            choice_step = input("Сделайте выбор (1 или 2, либо 'q' для выхода в меню): ").strip()
            if choice_step == "1":
                session.current_scene_id = current_scene.next_scene_1
            elif choice_step == "2":
                session.current_scene_id = current_scene.next_scene_2
            elif choice_step.lower() == 'q':
                continue
            else:
                print("Неверный ввод. Возвращаем в меню.")

        elif action == "2":
            
            keyword = input("Введите ключевое слово для поиска по тексту сцен: ").strip()
            found_scenes = session.search_scene_by_keyword(keyword)
            print(f"\nРезультаты поиска (найдено: {len(found_scenes)}):")
            for sc in found_scenes:
                print(f" -> Сцена #{sc.scene_id}: {sc.text}")

        elif action == "3":
             
            sorted_chars = session.sort_characters_by_sympathy()
            print("\n--- СПИСОК ПЕРСОНАЖЕЙ (отсортировано по симпатии) ---")
            for char in sorted_chars:
                print(f"• {char.name} (Симпатия: {char.sympathy_points}) — Статус: {char.status}")
                
                print(f"  Действие: {char.interact()}")

        elif action == "4":
            # Сохранение
            game_state = {
                "player_name": session.player_name,
                "current_scene_id": session.current_scene_id,
                "inventory": session.inventory
            }
            DataStorage.save_game_to_json(json_path, game_state)
            print("[Успех] Игра сохранена в JSON-файл!")

        elif action == "5":
            print("Спасибо за игру! До свидания!")
            break
        else:
            print("Неверный пункт меню. Пожалуйста, выберите от 1 до 5.")

if __name__ == "__main__":
    main()