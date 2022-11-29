import pygame
from constantes import *
from auxiliar import*
from master_enemigo import Enemigo_master



'''
class Jefe_uno(Enemigo):
    def __init__(self, x=500, y=0, direction = DIRECTION_R, gravity=10, frame_rate_ms=150, move_rate_ms=50) -> None:
        super().__init__(x, y, direction, gravity, frame_rate_ms, move_rate_ms)
        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet("PIXEL ADVENTURE\Recursos\Enemies\AngryPig\Idle (36x30).png",9,1,True,scale=5)
        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet("PIXEL ADVENTURE\Recursos\Enemies\AngryPig\Idle (36x30).png",9,1,scale=5)

    def update(self, delta_ms, plataform_list,bala,player):
        self.stay()
        self.do_movement(delta_ms,plataform_list)
        self.do_animation(delta_ms)
        self.colision_bala(bala)
        self.colision_head(player)
        self.definir_rect()
'''

class Jefe_uno(Enemigo_master):
    def __init__(self, x=400,y=0,direction=DIRECTION_R,gravity=14, frame_rate_ms=100, move_rate_ms=50) -> None:
        super().__init__(gravity, frame_rate_ms, move_rate_ms)
    

        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet("PIXEL ADVENTURE\Recursos\Enemies\AngryPig\Idle (36x30).png",9,1,True,scale=5)
        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet("PIXEL ADVENTURE\Recursos\Enemies\AngryPig\Idle (36x30).png",9,1,scale=5)
        self.muerte = Auxiliar.getSurfaceFromSpriteSheet("PIXEL ADVENTURE\Recursos\Enemies\AngryPig\Hit 1 (36x30).png",5,1,scale=5)

        self.vidas = 20
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.gravity = gravity
        self.animation = self.stay_r
        self.direction = direction
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #rectangulo del personsaje
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y-5,self.rect.width/3,self.rect.height)
        #rectangulo de los pies
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H
        #rectangulo de la cabeza
        self.head_collition_rect = pygame.Rect(self.collition_rect)
        self.head_collition_rect.height = GROUND_COLLIDE_H
        self.head_collition_rect.y = y
        #collision para que comience a disparar
        self.disparo_collition_rect = pygame.Rect(x,y,300,GROUND_COLLIDE_H)
        self.disparo_collition_rect_l = pygame.Rect(x-300,y,300,GROUND_COLLIDE_H)
        self.disparo_collition_rect_r = pygame.Rect(x,y,300,GROUND_COLLIDE_H)

        self.is_fall = False
        self.eliminado = False
        self.soltar_vida = False
        self.disparar = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general

    def cambiar_direccion(self,delta_ms):
        self.tiempo_transcurrido += delta_ms
        if self.tiempo_transcurrido < 5000:
            self.direction = DIRECTION_L
        else:
            self.direction = DIRECTION_R
            if self.tiempo_transcurrido > 5000:
                self.tiempo_transcurrido = 0

    def stay(self):
        if(self.animation != self.muerte):
            if(self.direction == DIRECTION_R):
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l
            self.move_x = 0
            self.move_y = 0
            self.frame = 0

    def animacion_muerte(self,delta_ms):
        self.tiempo_transcurrido += delta_ms
        if self.tiempo_transcurrido > 500:
            self.tiempo_transcurrido = 0

            if self.eliminado:
                self.animation = self.muerte
                for i in range(4):
                    self.change_x(10)
                self.change_y(50)

    def update(self,delta_ms,plataform_list,bala,player):
        self.stay()
        self.do_movement(delta_ms,plataform_list)
        self.do_animation(delta_ms)
        self.colision_bala(bala,delta_ms,player)
        #self.colision_head(player)
        self.cambiar_direccion(delta_ms)
        self.animacion_muerte(delta_ms)
    
    
    def draw(self,screen):
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        if(DEBUG):
            pygame.draw.rect(screen,color=BLUE,rect=self.collition_rect)
            pygame.draw.rect(screen,color=RED,rect=self.ground_collition_rect)
            pygame.draw.rect(screen,color=BLACK,rect=self.head_collition_rect)

