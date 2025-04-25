import pygame
import sys
import random

# Colores
negro = (0, 0, 0)
gris = (124, 130, 133)
verde = (0, 255, 0)
azul_claro = (100, 149, 237)
amarillo = (255, 250, 0)
rosa = (255, 192, 203)
naranja = (255, 165, 0)
rojo = (255, 0, 0)
azul = (0, 0, 255)
blanco = (255, 255, 255)

colores_unicos = [
    rojo, azul, naranja, rosa, verde, amarillo, blanco, gris,
    (128, 0, 128), (0, 255, 255), (255, 105, 180), (0, 100, 0),
    (210, 105, 30), (75, 0, 130), (255, 20, 147), (0, 191, 255),
    (255, 140, 0), (127, 255, 212), (220, 20, 60)
]

pygame.init()
ventana = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Crossy Road")
clock = pygame.time.Clock()

fuente = pygame.font.SysFont("arial", 36)
vidas = 3

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 550
        self.vel = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.vel
        if teclas[pygame.K_UP]:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.vel
        self.rect.clamp_ip(pygame.Rect(0, 0, 900, 700))

    def draw(self, surface):
        x = self.rect.x
        y = self.rect.y
        pygame.draw.rect(surface, azul, (x, y, 50, 50))
        pygame.draw.rect(surface, azul, (x+50, y+8, 15, 35))
        pygame.draw.rect(surface, azul, (x-15, y+8, 15, 35))
        pygame.draw.rect(surface, azul, (x+7, y-10, 35, 15))
        pygame.draw.rect(surface, negro, (x+28, y+5, 13, 13))
        pygame.draw.rect(surface, negro, (x+10, y+5, 13, 13))
        pygame.draw.rect(surface, naranja, (x+20, y+15, 11, 11))
        pygame.draw.rect(surface, rosa, (x+35, y+18, 11, 11))
        pygame.draw.rect(surface, rosa, (x+5, y+18, 11, 11))
        pygame.draw.rect(surface, naranja, (x+35, y+50, 10, 20))
        pygame.draw.rect(surface, naranja, (x+10, y+50, 10, 20))

class Carro(pygame.sprite.Sprite):
    def __init__(self, x, y, color, velocidad):
        super().__init__()
        self.image = pygame.Surface((60, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = velocidad

    def update(self, carros_mismo_carril):
        bloqueado = False
        for otro in carros_mismo_carril:
            if otro == self:
                continue
            distancia = otro.rect.x - self.rect.x if self.velocidad > 0 else self.rect.x - otro.rect.x
            if 0 < distancia < 65 and otro.rect.y == self.rect.y:
                bloqueado = True
                break
        if not bloqueado:
            self.rect.x += self.velocidad

        if self.velocidad > 0 and self.rect.left > 900:
            self.rect.right = 0
        elif self.velocidad < 0 and self.rect.right < 0:
            self.rect.left = 900

# Generar lluvia
lluvia = []
for _ in range(100):
    x = random.randint(0, 900)
    y = random.randint(0, 700)
    velocidad = random.randint(4, 8)
    longitud = random.randint(7, 12)
    lluvia.append([x, y, velocidad, longitud])

def agregar_carros_sin_superposicion(cantidad, y, direccion, velocidades):
    global color_index
    carros = []
    usados = []
    for _ in range(cantidad):
        while True:
            x = random.randint(-2000, 0) if direccion == "derecha" else random.randint(900, 2500)
            velocidad = random.choice(velocidades)
            if direccion == "izquierda":
                velocidad = -velocidad
            espacio_valido = all(abs(x - usado[0]) > 120 for usado in usados)
            if espacio_valido:
                color = colores_unicos[color_index % len(colores_unicos)]
                color_index += 1
                carro = Carro(x, y, color, velocidad)
                carros.append(carro)
                usados.append((x, y))
                break
    return carros

jugador = Jugador()
grupo_jugador = pygame.sprite.Group(jugador)
random.shuffle(colores_unicos)
color_index = 0

# Carriles separados
carril_1 = pygame.sprite.Group(agregar_carros_sin_superposicion(6, 130, "derecha", [2, 3, 4]))
carril_2 = pygame.sprite.Group(agregar_carros_sin_superposicion(8, 320, "derecha", [3, 5, 6]))
carril_3 = pygame.sprite.Group(agregar_carros_sin_superposicion(8, 370, "izquierda", [2, 4, 5, 6]))

todos_los_carros = [carril_1, carril_2, carril_3]

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    jugador.update()
    for grupo in todos_los_carros:
        for carro in grupo:
            carro.update(grupo)

    # Colisiones
    for grupo in todos_los_carros:
        if pygame.sprite.spritecollideany(jugador, grupo):
            vidas -= 1
            jugador.rect.x, jugador.rect.y = 400, 550
            pygame.time.delay(500)
            if vidas == 0:
                ventana.fill(negro)
                texto_gameover = fuente.render("GAME OVER", True, rojo)
                ventana.blit(texto_gameover, (350, 300))
                pygame.display.update()
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

    ventana.fill(azul_claro)

    # Fondo
    pygame.draw.rect(ventana, azul_claro, (0, 1, 900, 200))
    pygame.draw.rect(ventana, azul_claro, (0, 500, 900, 200))
    pygame.draw.rect(ventana, negro, (0, 290, 900, 160))
    pygame.draw.rect(ventana, gris, (0, 450, 900, 50))
    pygame.draw.rect(ventana, gris, (0, 240, 900, 50))
    pygame.draw.rect(ventana, gris, (0, 50, 900, 50))
    pygame.draw.rect(ventana, negro, (0, 100, 900, 150))
    for x in [20, 240, 450, 650]:
        pygame.draw.rect(ventana, blanco, (x, 160, 170, 20))
        pygame.draw.rect(ventana, blanco, (x, 355, 170, 20))

    # Lluvia
    for gota in lluvia:
        pygame.draw.line(ventana, blanco, (gota[0], gota[1]), (gota[0], gota[1] + gota[3]), 1)
        gota[1] += gota[2]
        if gota[1] > 700:
            gota[0] = random.randint(0, 900)
            gota[1] = random.randint(-20, 0)

    for grupo in todos_los_carros:
        grupo.draw(ventana)

    jugador.draw(ventana)

    texto_vidas = fuente.render(f"Vidas: {vidas}", True, blanco)
    ventana.blit(texto_vidas, (20, 20))

    pygame.display.update()
    clock.tick(60)













