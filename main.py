import pygame
from sys import exit
from ui.button import Button
import os, random
pygame.init()

screen = pygame.display.set_mode((1380,1000))
pygame.display.set_caption("Pixel football manager")
icon = pygame.image.load("assets/images/icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


#----start button/exit button----#
start_img = pygame.image.load("assets/images/startbutton.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (160, 105))
exit_img = pygame.image.load("assets/images/exitbutton.png").convert_alpha()
exit_img = pygame.transform.scale(exit_img, (160, 100))
options_img = pygame.image.load("assets/images/optionsbutton.png").convert_alpha()
options_img = pygame.transform.scale(options_img, (165, 110))
#--------------------------------#
start_button = Button(100,200, start_img)
exit_button = Button(100,200, exit_img)
options_button = Button(100,200, options_img)
start_button.rect.topleft = (190, 889)
exit_button.rect.topleft  = (350, 895)
options_button.rect.topleft = (510,889)

#---------font-------------#
font = pygame.font.Font(None, 40)
name_font = pygame.font.Font(None, 26)
table_font = pygame.font.Font(None, 24)



#---------Vs prozor logo------------#

def load_img(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img
LOGO_SIZE = (110, 110)
my_logo = load_img("assets/logos/my_club.png", LOGO_SIZE)


opponent_logos = []
for fn in os.listdir("assets/logos/opponents"):
    if fn.lower().endswith((".png", ".jpg", ".jpeg")):
        opponent_logos.append(load_img(f"assets/logos/opponents/{fn}", LOGO_SIZE))

current_opponent_logo = random.choice(opponent_logos)

MY_LOGO_POS = (65, 235)        
OPP_LOGO_POS = (280, 240) 

#-----------------------------------------------#


#######################
GREEN = (40, 200, 40)
RED   = (220, 50, 50)
GRAY  = (170, 170, 170)
WHITE = (255, 255, 255)
#######################


#------------------utakmice-------------------#


def prettify_name(filename: str) -> str:
    name = os.path.splitext(filename)[0]   # ovako se mice png
    name = name.replace("_", " ").strip()
    name = " ".join(name.split())
    return name

def load_img(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img

LOGO_NEXT_SIZE = (110, 110)   
LOGO_TABLE_SIZE = (24, 24)   

def make_club(name, logo_path):
    return {
        "name": name,
        "logo_next": load_img(logo_path, LOGO_NEXT_SIZE),
        "logo_table": load_img(logo_path, LOGO_TABLE_SIZE),
        "P": 0, "W": 0, "D": 0, "L": 0,
        "GF": 0, "GA": 0, "Pts": 0
    }


# tvoj klub (promijeni path i ime kako želiš)
my_club = make_club("Player FC", "assets/logos/my_club.png")

# protivnici iz foldera
clubs = [my_club]

opp_dir = "assets/logos/opponents"
for fn in os.listdir(opp_dir):
    if fn.lower().endswith((".png", ".jpg", ".jpeg")):
        clubs.append(make_club(prettify_name(fn), os.path.join(opp_dir, fn)))

# ovo su svi protivnici (bez tebe)
opponents = [c for c in clubs if c is not my_club]

# trenutni protivnik za NEXT MATCH
current_opponent = random.choice(opponents)

#----------Logika da se mijenja protivnik nakon svakog matcha i match logika-----------#

recent_form = []
matchday = 1

def new_match():
    global current_opponent
    current_opponent = random.choice(opponents)

def play_match():
    global matchday

    my_goals = random.randint(0, 7)
    opp_goals = random.randint(0, 7)

    
    tag = apply_result(my_club, current_opponent, my_goals, opp_goals)

    # recent form
    recent_form.insert(0, {
        "result": tag,
        "score": f"{my_goals}-{opp_goals}"
    })

    recent_form[:] = recent_form[:5]

    matchday += 1
    new_match()


#------------------------------#

def apply_result(a, b, a_goals, b_goals):
    # played
    a["P"] += 1
    b["P"] += 1

    # goals
    a["GF"] += a_goals
    a["GA"] += b_goals
    b["GF"] += b_goals
    b["GA"] += a_goals

    # points & W/D/L
    if a_goals > b_goals:
        a["W"] += 1
        b["L"] += 1
        a["Pts"] += 3
        return "W"
    elif a_goals < b_goals:
        a["L"] += 1
        b["W"] += 1
        b["Pts"] += 3
        return "L"
    else:
        a["D"] += 1
        b["D"] += 1
        a["Pts"] += 1
        b["Pts"] += 1
        return "D"

def goal_diff(c):
    return c["GF"] - c["GA"]



#------------------------------------------------------------------------#

start_surface = pygame.image.load("assets/images/Planestart.png").convert_alpha()


PLAY_BTN_RECT = pygame.Rect(1030, 840, 150, 130)  # x, y, w, h (privremeno)


player_x_pos = 1200
game_state = "menu"

menu_surface = pygame.image.load("assets/images/background.png").convert_alpha()   # START SCREEN (stadion)
main_surface = pygame.image.load("assets/images/mainmenu.png").convert_alpha()   # MAIN SCREEN (dashboard)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "menu":
                if start_button.rect.collidepoint(event.pos):
                    game_state = "main"

                elif options_button.rect.collidepoint(event.pos):
                    print("Isnt added yet")
                elif exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

            elif game_state == "main":
                if PLAY_BTN_RECT.collidepoint(event.pos):
                    play_match()
                    print("PLAY MATCH!", recent_form[0])
                pass

    if game_state == "menu":
        screen.blit(menu_surface, (0, 0))

        player_x_pos -= 2
        if player_x_pos < -600:
            player_x_pos = 1380
        screen.blit(start_surface, (player_x_pos, 10))
        start_button.draw(screen)
        exit_button.draw(screen)
        options_button.draw(screen)

    elif game_state == "main":
        screen.blit(main_surface, (0, 0))


        # --- LEAGUE TABLE --- #
        table_x = 1000
        table_y = 180
        row_h = 28

        sorted_clubs = sorted(
            clubs,
            key=lambda c: (c["Pts"], goal_diff(c), c["GF"]),
            reverse=True
        )

        screen.blit(table_font.render("#  Club", True, WHITE), (table_x, table_y))
        screen.blit(table_font.render("GD", True, WHITE), (table_x + 300, table_y))
        screen.blit(table_font.render("Pts", True, WHITE), (table_x + 350, table_y))

        for i, c in enumerate(sorted_clubs):
            y = table_y + 25 + i * row_h

            if c is my_club:
                pygame.draw.rect(screen, (40, 60, 90), (table_x-10, y-2, 430, row_h), 0)

            screen.blit(table_font.render(str(i+1), True, WHITE), (table_x, y))
            screen.blit(c["logo_table"], (table_x + 25, y + 2))
            screen.blit(table_font.render(c["name"], True, WHITE), (table_x + 55, y))
            screen.blit(table_font.render(f"{goal_diff(c):+}", True, WHITE), (table_x + 300, y))
            screen.blit(table_font.render(str(c["Pts"]), True, WHITE), (table_x + 350, y))

            pygame.draw.rect(screen, RED, PLAY_BTN_RECT, 2)

            screen.blit(my_club["logo_next"], MY_LOGO_POS)
            screen.blit(current_opponent["logo_next"], OPP_LOGO_POS)

            screen.blit(name_font.render(my_club["name"], True, WHITE),
                        (MY_LOGO_POS[0] - 5, MY_LOGO_POS[1] + 110))
            screen.blit(name_font.render(current_opponent["name"], True, WHITE),
                        (OPP_LOGO_POS[0] - 5, OPP_LOGO_POS[1] + 110))

            start_x = 60
            start_y = 680
            gap = 70

            for i, match in enumerate(recent_form):
                x = start_x + i * gap
                y = start_y

                if match["result"] == "W":
                    color = GREEN
                elif match["result"] == "L":
                    color = RED
                else:
                    color = GRAY

                screen.blit(font.render(match["result"], True, color), (x, y))
                screen.blit(font.render(match["score"], True, WHITE), (x, y + 25))
     
    
    pygame.display.update()
    clock.tick(60)