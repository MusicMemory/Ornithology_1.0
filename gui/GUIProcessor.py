import pygame
from pygame.rect import Rect

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
alertbox_size = (300, 50)
answer_height = 40

class GUIProcessor:
    def __init__(self, width, height, no_answers):
        self.screen = screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.no_answer_lines = no_answers // 2
        self.margin_left = width // 10
        self.margin_top = height // 10
        self.margin_right = self.margin_left
        self.margin_bottom = width // 15
        self.width_minus_margins  = self.width - self.margin_left - self.margin_right
        self.height_minus_margins = self.height - self.margin_top - self.margin_bottom
        self.image_size = (self.width_minus_margins, self.width_minus_margins * 3 // 4)
        self.image_pos = (self.margin_left, self.margin_top)
        self.dist_image_to_alertbox = self.height_minus_margins // 30
        self.dist_alertbox_to_text = self.height_minus_margins // 25
        self.alertbox_pos = ((self.width - alertbox_size[0]) / 2, self.margin_top + self.image_size[1] + self.dist_image_to_alertbox)
        self.text_margin_top = self.margin_top + self.image_size[1] + self.dist_image_to_alertbox + alertbox_size[1] + self.dist_alertbox_to_text
        self.answer_dist = self.width_minus_margins // 5
        self.answer_width = (self.width_minus_margins - self.answer_dist) // 2

        self.font_answer = pygame.font.SysFont('Comic Sans MS', 30)
        self.font_correct = pygame.font.SysFont('Comic Sans MS', 40)
        self.font_start = pygame.font.SysFont('Comic Sans MS',30)
        self.font_header = pygame.font.SysFont('Comic Sans MS', 50)

    def clear(self):
        self.screen.fill(black)

    def clear_by_color(self,color):
        self.screen.fill(color)

    def set_logo(self,logo):
        rect = logo.get_rect()
        #x zentriert
        w = rect.width//2
        self.screen.blit(logo, (self.width // 2 - w, 50))

    def set_image(self, image):
        image_scaled = pygame.transform.scale(image, self.image_size)
        average_color = pygame.transform.average_color(image_scaled)
        self.clear_by_color(average_color)
        self.screen.blit(image_scaled, self.image_pos)

    def set_nth_text(self,n,text):
        textsurface = self.font_answer.render(str(n+1) + '. ' + text, True, white)
        rest_space_box_to_bottom = self.height - self.margin_bottom - self.text_margin_top
        answer_height = rest_space_box_to_bottom // self.no_answer_lines
        text_y = self.text_margin_top + n // 2 * answer_height
        if (n % 2 == 0):
            self.screen.blit(textsurface,(self.margin_left, text_y))
        else:
            self.screen.blit(textsurface,(self.margin_left + self.answer_dist +  self.answer_width, text_y))

    def alert(self, trueOrFalse, points):
        x = self.alertbox_pos[0]
        y = self.alertbox_pos[1]
        text = "Richtig" if trueOrFalse else "Falsch"
        color = green if trueOrFalse else red
        pygame.draw.rect(self.screen, color, Rect((x, y), alertbox_size))
        textsurface = self.font_correct.render(text, True, white)
        self.screen.blit(textsurface, (self.width / 2 - 45, y + alertbox_size[1] // 2 - 12))

    def show_final_page(self, sum_points):
        self.screen.fill(black)
        text = "Sie haben " + str(sum_points) + " Punkte erreicht."
        textsurface = self.font_correct.render(text, True, white)
        self.screen.blit(textsurface,(self.width // 2 - 200, self.height * 2//5))
        text = "Möchten Sie noch einmal spielen (j/n)?"
        textsurface = self.font_correct.render(text, True, white)
        self.screen.blit(textsurface,(self.width // 2 - 260, self.height * 3//5))

    def show_start_page(self):
        self.screen.fill(black)
        self.printTextRel("Ornithology", self.font_header, white, (0, 0))
        image = pygame.image.load("images/niclas.jpg")
        image_scaled = pygame.transform.scale(image, (self.width*3//5, self.width*3//5))
        self.screen.blit(image_scaled, (self.width*1//5, self.width//5))
        self.printTextRel("Wählen Sie die Schwierigkeit auf der Tastatur (1 - 3)", self.font_start, white, (0, 90))

    def update(self):
        pygame.display.update()

    def printTextRel(self, text, font, color, percentCoord):
        textsurface = font.render(text, True, color)
        absCoord = self.percentToAbs(percentCoord)
        self.screen.blit(textsurface, absCoord)

    def percentToAbs(self, percentCoord):
        absX = self.margin_left + percentCoord[0] * self.width_minus_margins // 100
        absY = self.margin_top +  percentCoord[1] * self.height_minus_margins // 100
        return (absX, absY)
