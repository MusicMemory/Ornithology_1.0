import random as r

from domain.BirdRepository import BirdRepository

MAX_ITERATIONS = 100

class Game:
    def __init__(self, no_birds, no_questions, no_answers, difficulty):
        self.__points = 0
        self.__no_answers = no_answers
        self.__questions = [None for i in range(no_questions)]
        self.__answers = [None for i in range(no_questions)]

        bird_repository = BirdRepository()
        for q in range(0, no_questions):
            # Liste __questions mit Zahlen (ID) füllen ohne Wiederholung
            counter = 0;
            while counter < MAX_ITERATIONS:
                bird_id_candidate = r.randint(0, no_birds - 1)
                bird_candidate = bird_repository.get_bird_by_id(bird_id_candidate)
                # Alle Vögel sollen die Schwierigkeit difficulty haben
                if not bird_id_candidate in self.__questions and bird_candidate.get_difficulty() == difficulty:
                    self.__questions[q] = bird_id_candidate
                    break;
                counter +=1
            # Wenn weniger Vögel da sind als gebraucht, würde das hier zu einer Exception führen:
            if (counter >= MAX_ITERATIONS):
                raise Exception("Probably there are not enough bird present with difficulty " + str(difficulty))
            # Liste __answers mit Zahlen (ID) füllen ohne Wiederholung
            # ohne gleichen Namen
            answer_list = []
            while len(answer_list) < no_answers:
                bird_id_candidate = r.randint(0, no_birds - 1)
                bird_name_candidate = bird_repository.get_bird_by_id(bird_id_candidate).get_name()
                if bird_name_candidate == bird_repository.get_bird_by_id(self.__questions[q]).get_name():
                    continue
                is_different = True
                for a in answer_list:
                    if bird_name_candidate == bird_repository.get_bird_by_id(a).get_name():
                        is_different = False
                        break;
                if is_different:
                    answer_list.append(bird_id_candidate)
            # richtige Antwort zufällig platzieren
            pos_right_answer = r.randint(0, no_answers - 1)
            answer_list[pos_right_answer] = self.__questions[q]
            self.__answers[q] = answer_list

        # Debug-Ausgabe der gewählen zu erratenden Bilder und der möglichen Antworten
        image_cnt = 0
        for answer_set in self.__answers:
            print(str(image_cnt+1) + ". Image", self.__questions[image_cnt], "-> Answers", answer_set)
            image_cnt += 1

    def get_question(self, q):
        return self.__questions[q], self.__answers[q]

    def is_correct(self, q, a):
        correct = self.__questions[q] == self.__answers[q][a]
        print("Answer: ", a, ", correct:", correct)
        return correct

    def add_points(self, points):
        self.__points += points
        print("Points: ", self.__points)

    def get_points(self):
        return self.__points
