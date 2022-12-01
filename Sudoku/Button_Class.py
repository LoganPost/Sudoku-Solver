import pygame as pg
from Matrix_Class import V

debug=False
pg.init()

evscl=1

rad=10*evscl # Corner radius of buttons
class Button():
    def __init__(self,size,color,text="",text_color=(0,0,0),font=pg.font.SysFont('calibri', 20*evscl),thickness=2):
        if debug: # Preconditions: parameters must be the right type
            assert len(size)==2
            assert len(color)==3
            for i in color:
                assert 0<=i<256
            assert isinstance(text,str)
            assert len(text_color)==3
            for i in text_color:
                assert 0<=i<256
            assert isinstance(thickness,int)
        self.rad=rad
        self.size=size
        self.font=font                                      # Font of text
        self.thickness=thickness                            # Thickness of border
        self.color=V(color)                                    # Color of fill
        self.text_color=text_color                          # Color of text
        self.text=text                                      # Words to print
        self.rect=pg.Rect(0,0,*size)                        # Dimensions of button
        self.text_surface=font.render(text,True,text_color) # Rendering text onto surface
        self.text_rect=self.text_surface.get_rect()         # Used for centering text surface
        self.text_shift=V((0,0)) # Used to shift text off center
        self.pressed=False
        if debug: # Postconditions: The rects should be in same place
            assert self.rect.topleft==self.text_rect.topleft
        pass
    def changeColor(self,color):
        self.color=V(color)    # Changes color lol
    def changeText(self,text=None,color=None,font=None):    # Changes some properties about the text
        if debug: # Preconditions: Check for correct type. Not dealing with font
            if text!=None:
                assert isinstance(text,str)
            if color!=None:
                assert isinstance(color,tuple) and len(color)==3
        if text!=None:
            self.text=text          # Change the words
        if color!=None:
            self.text_color=color   # Change color of the text
        if font!=None:
            self.font=font          # Change the font
        self.text_surface=(self.font).render(self.text,True,self.text_color)    # Redraw text surface
        self.text_rect=self.text_surface.get_rect()                             # New Rect for centering
        self.text_rect.center=self.rect.center+self.text_shift                  # Center the text
        # No Postconditions necessary
    def pop_string(self):
        self.changeText(self.text[:-1])
    def blit(self,surf,clicking=False):   # Draws the button on the screen, bolder if selected
        if debug: # Preconditions: Correct input types, text is right
            assert isinstance(clicking,bool)
            assert self.text_rect.center==self.rect.center+self.text_shift

        if clicking or self.pressed: # Draw the button; make it different if the button is being pressed.
            pg.draw.rect(surf, self.color*.9, self.rect, border_radius=self.rad)  # Draw bg, darker if being pressed
            surf.blit(self.text_surface, self.text_rect)  # Write text
            if self.thickness!=0:
                pg.draw.rect(surf, V(self.color)/3, self.rect, self.thickness*2*evscl,border_radius=self.rad) # Thicker border
        else:
            pg.draw.rect(surf, self.color, self.rect, border_radius=self.rad)  # Draw background
            surf.blit(self.text_surface, self.text_rect)  # Write text
            if self.thickness!=0:
                pg.draw.rect(surf, V(self.color)/3, self.rect, self.thickness*evscl,border_radius=self.rad)
    def midleft(self,loc): # Move button by setting the midleft point
        self.rect.midleft = loc  # Move rect
        self.text_rect.center = self.rect.center + self.text_shift  # Recenter text (with shift)
    def topleft(self,loc):
        self.rect.topleft = loc  # Move rect
        self.text_rect.center = self.rect.center + self.text_shift  # Recenter text (with shift)
    def center(self,loc): # Move button by setting the center point
        if debug:
            assert isinstance(loc,tuple) and len(loc)==2
        self.rect.center=loc    # Move rect
        self.text_rect.center=loc+self.text_shift               # Recenter text (with shift)
    def centerx(self,pos): # Move the central x coord of the button
        if debug:
            assert isinstance(pos,int) or isinstance(pos,float)
        self.center((pos,self.rect.centery)) # Keep centery where it is, move to new x
    def shiftText(self,shift=(0,0)): #Shift the text off the the center of the button
        if debug:
            assert isinstance(shift,tuple) and len(shift)==2
        self.text_shift=shift
        self.text_rect.center = V(shift)+self.text_rect.center # Center the text off the button's center
    def collidepoint(self,point):   # Check for collision
        if debug:
            assert isinstance(point,tuple) and len(point)==2
        return self.rect.collidepoint(point)
    def size_to_fit(self):
        cntr=self.rect.center
        self.rect.width =max(self.text_rect.width+5,self.size[0])
        self.rect.height=max(self.text_rect.height+5, self.size[1])
        self.rect.center=cntr

class TextBox():
    def __init__(self,text="",color=(0,0,0),font=pg.font.SysFont('calibri',20*evscl)):
        self.font=font                                      # Font of text
        self.color=color                                    # Color of text
        self.text=text                                      # Words to print
        self.surf=font.render(text,True,color) # Rendering text onto surface
        self.rect=self.surf.get_rect()                      # Dimensions of textbox
        self.middle=self.rect.center
    def center(self,pos): #Sets the center of the textbox
        self.rect.center=pos
        self.middle = self.rect.center
    def topleft(self,pos):
        self.rect.topleft=pos
        self.middle = self.rect.center
    def changeText(self,text=None,color=None,font=None): #Changes some properties of the text
        if text!=None:
            self.text=text          # Change the words
        if color!=None:
            self.color=color   # Change color of the text
        if font!=None:
            self.font=font          # Change the font
        self.surf=self.font.render(self.text,True,self.color) # Re render
        self.rect=self.surf.get_rect()                          # re rect
        self.center(self.middle)                                # Re center
    def blit(self,screen): #Draws the textbox on the screen
        screen.blit(self.surf,self.rect)

class Bonus():
    def __init__(self,text,color,font=pg.font.SysFont("calibri",40*evscl),size=V((40,40))*evscl):
        self.text=text
        self.color=V(color)
        self.font=font
        self.size=size
        # self.surf=pg.Surface(self.size, pg.SRCALPHA, 32).convert_alpha()
        # self.rect=self.surf.get_rect()
        # pg.draw.ellipse(self.surf,self.color,pg.Rect((0,0),self.size))
        self.tsurf=font.render(self.text,True,(220,220,220))
    def stamp(self,screen,pos,size):
        size=V(size)
        surf=pg.transform.scale(self.tsurf,size/2)
        pg.draw.ellipse(screen, self.color, pg.Rect(pos+size*.1, size*.8))
        screen.blit(surf,pos+size/4)
        # screen.blit(surf,pos)