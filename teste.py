from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np
import random

# Variáveis globais
LEFT = 0.0
RIGHT = 0.0
UP = 0.0
T = 0
T2 = 0
ANGLE = 0.0
ASTEROIDES_ROTACAO = 0.0
VELOCIDADE = 1.0
ASTEROIDES = []
TIROS = []

# classe para representar o tiro
class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.velocidade = 10.0
        self.size = 0.5

# Função para adicionar um novo tiro
def adicionar_tiro():
    global ANGLE, TIROS
    angulo = np.copy(ANGLE)
    x = T
    y = T2
    tiro = Tiro(x, y, ANGLE)
    TIROS.append(tiro)

def atualiza_tiros():
    global TIROS
    for tiro in TIROS:
        tiro.x += (0.15 * np.cos(np.radians(tiro.angulo))) * tiro.velocidade
        tiro.y += (0.15 * np.sin(np.radians(tiro.angulo))) * tiro.velocidade
        
        # Se o tiro colidir com um asteroide, remova o tiro e o asteroide da lista
        for asteroid in ASTEROIDES:
            if np.sqrt((tiro.x - asteroid.x)**2 + (tiro.y - asteroid.y)**2) <  asteroid.size + 0.5:
                TIROS.remove(tiro)
                ASTEROIDES.remove(asteroid)
        
        # Se o tiro sair da tela, remova-o da lista
        if tiro.x < -30.0 or tiro.x > 30.0 or tiro.y < -30.0 or tiro.y > 30.0:
            TIROS.remove(tiro)

# classe para representar um asteroide
class Asteroid:
    def __init__(self, x, y, size, speed, surgimento, angulo):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.surgimento = surgimento
        self.angulo = angulo
        self.rotacao = 0.0

# Função para adicionar um novo asteroide em uma posição aleatória na borda
def adicionar_asteroide():
    # Escolha aleatoriamente uma das quatro bordas (cima, baixo, esquerda, direita)
    borda = random.choice(["cima", "direita", "esquerda", "baixo"])
    
    if borda == "cima":
        angulo = random.uniform(180, 360)
        surgimento = "cima"
        x = random.uniform(-30.0, 30.0)  # Posição x aleatória
        y = 30.0  # Na parte superior da tela
    elif borda == "baixo":
        angulo = random.uniform(0, 180)
        surgimento = "baixo"
        x = random.uniform(-30.0, 30.0)  # Posição x aleatória
        y = -30.0  # Na parte inferior da tela
    elif borda == "esquerda":
        # Escolher aleatoriamente entre os dois intervalos: (270, 360) ou (0, 90)
        intervalo = random.choice([(270, 360), (0, 90)])
        # Gerar um ângulo aleatório dentro do intervalo selecionado
        angulo = random.uniform(intervalo[0], intervalo[1])
        surgimento = "esquerda"
        x = -30.0  # Na parte esquerda da tela
        y = random.uniform(-30.0, 30.0)  # Posição y aleatória
    else:
        angulo = random.uniform(90, 270)
        surgimento = "direita"
        x = 30.0  # Na parte direita da tela
        y = random.uniform(-30.0, 30.0)  # Posição y aleatória
    
    size = random.uniform(1.0, 3.0)  # Tamanho aleatório
    speed = random.uniform(0.1, 0.3)  # Velocidade aleatória
    
    # Crie um novo asteroide e adicione-o à lista
    asteroid = Asteroid(x, y, size, speed, surgimento, angulo)
    ASTEROIDES.append(asteroid)

# Atualiza a posição de cada asteroide
def atualiza_asteroides():
    global ASTEROIDES
    for asteroid in ASTEROIDES:
        # Se o asteroide estiver na parte superior da tela, mova-o para baixo
        if asteroid.surgimento == "cima":
            asteroid.x -= asteroid.speed * np.cos(np.radians(asteroid.angulo))
            asteroid.y -= asteroid.speed * np.sin(np.radians(asteroid.angulo))
        # Se o asteroide estiver na parte inferior da tela, mova-o para cima
        elif asteroid.surgimento == "baixo":
            asteroid.x += asteroid.speed * np.cos(np.radians(asteroid.angulo))
            asteroid.y += asteroid.speed * np.sin(np.radians(asteroid.angulo))
        # Se o asteroide estiver na parte esquerda da tela, mova-o para a direita
        elif asteroid.surgimento == "esquerda":
            asteroid.x += asteroid.speed * np.cos(np.radians(asteroid.angulo))
            asteroid.y += asteroid.speed * np.sin(np.radians(asteroid.angulo))
        # Se o asteroide estiver na parte direita da tela, mova-o para a esquerda
        if asteroid.surgimento == "direita":
            asteroid.x += asteroid.speed * np.cos(np.radians(asteroid.angulo))
            asteroid.y += asteroid.speed * np.sin(np.radians(asteroid.angulo))
        
        # Se o asteroide colidir com a nave, remova-o da lista
        if np.sqrt((T - asteroid.x)**2 + (T2 - asteroid.y)**2) <  asteroid.size + 1.0:
            ASTEROIDES.remove(asteroid)
          
        # Se o asteroide sair da tela, remova-o da lista
        if asteroid.x < -30.0 or asteroid.x > 30.0 or asteroid.y < -30.0 or asteroid.y > 30.0:
            ASTEROIDES.remove(asteroid)

# Função de inicialização
def init():
    glClearColor(0.2, 0.2, 0.2, 1.0) # Cor de fundo
    glShadeModel(GL_SMOOTH) # Tipo de sombreamento
    glClearDepth(1.0) # Profundidade do buffer de profundidade
    glEnable(GL_DEPTH_TEST) # Habilita o teste de profundidade
    glDepthFunc(GL_LEQUAL) # Tipo do teste de profundidade
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST) # Correção de perspectiva
    # Adicione a luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0]) # Cor da luz ambiente
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0]) # Cor da luz ambiente
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0]) # Cor da luz difusa
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1]) # Cor da luz especular
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 10.0, 10.0, 0.0]) # Posição da luz
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01) # Atenuação da luz
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01) # Atenuação da luz
    glEnable(GL_LIGHT0)  # Habilita a luz de número 0
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

# Função de exibição
def display():
    global ASTEROIDES_ROTACAO
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa o buffer de cor e o buffer de profundidade
    glMatrixMode(GL_MODELVIEW) # Matriz de modelagem
    
    atualiza_nave() 
    atualiza_asteroides()
    atualiza_tiros()
    
    glPushMatrix() # Empilha a matriz atual
    glTranslatef(T, T2, 0) 
    glRotatef(ANGLE, 0.0, 0.0, 1.0) 
    glScalef(0.3, 0.3, 0.3) 
    visualization.draw(rocket) 
    glPopMatrix() # Desempilha a matriz atual
    
    # Desenhe os asteroides
    for asteroid in ASTEROIDES:
        glPushMatrix()
        glTranslatef(asteroid.x, asteroid.y, 0.0)
        asteroid.rotacao += asteroid.speed * 5.0
        glRotatef(asteroid.rotacao, 1.0, 0.0, 0.0)
        glScalef(asteroid.size, asteroid.size, asteroid.size) 
        glColor3f(0.5, 0.2, 0.0)
        glutSolidSphere(1.0, 5, 5)  # Use glutSolidSphere ou outro modelo de asteroide
        glPopMatrix()
    
    # Desenhe os tiros
    for tiro in TIROS:
        glPushMatrix()
        glTranslatef(tiro.x, tiro.y, 0.0)
        glScalef(tiro.size, tiro.size, 1.0) 
        glColor3f(1.0, 0.0, 0.0)  # Cor dos tiros
        glutSolidSphere(0.5, 10, 10)
        glPopMatrix()

    # Adicione a luz da esfera
    glPushMatrix() 
    glTranslatef(19.0, 9.0, -20)  # Posição da esfera (0, 0, 0)
    glColor3f(1.0, 1.0, 0.0)    # Cor amarela
    glutSolidSphere(5.0, 20, 20)  # Crie uma esfera sólida
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1.0, 1.0, 0.0, 1.0])
    glPopMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    glutSwapBuffers()

# Função de redimensionamento
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(37.0, w / h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 60.0,   # posição da câmera
              0.0, 0.0, 0.0,    # onde a câmera vai apontar
              0.0, 1.0, 0.0)    # parte para cima

# Função para lidar com teclas pressionadas
def Keys(key, x, y):
    global UP, LEFT, RIGHT, VELOCIDADE

    if key == GLUT_KEY_LEFT:
        # Rotacionar a nave para a esquerda no eixo Z
        LEFT = 1
    elif key == GLUT_KEY_RIGHT:
        # Rotacionar a nave para a direita no eixo Z
        RIGHT = 1
    elif key == GLUT_KEY_UP:
        # Mover a nave para frente levando em conta a rotação atual
        UP = 1

# Função para lidar com teclas liberadas
def KeysUp(key, x, y):
    global UP, LEFT, RIGHT

    if key == GLUT_KEY_LEFT:
        LEFT = 0
    elif key == GLUT_KEY_RIGHT:
        RIGHT = 0
    elif key == GLUT_KEY_UP:
        UP = 0

# Função de atualização da nave
def atualiza_nave():
    global ANGLE, UP, LEFT, RIGHT, VELOCIDADE

    if LEFT == 1:
        ANGLE += 5.0
        if VELOCIDADE > 1.0:
            VELOCIDADE -= 0.02
    if RIGHT == 1:
        ANGLE -= 5.0
        if VELOCIDADE > 1.0:
            VELOCIDADE -= 0.02
    if UP == 1:
        avanca_nave()
    if UP == 0:
        desacelera_nave()

# Função para mover a nave para frente
def avanca_nave():
    global T, T2, ANGLE, VELOCIDADE
    if VELOCIDADE < 4.0:
        VELOCIDADE += 0.06
    T += (0.15 * np.cos(np.radians(ANGLE))) * VELOCIDADE
    T2 += (0.15 * np.sin(np.radians(ANGLE))) * VELOCIDADE

# Função para desacelerar a nave
def desacelera_nave():
    global T, T2, ANGLE, VELOCIDADE
    if VELOCIDADE > 1.0:
        VELOCIDADE -= 0.06
        T += (0.15 * np.cos(np.radians(ANGLE))) * VELOCIDADE
        T2 += (0.15 * np.sin(np.radians(ANGLE))) * VELOCIDADE

# Função de animação
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao, 1)
    
    # Gera asteroides aleatórios em intervalos regulares
    if random.random() < 0.04: # 3% de chance
        adicionar_asteroide()

# Função idle
def idle():
    global T
    T -= 1
    
# Função para lidar com teclas pressionadas
def KeysBoards(key, x, y):
    if key == b' ':
        adicionar_tiro()

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1280, 720)
    glutInitWindowPosition(50, 50)
    wind = glutCreateWindow("Meu Asteroids")
    init()
    rocket = pywavefront.Wavefront("AirShip\AirShip.obj")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutTimerFunc(30, animacao, 1)
    glutSpecialFunc(Keys)
    glutSpecialUpFunc(KeysUp)
    glutKeyboardUpFunc(KeysBoards)
    
    glutMainLoop()
