from pygame import*
from random import randint, choice

folder = "files/"
enemy_file = ["_1.png","_2.png","_3.png","_4.png"]

height = 500
width = 700
limit_rocket = 10
limit_enemy = 10
limit_score = 100
limit_life = 9
мах_speed = 2

class Game_Sprite:
    def __init__(self, filename, x, y, speed, size_x, size_y):
        self.speed = speed
        self.image = transform.scale(image.load(filename),(size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.life = 1
        self.score = 0   
         
    def is_colide(self, border):
         return self.rect.colliderect(border.rect) 
    
    def is_collide_enemy(self):
        for enemy in enemys:
            if self.rect.colliderect(enemy.rect):
                player.score += 1 
                sound_score.play() 
                enemys.remove(enemy)
                rockets.remove(self)
                break
                     
     
    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  
                   
    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= self.speed
                          
    def move_right(self):   
        if self.rect.x < width - self.size_x:
            self.rect.x += self.speed 
        
             
    def launch_rocket(self):
        if len(rockets) < limit_rocket :
            rocket = Game_Sprite(folder + "rocket.png", self.rect.x + self.size_x / 3, self.rect.y, 5, 7, 21)
            rockets.append(rocket)
            sound_lanch.play() 
             
def move_rockets():    
        for rocket in rockets:
            rocket.is_collide_enemy()
            #rockets.remove(rocket)      
            if rocket.rect.y < 10 and rocket in rockets:  #- rocket.size_y: проверить     
                rockets.remove(rocket) 
            else:    
                rocket.rect.y -= rocket.speed
            
def draw_rockets():
    for rocket in rockets:
        window.blit(rocket.image, (rocket.rect.x, rocket.rect.y))

 
def create_enemy(n):
    for i in range(n):
        if len(enemys) < limit_enemy:
            size = randint(30, 80)
            speed = randint(1, мах_speed)
            enemy = Game_Sprite(folder + choice(enemy_file),  randint(0, width - 50), randint(-90, 10), speed , size, size)
            enemys.append(enemy) 
        
def move_enemys():    
    global enemy_score
    for enemy in enemys:
        enemy.rect.y += enemy.speed #+ randint(-1,0) 
        #enemy.rect.x += randint(-3,3)  
        if enemy.rect.y > height:
            enemys.remove(enemy)
            enemy_score +=1
            sound_loser.play() 
        if enemy.is_colide(player):
            sound_boom.play() 
            player.life -=1
            player.score +=1
            enemys.remove(enemy)
            life_labels.pop(len(life_labels)-1)
            break   
                                        
def draw_enemys():
    for enemy in enemys:
        window.blit(enemy.image, (enemy.rect.x, enemy.rect.y))  

def info(x, y, string, size=75, color=(100,100,100)):
    font1 = font.SysFont('Comic Sans MS', size)
    text1 = font1.render(string, True, color)
    place = text1.get_rect(center=(x, y))
    window.blit(text1, place) 

def draw_info_string():
    #info(100, height - 10, "Залишилось котожиттів " + str(player.life), size=15, color=(250,250,50))
    # 1 верхня, або 2 наступних
    #life_string =  "@ " * player.life 
    #info(150, height - 10, life_string, size=15, color=(250,250,50))
    info(350, height - 10, "Знищено монстрів " + str(player.score), size=15, color=(250,150,150))
    info(550, height - 10, "Пропущено монстрів " + str(enemy_score), size=15, color=(250,50,250))


def label_life():
    for i in range(limit_life):
        life_label = Game_Sprite(folder + "_cat.png", 25 * i, height - 25, 0, 20, 25)
        life_labels.append(life_label)
           
def draw_life():
    for label in life_labels:
        label.draw_sprite()
    
        
def wait_key(key):  
    global game
    wait = True
    while wait:
        for e in event.get():
            if e.type == QUIT:
                wait = False
                break   
            elif e.type == KEYDOWN:
                if e.key == key:
                    wait = False
                    break 

def pause_game():
    info(width * 0.5, height  * 0.5, "Для продовження гри натисни - SPACE", size=35, color=(0,250,250))
    display.update()
    wait_key(K_SPACE)
                    
def rule_game():
    info(width * 0.5, height  * 0.3, "ПРАВИЛА ГРИ", size=40, color=(250,250,0))
    info(width * 0.5, height  * 0.40, "Рух котика - стрілки RIGHT, LEFT " , size=25, color=(250,250,0))
    info(width * 0.5, height  * 0.45, "Стрільба  - SPACE " , size=25, color=(250,250,0))
    info(width * 0.5, height  * 0.5, "Пауза - P         " , size=25, color=(250,250,0))
    info(width * 0.5, height  * 0.55, "Вихід з гри - Q   " , size=25, color=(250,250,0))
    info(width * 0.5, height  * 0.7, "Для продовження гри натисни - SPACE", size=15, color=(250,250,250))
    display.update()
    wait_key(K_SPACE)
    
def game_over():
    #background = transform.scale(image.load(folder + "_fon.jpg"), (width, height))
    #window.blit(background, (0,0))
    info(width * 0.5, height  * 0.3, "ГРУ ЗАКІНЧЕНО", size=70, color=(250,250,0))
    info(width * 0.5, height * 0.45, "Витрачено котожиттів " + str(9 - player.life), size=25, color=(250,250,0))
    info(width * 0.5, height * 0.5,  "Знищено монстрів " + str(player.score), size=25, color=(250,250,0))
    info(width * 0.5, height * 0.55, "Пропущено монстрів " + str(enemy_score), size=25, color=(250,250,0))
    info(width * 0.5, height * 0.85, "Для виходу натисни SPACE ", size=20, color=(250,250,250))
    if player.life > 0 and player.score == limit_score:
        result = "ТИ ВИГРАВ! МОЛОДЕЦЬ!"
    else:    
        result = "ТИ ПРОГРАВ, СПРОБУЙ ЩЕ РАЗ"
    info(width * 0.5, height * 0.7, result, size=30, color=(250,250,0))    
    display.update()
    time.delay(3000) 
    wait_key(K_SPACE) 
                                       
life_labels = []       
enemys = []
rockets = []
enemy_score = 0
init()
window = display.set_mode((width, height))
display.set_caption("Aliens")
clock = time.Clock()

mixer.music.load(folder + "_kosmos.ogg")
mixer.music.play()
sound_boom = mixer.Sound(folder + "_boom.ogg")
sound_score = mixer.Sound(folder + "_boom.ogg")
sound_loser = mixer.Sound(folder + "_loser.ogg")
sound_lanch = mixer.Sound(folder + "_rocket_lanch.ogg")

background = transform.scale(image.load(folder + "_fon.jpg"), (width, height))
window.blit(background, (0,0))

player = Game_Sprite(folder + "_cat.png", width / 2, height - 75, 7,   40, 58)
player.life = limit_life
create_enemy(10)
label_life()
rule_game()
game = True
while game:
    create_enemy(1)
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE: 
                player.launch_rocket()
            if e.key == K_x:    
                enemys.clear()
            if e.key == K_r:      
                rule_game()       
            if e.key == K_p:    
                pause_game()
            if e.key == K_q:    
                game = False      
             
    pressed_keys = key.get_pressed()     
    if pressed_keys[K_LEFT]:
        player.move_left()
    if pressed_keys[K_RIGHT]:
        player.move_right()
           
    if  player.score >= limit_score or player.life <= 0 or enemy_score >= 10: 
        game = False
        break
    
    move_rockets() 
    move_enemys() 
    window.blit(background, (0,0))
    player.draw_sprite()
    draw_enemys()
    draw_rockets()
    draw_info_string()
    draw_life()
    display.update()
    clock.tick(60) 
game_over() 
