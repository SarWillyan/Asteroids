from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np

# Variáveis globais
left = 0.0
right = 0.0
up = 0.0
down = 0.0
T = 0
T2 = 0
T3 = 0
angle = 0.0
velocidade = 0.8

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa o buffer de cor e o buffer de profundidade
    glMatrixMode(GL_MODELVIEW) # Matriz de modelagem
    
    atualiza_nave() 
    
    glPushMatrix() # Empilha a matriz atual
    glTranslatef(T, T2, 0) 
    glRotatef(angle, 0.0, 0.0, 1.0) 
    glScalef(0.3, 0.3, 0.3) 
    visualization.draw(rocket) 
    glPopMatrix() # Desempilha a matriz atual

    # Adicione a luz da esfera
    glPushMatrix() 
    glTranslatef(19.0, 9.0, 0)  # Posição da esfera (0, 0, 0)
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
    global up, down, left, right

    if key == GLUT_KEY_LEFT:
        # Rotacionar a nave para a esquerda no eixo Z
        left = 1
    elif key == GLUT_KEY_RIGHT:
        # Rotacionar a nave para a direita no eixo Z
        right = 1
    elif key == GLUT_KEY_UP:
        # Mover a nave para frente levando em conta a rotação atual
        up = 1
    elif key == GLUT_KEY_DOWN:
        # Mover a nave para trás levando em conta a rotação atual
        down = 1
        velocidade = 0.8

# Função para lidar com teclas liberadas
def KeysUp(key, x, y):
    global up, down, left, right, velocidade

    if key == GLUT_KEY_LEFT:
        left = 0
    elif key == GLUT_KEY_RIGHT:
        right = 0
    elif key == GLUT_KEY_UP:
        up = 0
    elif key == GLUT_KEY_DOWN:
        down = 0

# Função de atualização da nave
def atualiza_nave():
    global angle, up, down, left, right

    if left == 1:
        angle += 5.0
    if right == 1:
        angle -= 5.0
    if up == 1:
        avanca_nave()
    if down == 1:
        recua_nave()
    if up == 0 and down == 0:
        desacelera_nave()

# Função para mover a nave para frente
def avanca_nave():
    global T, T2, angle, velocidade
    if velocidade < 3.5:
        velocidade += 0.03
    T += (0.15 * np.cos(np.radians(angle))) * velocidade
    T2 += (0.15 * np.sin(np.radians(angle))) * velocidade

# Função para mover a nave para trás
def recua_nave():
    global T, T2, angle, velocidade
    if velocidade < 3.5:
        velocidade += 0.03
    T -= (0.15 * np.cos(np.radians(angle))) * velocidade
    T2 -= (0.15 * np.sin(np.radians(angle))) * velocidade

# Função para desacelerar a nave
def desacelera_nave():
    global T, T2, angle, velocidade
    if velocidade > 0.8:
        velocidade -= 0.1
        T += (0.15 * np.cos(np.radians(angle))) * velocidade
        T2 += (0.15 * np.sin(np.radians(angle))) * velocidade

# Função de animação
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao, 1)
    global T

# Função idle
def idle():
    global T
    T -= 1

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1280, 720)
    glutInitWindowPosition(50, 50)
    wind = glutCreateWindow("Jogo")
    init()
    rocket = pywavefront.Wavefront("AirShip\AirShip.obj")
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutTimerFunc(30, animacao, 1)
    glutSpecialFunc(Keys)
    glutSpecialUpFunc(KeysUp)
    glutMainLoop()
