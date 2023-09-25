from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization

T = 0
T2 = 0
T3 = 0

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    
    glPushMatrix()
    glTranslatef(T, T2, 0)
    glRotatef(180, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glScalef(0.3, 0.3, 0.3)
    visualization.draw(rocket)
    glPopMatrix()
    
    # Adicione a luz da esfera
    glPushMatrix()
    glTranslatef(19.0, 9.0, -20.0)  # Posição da esfera (0, 0, 0)
    glColor3f(1.0, 1.0, 0.0)    # Cor amarela
    glutSolidSphere(5.0, 20, 20)  # Crie uma esfera sólida
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1.0, 1.0, 0.0, 1.0])
    glPopMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    glutSwapBuffers()
    
def Keys(key, x, y):
    global T
    global T2
    global T3
    
    if(key == GLUT_KEY_LEFT ):
        if (T > -9): 
            T -= 0.15
    elif(key == GLUT_KEY_RIGHT ): 
        if (T < 9):
            T += 0.15
    elif(key == GLUT_KEY_UP ): 
        if (T2 < 7):
            T2 += 0.15
    elif(key == GLUT_KEY_DOWN ): 
        if (T2 > -7):
            T2 -= 0.15
    elif(key == GLUT_KEY_PAGE_UP ): 
        T3 -= 1 
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        T3 += 1       
       
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)
    global T
    
def idle():
    global T
    T-=1
    
    
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 40.0,   # posição da câmera
                0.0, 0.0, 0.0,  # onde a câmera vai apontar
                0.0, 1.0, 0.0)  # parte para cima

def init():
    glClearColor (0.0, 0.0, 0., 1.0)
    glShadeModel( GL_SMOOTH )
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0] )
    glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.2, 0.2, 0.2, 1.0] )
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0] )
    glLightfv( GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1] )
    glLightfv( GL_LIGHT0, GL_POSITION, [10.0, 10.0, 10.0, 0.0])
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01)
    glEnable( GL_LIGHT0 )
    glEnable( GL_COLOR_MATERIAL )
    glShadeModel( GL_SMOOTH )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1280, 720)
glutInitWindowPosition(50, 50)
wind = glutCreateWindow("Jogo")
init()
rocket = pywavefront.Wavefront("AirShip\AirShip.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutMainLoop()
