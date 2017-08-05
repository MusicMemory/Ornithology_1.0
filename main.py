import pygame
import sys

from domain.BirdRepository import BirdRepository
from domain.Game import Game
from domain.ImageRepository import ImageRepository
from gui.GUIProcessor import GUIProcessor


# Wartet darauf, dass eine Taste gedrückt wird, die sich auch in Bezug auf
# key_map mappen lässt. Falls key_map die Taste enthält, wird der gemappte
# Wert zurückgegeben.
def wait_on_key_and_map(key_map):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                try:
                    return key_map[event.key]
                except:
                    None
        pygame.time.wait(100)


pygame.init()
display_width = 700
display_height = 700
no_questions = 10
no_answers = 4


key_map_difficulty = {
    pygame.K_1 : 1,
    pygame.K_2 : 2,
    pygame.K_3 : 3,
}

key_map_answer = {
    pygame.K_1 : 0,
    pygame.K_2 : 1,
    pygame.K_3 : 2,
    pygame.K_4 : 3,
    pygame.K_5 : 4,
    pygame.K_6 : 5,
    pygame.K_7 : 6,
    pygame.K_8 : 7,
}

key_map_again = {
    pygame.K_j : True,
    pygame.K_n : False,
    pygame.K_ESCAPE : False
}

print("Start of Ornithologie")
bird_repository = BirdRepository("birds.csv")
image_repository = ImageRepository("images")
gui_processor = GUIProcessor(display_width, display_height, no_answers)
# clock = pygame.time.Clock()

again = True
while again:
    # Startseite mit der Schwierigkeitsauswahl:
    gui_processor.show_start_page()
    gui_processor.update()

    difficulty = wait_on_key_and_map(key_map_difficulty)
    print("difficulty = ", difficulty)

    # Spiel:
    game = Game(bird_repository.no_birds(),no_questions,no_answers,difficulty)
    for q in range(no_questions):
        question,answers = game.get_question(q)
        bird = bird_repository.get_bird_by_id(question)
        image = image_repository.load_image(bird.get_filename())
        gui_processor.clear()
        gui_processor.set_image(image)
        for a in range(len(answers)):
            bird_answer = bird_repository.get_bird_by_id(answers[a])
            gui_processor.set_nth_text(a,bird_answer.get_name())

        gui_processor.update()

        answer = -1;
        while answer < 0 or answer >= no_answers:
            answer = wait_on_key_and_map(key_map_answer)

        if game.is_correct(q,answer):
            game.add_points(bird.get_difficulty())
            gui_processor.alert(True, bird.get_difficulty())
        else:
            gui_processor.alert(False, 0)

        gui_processor.update()
        pygame.event.get()
        pygame.time.wait(500)

    # Punktestand anzeigen:
    gui_processor.show_final_page(game.get_points())
    gui_processor.update()

    again = wait_on_key_and_map(key_map_again)
    print("again = ", again)

pygame.quit()
sys.exit()

