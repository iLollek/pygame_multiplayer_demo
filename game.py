import os
import socket
import sys
import pygame
import threading
import time
import string
import random

host = 'localhost'
port = 8888
names = []

def generate_random_string(length):
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def send_circle_data(x, y, name):
    """Sends the Circle Data"""

    x = round(x)

    y = round(y)

    s = socket.socket()

    s.connect((host, port))

    s.send(f'REQ=SENDPOS#{x}#{y}#{name}'.encode())

    s.close()

def get_circle_data(name):
    """Receives the other circles Data"""

    s = socket.socket()

    s.connect((host, port))

    s.send(f'REQ=GETPOS#{name}'.encode())

    data = s.recv(1024).decode()

    s.close()

    return data.split("#")

def get_all_players():
    """Gets all Names of Players connected in the Lobby"""

    s = socket.socket()

    s.connect((host, port))

    s.send(f'REQ=GETALLNAMES'.encode())

    names = s.recv(4098).decode()

    names = names.split("#")

    s.close()

    return names

def draw_circle_to_screen(x, y, name):
    x = int(x)
    y = int(y)
    if name != player_name:
        pygame.draw.circle(screen, (255, 0, 0), pygame.Vector2(x, y), 40)
        # Render the player's name to a text surface
        text_surface = font.render(name, True, (255, 255, 255))  # White color

        # Blit the text surface above the player's position
        text_rect = text_surface.get_rect(center=(x, y - 60))
        screen.blit(text_surface, text_rect)
        print(f'Drawing {name} at X: {x} & Y: {y}')

def multiplayer_update():
    while True:
        global names

        print("Multiplayer name update")

        names = get_all_players()
        time.sleep(120)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 360))
clock = pygame.time.Clock()
running = True
dt = 0

FPS = 30

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_name = generate_random_string(4)
font = pygame.font.Font(None, 36)  # Font for rendering the player's name

t1 = threading.Thread(target=multiplayer_update)
t1.start()

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    

    pygame.draw.circle(screen, (255, 0, 0), player_pos, 40)
    send_circle_data(player_pos.x, player_pos.y, player_name)
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # Render the player's name to a text surface
    text_surface = font.render(player_name, True, (255, 255, 255))  # White color

    for playername in names:
        if len(playername) != 0:
            position = get_circle_data(playername)
            if position[1] != "NONE":
                draw_circle_to_screen(position[1], position[2], playername)

    # Blit the text surface above the player's position
    text_rect = text_surface.get_rect(center=(player_pos.x, player_pos.y - 60))
    screen.blit(text_surface, text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 30
    dt = clock.tick(FPS) / 1000  # Lock the frame rate to 60 FPS

    screen.fill((128, 0, 128))  # Purple color



pygame.quit()
