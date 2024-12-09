import pygame
import os
import time
import numpy as np

pygame.init()
    
class button(object):
    def __init__(self, pos, size, colour=(0,0,0), image=None, text=None):
        self.x, self.y = pos
        self.colour = colour
        self.size = size
        self.display_size = size
        self.surf = pygame.surface.Surface(self.size)
        self.surf.fill(colour)
        
        self.image = image
        if self.image != None:
            self.surf = pygame.transform.smoothscale(self.image, self.size)
        
        self.text = text
            
        self.rect = self.surf.get_rect()
        
        self.active = True
        self.page = None
        self.display = None
        self.ID = None
    
    def is_hovering(self):
        if self.active:
            # Unpack the mouse x and mouse y
            mx, my = pygame.mouse.get_pos()
            # Get the borders
            mx += self.rect.width/2
            my += self.rect.height/2
            # Check if the x position is in the bounds
            x_border = mx > self.x and mx < self.x + self.rect.width
            # Check if the y position is in the bounds
            y_border = my > self.y and my < self.y + self.rect.height
            # Change state regarding whether the mouse is hovering
            hover = x_border and y_border
            # Return whether the mouse is hovering over the button
            index = self.page.IDs[self.ID]
            self.page.hover[index] = hover
            return hover
        else:
            return False
    
    def set_colour(self, colour):
        self.colour = colour
    
    def set_size(self, size):
        self.size = size
        self.surf = pygame.transform.smoothscale(self.surf, self.size)
        self.rect = self.surf.get_rect()
    
    def show(self):
        if self.active:
            # Center the surface
            self.rect.center = (self.x, self.y)
            
            if self.image == None:
                self.surf.fill(self.colour)
            self.display.blit(self.surf, self.rect)
            
            if self.text != None:
                font = self.page.interface.font_types['button']
                r,g,b = self.colour
                r = 255-r
                g = 255-g
                b = 255-b
                # Anti-aliasing and negative colour
                textSurf = font.render(self.text, True, (r,g,b))
                textrect = textSurf.get_rect()
                textrect.center = (self.x, self.y)
                self.display.blit(textSurf, textrect)
    
    def click(self):
        self.colour = np.random.randint(0,255,3)

class Page(object):
    def __init__(self):
        self.active = False
        self.interface = None
        self.display = None
        
        # Dictionaries and lists for the buttons
        self.buttons = []
        self.hover = {}
        self.IDs = {}
    
    def check_hover(self):
        # Check which buttons have the mouse hovering
        buttons = [button for button, state in self.hover.items() if state is True]
        # Return those buttons
        return buttons
    
    def add(self, button, index=-1):
        # Make a valid new ID
        newID = 0
        while newID in list(self.IDs.keys()):
            # The ID is randomly generated
            newID = np.random.randint(1, len(self.buttons)*2)
        
        # Add in the relevant information for the new button
        button.ID = newID
        button.display = self.display
        button.page = self
        
        # Add the new button
        self.IDs[newID] = len(self.buttons)
        if index == -1:
            self.buttons.append(button)
        else:
            self.buttons[index] = button
        self.hover[newID] = False
    
    def display_text(self, text, colour, position, font_type='header', antialiasing=True):
        font = self.interface.font_types[font_type]
        text_surface = font.render(text, antialiasing, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.display.blit(text_surface, text_rect)
    
    def tick(self):
        running = True
        self.display.fill((50,0,50))
        button_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                button_up = True
                
        # Iterate through every button
        for button in self.buttons:
            # Update and check if the button is hovering
            hovering = button.is_hovering()
            if hovering:
                if button_up:
                    button.click()
                
            button.show()
                
        # Update the display
        pygame.display.flip()
        
        # Is the program still running?
        return running
                
class interface():
    def __init__(self, size):
        self.pages = []
        self.stack = []
        self.fontname = None
        self.pageinit = False
        self.prevPage = None
        
        # Initialise a window
        self.sw, self.sh = size
        self.display = pygame.display.set_mode((self.sw,self.sh))
        
        # Font types
        self.font_types = {
            'header': pygame.font.Font(self.fontname, 50),
            'button': pygame.font.Font(self.fontname, 30),
            'display': pygame.font.Font(self.fontname, 40),
            }
        
        self.background_colour = (100, 50, 100)
    
    def set_font(self, font, size):
        self.fontname = font
        self.font = pygame.font.Font(self.fontname, size)
    
    def add(self, page):
        # Add the page to the current possible pages in the interface
        self.pages.append(page)
        page.display = self.display
        page.interface = self
        
        # Set the display of all the buttons as well
        for button in page.buttons:
            button.display = self.display
        
        if len(self.stack) == 0:
            self.push(page)
    
    def push(self, page):
        # Only push the page into the stack if the page is already in the interface object
        if page in self.pages:
            # If the page is already in the stack remove the last loop
            if page in self.stack:
                index = self.stack.index(page)
                self.stack = self.stack[0:index]
            self.stack.append(page)
    
    def pop(self):
        # Remove the last page
        out = self.stack.pop(-1)
        return out
    
    def loop(self):
        # Flag variable
        running = True
        while running:
            # Set the active page
            active_page = self.stack[-1]
            # Check with previous page
            self.pageinit = self.prevPage != active_page
            # Check if still running
            running = active_page.tick()
            # Update the previous page
            self.prevPage = active_page
        # Close the program
        pygame.quit()

class navigation(button):
    def __init__(self, pos, size, newPage, colour=(0,0,0), image=None, text=None):
        super().__init__(pos, size, colour, image, text)
        self.newPage = newPage
    
    def click(self):
        self.page.interface.push(self.newPage)

class Back(button):
    def __init__(self, pos, size, colour=(0,0,0), image=None, text=None):
        super().__init__(pos, size, colour, image, text)
    
    def click(self):
        self.page.interface.pop()

class dropdown(button):
    def __init__(self, pos, size, options, colour=(0,0,0), image=None, text=None):
        super().__init__(pos, size,  colour, image, text)
        # The list of options
        self.options = options
        # The list of buttons
        self.buttons = []
        # Has the dropdown box been clicked?
        self.clicked = False
        # The option that is being hovered over
        self.hover_option = None
        # The option that is selected
        self.selected_option = None
        # The original name of the dropdown
        self.name = text
        
        
        # The y position of original button
        ypos = self.y
        # The change in y position of all other buttons
        height = self.size[1]
        # Decrease the size slightly in the horizontal direction
        newsize = (self.size[0]*0.8, self.size[1]*0.9)
        # Darken the colour slightly
        newcolour = np.array(self.colour)*0.8
        for i, option in enumerate(self.options):
            # Move the next button down by the height
            ypos += height
            # The new button is just another button with the option as the text
            new = button((self.x, ypos), newsize, newcolour, image, option)
            # Deactivate the button
            new.active = False
            # Store the new button in the list of buttons
            self.buttons.append(new)
    
    def show(self):
        if self.active:
            super().show()
                
            for button in self.buttons:
                button.ID = self.ID
                button.page = self.page
                button.display = self.display
                button.show()
    
    def click(self):
        # Flip the active status of all the buttons
        self.clicked = not  self.clicked
        for button in self.buttons:
            button.active = self.clicked
        
        # If one of the option buttons has been selected
        if self.hover_option != None:
            # The hover option is committed
            self.selected_option = self.hover_option 
            self.hover_option = None
            
            # The text changes to reflect this
            self.text = self.name + ': ' + self.selected_option
        
        return self.selected_option
    
    def is_hovering(self):
        if self.active:
            # Is the original button hovering?
            hover = super().is_hovering()
            
            # Loop through the buttons to see which one is hovering
            hover_list = []
            if self.clicked:
                for button in self.buttons:
                    is_hovering = button.is_hovering()
                    hover_list.append(is_hovering)
            
            # If one of the buttons are in the hover state
            if True in hover_list:
                # Select the correct option
                hover_index = hover_list.index(True)
                self.hover_option = self.options[hover_index]
            else:
                self.hover_option = None
            
            # Is either the original button or one of the option buttons in the hover state
            return hover or (self.hover_option != None)
                
        else:
            return False

class slider(button):
    def __init__(self, pos, size, minimum, maximum, colour=(0,0,0), image=None, text=None):
        super().__init__(pos, size, colour, image, text)
        self.minimum = minimum
        self.maximum = maximum
        self.originalx = self.x
        
        self.drag = False
    
    def click(self):
        self.drag = not self.drag
        
    
    def follow(self, mousePos):
        newx = mousePos[0]
        newx = min(newx, self.maximum+self.originalx)
        newx = max(newx, self.minimum+self.originalx)
        self.x =  newx
        
        myRange = self.maximum - self.minimum
        value = self.maximum-(self.x - self.originalx)
        value /= myRange
        
        return value
        
    def show(self):
        if self.active:
            bar = pygame.surface.Surface((self.maximum - self.minimum, self.size[1]*0.6))
            bar.fill((0,0,0))
            barrect = bar.get_rect()
            barrect.center = (self.originalx + (self.maximum+self.minimum)/2, self.y)
            self.display.blit(bar, barrect)
            
            progress = pygame.surface.Surface(((self.x - self.originalx - self.minimum), self.size[1]*0.4))
            progress.fill((200,150,50))
            progrect = progress.get_rect()
            self.display.blit(progress, (self.originalx + self.minimum, self.y-self.size[1]/2*0.4))
            
            radius = (self.size[0] + self.size[1])/4
            pygame.draw.circle(self.display, self.colour, (self.x, self.y), radius)
            
            if self.text != None:
                font = self.page.interface.font_types['button']
                r,g,b = self.colour
                r = 255-r
                g = 255-g
                b = 255-b
                # Anti-aliasing and negative colour
                textSurf = font.render(self.text, True, (r,g,b))
                textrect = textSurf.get_rect()
                textrect.center = (self.x, self.y)
                self.display.blit(textSurf, textrect)
