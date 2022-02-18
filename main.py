import pygame
import random
import os
from sudoku_boards import boards
from solve_sudoku import solve 
pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (112, 101, 214)

class GAME:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 365, 500
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku...")

        self.image = pygame.image.load(os.path.join('Assets', 'sudoku.png'))
        self.sound = pygame.mixer.Sound(os.path.join('Assets', 'game_end.mp3'))

        self.boxes = []
        self.check = []
        self.number = 0
        self.board = random.choice(boards)
        solve(self.board)
    

    def draw_or_not(self):
        for i in range(9):
            here = []
            for j in range(9):
                here.append(True)

            self.check.append(here)
        
        con = []
        while self.number:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            for number in con:
                if (i, j) == number:
                    continue
            self.check[i][j] = False
            con.append([i, j])
            self.number -= 1

              
    def set_boxes(self):
        x, y = 0, 0
        for i in range(9):
            x = 0 
            if i % 3 == 0:
                y += 1
            for j in range(9):
                if j % 3 == 0:
                    x += 1
                box = pygame.Rect(x, y, 38, 38)
                self.boxes.append(box)
                x += 40
            y += 40


    def draw_boxes(self):
        self.win.fill(WHITE)
        box = pygame.Rect(0, 0, 365, 1)
        for i in range(10):
            pygame.draw.rect(self.win, BLACK, box)
            if i % 3 == 0:
                box.y += 1
                pygame.draw.rect(self.win, BLACK, box)
            box.y += 40

        box = pygame.Rect(0, 0, 1, 365)
        for i in range(10):
            pygame.draw.rect(self.win,BLACK, box)
            if i % 3 == 0:
                box.x += 1
                pygame.draw.rect(self.win, BLACK, box)
            box.x += 40


    def draw_board(self):
        font = pygame.font.SysFont("comicsans", 20)
        index = 0
        for i in range(9):
            for j in range(9):
                if self.check[i][j]:
                    text = font.render(str(self.board[i][j]), 1, BLACK)
                    self.win.blit(text, (self.boxes[index].x + 15, self.boxes[index].y + 5))
                index += 1


    def draw_guess(self, text):
        font = pygame.font.SysFont("comicsans", 20)
        display_text = font.render(text, 1, BLACK)
        self.win.blit(display_text, (0, 400))
        pygame.display.update()


    def draw_time(self, seconds, pos, text):
        min = seconds // 60
        sec = seconds % 60
        timer = '{:02d}:{:02d}'.format(min, sec)
        dis_text = text + timer
        font = pygame.font.SysFont('freesansbold.ttf', 30)
        text = font.render(dis_text, 1, BLACK)
        self.win.blit(text, (pos[0], pos[1]))


    def draw_attempt(self, attempt):
        font = pygame.font.SysFont('freesansbold.ttf', 30)
        text = "Attempts: " + str(attempt)
        text = font.render(text, 1, RED)
        self.win.blit(text, (0, 380))


    def if_end(self):
        for i in range (9):
            for j in range(9):
                if not self.check[i][j]:
                    return False

        return True 


    def game_end(self, seconds, attempts):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        obj = GAME()
                        obj.play()
            
            self.win.fill(WHITE)
            font = pygame.font.SysFont('freesansbold.ttf', 50)
            text = font.render("You are Done!", 1, BLACK)
            self.win.blit(text, (self.WIDTH/2 - text.get_width()/2, self.HEIGHT/2 - text.get_height()/2))
            self.draw_time(seconds, (90, 300), "Time needed: ")
            font = pygame.font.SysFont('freesansbold.ttf', 30)
            text = "Attempts Done: " + str(attempts)
            text = font.render(text, 1, BLACK)
            self.win.blit(text, (90, 350))
            text = font.render("Press ENTER to play again.", 1, BLACK)
            self.win.blit(text, (self.WIDTH/2 - text.get_width()/2, 400))
            self.win.blit(self.image, (self.WIDTH/2 - self.image.get_width()/2, 100))
            pygame.display.update()
        
        pygame.quit()


    def draw_diff(self, box):
        self.win.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render("Choose Difficulty!", 1, WHITE)
        self.win.blit(text, (10, 100))
        self.win.blit(self.image, (self.WIDTH/2 - self.image.get_width()/2, 20))

        for i in range (3):
            pygame.draw.rect(self.win, WHITE, box[i])
        font = pygame.font.SysFont('comicsans', 20)
        text = font.render("EASY", 1, BLACK)
        self.win.blit(text, (box[0].x + 45, box[0].y + 15))
        text = font.render("MEDIUM", 1, BLACK)
        self.win.blit(text, (box[1].x + 30, box[1].y + 15))
        text = font.render("HARD", 1, BLACK)
        self.win.blit(text, (box[2].x + 45, box[2].y + 15))
        pygame.display.update()


    def set_difficulty(self):
        box = []
        button = pygame.Rect(110, 200, 150, 60)
        box.append(button)
        button = pygame.Rect(110, 300, 150, 60)
        box.append(button)
        button = pygame.Rect(110, 400, 150, 60)
        box.append(button)

        run = True 
        while run:
            self.draw_diff(box)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if box[0].collidepoint(m_x, m_y):
                    return 30
                if box[1].collidepoint(m_x, m_y):
                    return 40
                if box[2].collidepoint(m_x, m_y):
                    return 55

        pygame.quit()


    def play(self):
        FPS = 60
        clock = pygame.time.Clock()
        FRAMES = 0
        SECONDS = 0

        clicked = False, 0
        show = False
        text = ""
        number = 0
        attempt = 0

        self.number = self.set_difficulty()
        self.set_boxes()
        self.draw_or_not()

        run = True
        while run:
            clock.tick(FPS)
            if FRAMES == 60:
                SECONDS += 1
                FRAMES = 0

            FRAMES += 1

            self.draw_boxes()
            self.draw_board()
            self.draw_time(SECONDS, (250, 380), "Time: ")
            self.draw_attempt(attempt)
            if self.if_end():
                self.sound.play()
                self.game_end(SECONDS, attempt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    for i in range(81):
                        if self.boxes[i].collidepoint(m_x, m_y):
                            clicked = (True, i)
                            show = False
                            break
                
                if event.type == pygame.KEYDOWN and event.unicode.isdigit() and clicked[0]:
                    attempt += 1
                    show = True
                    number = int(event.unicode)
                    text = str(number)
                    
            
            if clicked[0]:
                if not self.check[clicked[1] // 9][clicked[1] % 9]:
                    box = pygame.Rect(self.boxes[clicked[1]].x , self.boxes[clicked[1]].y , 40, 40)
                    pygame.draw.rect(self.win, RED, box)
            
            if show and clicked[0]:
                font = pygame.font.SysFont("comicsans", 20)
                display_text = font.render(text, 1, BLACK)
                self.win.blit(display_text, (self.boxes[clicked[1]].x + 15, self.boxes[clicked[1]].y + 5))

                if number == self.board[clicked[1] // 9][clicked[1] % 9]:
                    self.check[clicked[1] // 9][clicked[1] % 9] = True
                    clicked = (False, 0)
                    show = False
                    self.draw_guess("Correct Guess!")
                    pygame.time.delay(2000)
                else:
                    self.draw_guess("Wrong Guess!")


            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    obj = GAME()
    obj.play()