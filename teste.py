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
PONTUACAO = 0
VIDAS = 5
GAMEOVER = False
PART_VELOCIDADE = 0.1
EXPLOSAO_TEMPO = 0.06

explosoes = []

# Classe que representa uma partícula
class Particula:
    def __init__(self, vx, vy, vz):
        self.vx = vx
        self.vy = vy
        self.vz = vz

# Classe que representa uma explosão de partículas      
class Explosao:
    px = py = pz = 0.0 #Posição
    contador = 0 #Tempo
    tdv = 1 #Tempo de vida
    particulas = [] #Particulas
        
    def __init__(self, px, py, pz, n_part): 
        self.px = px
        self.py = py
        self.pz = pz
        self.particulas = []
        for i in range(n_part):
            vx = np.random.randn() * PART_VELOCIDADE
            vy = np.random.randn() * PART_VELOCIDADE
            vz = np.random.randn() * PART_VELOCIDADE
            self.particulas.append(Particula(vx + 0.1, vy/2, vz/2)) 
         
    def desenha(self):
        for particula in self.particulas:
            part_px = self.px + particula.vx * (self.contador / 2)
            part_py = self.py + particula.vy * (self.contador / 2)
            part_pz = self.pz + particula.vz * (self.contador / 2)
            glPushMatrix()
            glTranslatef(part_px, part_py, part_pz)
            glRotatef( self.contador*10, 0.0, 1.0, 0.0)
            # glColor4f(0.9,  0.1, 0.1, self.tdv) #Vermelho
            glScalef(0.5, 0.5, 0.5)
            # glutSolidSphere(1.0, 10, 10)  # Use glutSolidSphere ou outro modelo de 
            visualization.draw(explosao) # desenho para a partícula
            glPopMatrix()
            
        self.tdv -= EXPLOSAO_TEMPO
        self.contador += 1


# classe para representar o tiro
class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.velocidade = 7.0
        self.size = 0.8

# Função para adicionar um novo tiro
def adicionar_tiro():
    global ANGLE, TIROS
    angulo = np.copy(ANGLE)
    x = T
    y = T2
    tiro = Tiro(x, y, ANGLE)
    TIROS.append(tiro)

def atualiza_tiros():
    global TIROS, PONTUACAO
    for tiro in TIROS:
        tiro.x += (0.15 * np.cos(np.radians(tiro.angulo))) * tiro.velocidade
        tiro.y += (0.15 * np.sin(np.radians(tiro.angulo))) * tiro.velocidade
        
        # Se o tiro colidir com um asteroide, remova o tiro e o asteroide da lista
        for asteroid in ASTEROIDES:
            if np.sqrt((tiro.x - asteroid.x)**2 + (tiro.y - asteroid.y)**2) <  (asteroid.size-(asteroid.size*0.1)):
                PONTUACAO += 100
                TIROS.remove(tiro)
                ASTEROIDES.remove(asteroid)
                #######################
                explosoes.append(Explosao(asteroid.x, asteroid.y, 1, 20))
                #######################
                if (asteroid.size > 2.0):
                    angulo = random.uniform(0, 360)
                    asteroid1 = Asteroid(asteroid.x, asteroid.y, asteroid.size/2.0, asteroid.speed, asteroid.surgimento, angulo, asteroid.nome)
                    angulo = random.uniform(0, 360)
                    asteroid2 = Asteroid(asteroid.x, asteroid.y, asteroid.size/2.0, asteroid.speed, asteroid.surgimento, angulo, asteroid.nome)
                    ASTEROIDES.append(asteroid1)
                    ASTEROIDES.append(asteroid2)
        
        # Se o tiro sair da tela, remova-o da lista
        if tiro.x < -30.0 or tiro.x > 30.0 or tiro.y < -30.0 or tiro.y > 30.0:
            TIROS.remove(tiro)

# classe para representar um asteroide
class Asteroid:
    def __init__(self, x, y, size, speed, surgimento, angulo, nome):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.surgimento = surgimento
        self.angulo = angulo
        self.rotacao = 0.0
        self.nome = nome

# Função para adicionar um novo asteroide em uma posição aleatória na borda
def adicionar_asteroide():
    # Escolha aleatoriamente uma das quatro bordas (cima, baixo, esquerda, direita)
    nomes = random.choice(["Asteroids/Asteroid_Small_1.obj", "Asteroids/Asteroid_Small_2.obj", 
                           "Asteroids/Asteroid_Small_3.obj", "Asteroids/Asteroid_Small_4.obj", 
                           "Asteroids/Asteroid_Small_5.obj", "Asteroids/Asteroid_Small_6.obj"])
    borda = random.choice(["cima", "direita", "esquerda", "baixo"])
    
    if borda == "cima":
        angulo = random.uniform(225, 315)
        surgimento = "cima"
        x = random.uniform(-30.0, 30.0)  # Posição x aleatória
        y = 30.0  # Na parte superior da tela
    elif borda == "baixo":
        angulo = random.uniform(45, 135)
        surgimento = "baixo"
        x = random.uniform(-30.0, 30.0)  # Posição x aleatória
        y = -30.0  # Na parte inferior da tela
    elif borda == "esquerda":
        # Escolher aleatoriamente entre os dois intervalos: (270, 360) ou (0, 90)
        intervalo = random.choice([(315, 360), (0, 45)])
        # Gerar um ângulo aleatório dentro do intervalo selecionado
        angulo = random.uniform(intervalo[0], intervalo[1])
        surgimento = "esquerda"
        x = -30.0  # Na parte esquerda da tela
        y = random.uniform(-30.0, 30.0)  # Posição y aleatória
    else:
        angulo = random.uniform(135, 225)
        surgimento = "direita"
        x = 30.0  # Na parte direita da tela
        y = random.uniform(-30.0, 30.0)  # Posição y aleatória
    
    size = random.uniform(1.0, 3.0)  # Tamanho aleatório
    speed = random.uniform(0.1, 0.3)  # Velocidade aleatória
    
    # Crie um novo asteroide e adicione-o à lista
    asteroid = Asteroid(x, y, size, speed, surgimento, angulo, nomes)
    ASTEROIDES.append(asteroid)

# Atualiza a posição de cada asteroide
def atualiza_asteroides():
    global ASTEROIDES, VIDAS, T, T2
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
        if np.sqrt((T - asteroid.x)**2 + (T2 - asteroid.y)**2) <  ((asteroid.size-(asteroid.size*0.1)) + 1.0):
            morte()
            ASTEROIDES.remove(asteroid)
            
        
        # Se o asteroide sair da tela, remova-o da lista
        if asteroid.x < -30.0 or asteroid.x > 30.0 or asteroid.y < -30.0 or asteroid.y > 30.0:
            ASTEROIDES.remove(asteroid)

def morte():
    global PONTUACAO, T, T2, VELOCIDADE, VIDAS, GAMEOVER
    
    VIDAS -= 1
    if PONTUACAO - 300 >= 0:
        PONTUACAO -= 300
    else:
        PONTUACAO = 0
    T = 0.0
    T2 = 0.0
    VELOCIDADE = 0.5
    
    if VIDAS == 0:
        GAMEOVER = True 

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
   
# Escreve um texto na tela    
def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))
        
def reseta_jogo():
    global VIDAS, ASTEROIDES, TIROS, PONTUACAO, T, T2, VELOCIDADE
    VIDAS = 5
    ASTEROIDES = []
    TIROS = []
    PONTUACAO = 0
    T = 0.0
    T2 = 0.0
    VELOCIDADE = 0.5

# Função de exibição
def display():
    global ASTEROIDES_ROTACAO, VIDAS, GAMEOVER, UP, LEFT, RIGHT
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa o buffer de cor e o buffer de profundidade
    glMatrixMode(GL_MODELVIEW) # Matriz de modelagem
    
    draw_text(-28.0, 18.0, "Pontuação: " + str(PONTUACAO)) # Escreve a pontuação na tela
    draw_text(-28.0, 16.0, "Velocidade: " + str(round(VELOCIDADE, 2))) # Escreve a velocidade na tela
    draw_text(-28.0, 14.0, "Vida: " + " <3" * VIDAS) # Escreve a vida na tela")
    atualiza_nave() 
    atualiza_asteroides()
    atualiza_tiros()
    
    if GAMEOVER:
        # Se o jogo acabou, exiba a mensagem "game over"
        UP = 0.0
        LEFT = 0.0
        RIGHT = 0.0
        draw_text(-4.0, 0.0, "GAME OVER")
        draw_text(-7.0, -2.0, "Pressione espaço para reiniciar") 
    
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
        #desenha o asteroide de acordo com nome
        if asteroid.nome == "Asteroids/Asteroid_Small_1.obj":
            visualization.draw(asteroid1)
        elif asteroid.nome == "Asteroids/Asteroid_Small_2.obj":
            visualization.draw(asteroid2)
        elif asteroid.nome == "Asteroids/Asteroid_Small_3.obj":
            visualization.draw(asteroid3)
        elif asteroid.nome == "Asteroids/Asteroid_Small_4.obj":
            visualization.draw(asteroid4) 
        elif asteroid.nome == "Asteroids/Asteroid_Small_5.obj":
            visualization.draw(asteroid5)
        elif asteroid.nome == "Asteroids/Asteroid_Small_6.obj":
            visualization.draw(asteroid6)
        glPopMatrix()
    
    # Desenhe os tiros
    for tiro in TIROS:
        glPushMatrix()
        glTranslatef(tiro.x, tiro.y, 0.0)
        glScalef(tiro.size, tiro.size, tiro.size)
        # glutSolidSphere(0.5, 20, 20)
        visualization.draw(missel) 
        glPopMatrix()

    # Desenhe as explosões 
    for i, expl in enumerate(explosoes):
        expl.desenha()
        if(expl.tdv < 0):
            del explosoes[i]

    # # Adicione a luz da esfera
    # glPushMatrix() 
    # glTranslatef(19.0, 9.0, -20)  # Posição da esfera (0, 0, 0)
    # glColor3f(1.0, 1.0, 1.0)    # Cor amarela
    # glutSolidSphere(5.0, 20, 20)  # Crie uma esfera sólida
    # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1.0, 1.0, 0.0, 1.0])
    # glPopMatrix()
    # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

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
    global UP, LEFT, RIGHT, VELOCIDADE, GAMEOVER

    if GAMEOVER:
        pass
    else:
        if key == GLUT_KEY_LEFT:
            # Rotacionar a nave para a esquerda no eixo Z
            LEFT = 1
        if key == GLUT_KEY_RIGHT:
            # Rotacionar a nave para a direita no eixo Z
            RIGHT = 1
        if key == GLUT_KEY_UP:
            # Mover a nave para frente levando em conta a rotação atual
            UP = 1

# Função para lidar com teclas liberadas
def KeysUp(key, x, y):
    global UP, LEFT, RIGHT

    if key == GLUT_KEY_LEFT:
        LEFT = 0
    if key == GLUT_KEY_RIGHT:
        RIGHT = 0
    if key == GLUT_KEY_UP:
        UP = 0

# Função de atualização da nave
def atualiza_nave():
    global ANGLE, UP, LEFT, RIGHT, VELOCIDADE

    if LEFT == 1:
        ANGLE += 10.0
        if VELOCIDADE > 1.0:
            VELOCIDADE -= 0.02
    if RIGHT == 1:
        ANGLE -= 10.0
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
    global GAMEOVER
    if GAMEOVER:
        reseta_jogo()
        if key == b' ':
            GAMEOVER = False    
    else:
        # Caso contrário, permita que o jogador dispare tiros
        if key == b' ':
            adicionar_tiro()

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1280, 720)
    glutInitWindowPosition(50, 50)
    wind = glutCreateWindow("Meu Asteroids")
    init()
    
    # Referência para a nave
    rocket = pywavefront.Wavefront("AirShip\AirShip.obj")
    
    # referencia para os 6 asteroides
    asteroid1 = pywavefront.Wavefront("Asteroids\Asteroid_Small_1.obj")
    asteroid2 = pywavefront.Wavefront("Asteroids\Asteroid_Small_2.obj")
    asteroid3 = pywavefront.Wavefront("Asteroids\Asteroid_Small_3.obj")
    asteroid4 = pywavefront.Wavefront("Asteroids\Asteroid_Small_4.obj")
    asteroid5 = pywavefront.Wavefront("Asteroids\Asteroid_Small_5.obj")
    asteroid6 = pywavefront.Wavefront("Asteroids\Asteroid_Small_6.obj")
    
    # referencia para o tiro
    missel = pywavefront.Wavefront("Tiro\missile.obj")
    
    # referencia para a explosão
    explosao = pywavefront.Wavefront("explosao.obj")
    
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutTimerFunc(30, animacao, 1)
    glutSpecialFunc(Keys)
    glutSpecialUpFunc(KeysUp)
    glutKeyboardUpFunc(KeysBoards)
    
    glutMainLoop()
