from common import *
import modelpage

class Home(Page):
    def __init__(self):
        super().__init__()
    
    def tick(self):
        running = True
        self.display.fill(self.interface.background_colour)
        
        
        text = 'Would you like to capture or load an image?'
        self.display_text(text, (255,255,255),(self.interface.sw/2, self.interface.sh/3))
        
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

class Capture_Image(Page):
    def __init__(self):
        super().__init__()
        global camselect
        # Get the list of all the cameras
        camlist = pygame.camera.list_cameras()
        # Make the dropdown
        camselect = dropdown((4*UI.sw/5,UI.sh/10), (350,50), camlist, colour=(100,100,100), text = 'Select camera')
        self.add(camselect)
        self.cameraname = None
        self.camera_active = False
        self.img = None
    
    def tick(self):
        running = True
        self.display.fill(self.interface.background_colour)
        
        # Set the camera to active if there is a camera
        if self.cameraname != None and self.interface.pageinit:
            # Make a camera object
            self.camera = pygame.camera.Camera(self.cameraname)
            # Start the camera
            self.camera.start()
            # Tell the rest of the program that the camera is active
            self.camera_active = True
            # Record the start time of the camera
            self.starttime = time.time()
            
        
        text = 'No Camera Selected'
        self.display_text(text, (255,255,255),(self.interface.sw/2, self.interface.sh/3))
        
        button_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if self.camera_active:
                    # Stop the camera
                    self.camera.stop()
                    # Tell the rest of the program that the camera is inactive
                    self.camera_active = False
            if event.type == pygame.MOUSEBUTTONUP:
                button_up = True
        
        # If there is an active camera...
        if self.camera_active:
            # Calculate how long the camera has been active for
            endtime = time.time()
            # If the camera has been active for more than one second...
            if endtime - self.starttime - 0.5 > 0.1:
                # Capture an image
                self.img = self.capture(self.camera)
                # Flip horizontally
                self.img = pygame.transform.flip(self.img, True, False)
                imgrect = self.img.get_rect()
                imgrect.center = (self.interface.sw/2, self.interface.sh/2)
                # Display the image
                self.display.blit(self.img, imgrect)
                # Set the take camera button to active
                self.buttons[2].active = True
                
        # Iterate through every button
        for button in self.buttons:
            # Update and check if the button is hovering
            hovering = button.is_hovering()
            if hovering and button_up:
                if button == camselect:
                    # Select a camera
                    self.cameraname = button.click()
                    # If a camera is selected...
                    if self.cameraname != None:
                        # Make a camera object
                        self.camera = pygame.camera.Camera(self.cameraname)
                        # Start the camera
                        self.camera.start()
                        # Tell the rest of the program that the camera is active
                        self.camera_active = True
                        # Record the start time of the camera
                        self.starttime = time.time()
                else:
                    button.click()
                    # If the button is a navigation button...
                    if type(button) in [navigation, Back]:
                        if self.camera_active:
                            # Stop the camera
                            self.camera.stop()
                            # Tell the rest of the program that the camera is inactive
                            self.camera_active = False
            button.show()
                
        # Update the display
        pygame.display.flip()
        
        # Is the program still running?
        return running
    
    def capture(self, camera): # Capture image function

        for i in range(10): # Loop is required
            image = camera.get_image() # Capture the image
        
        return image

class Display_Image_c(Page):
    def __init__(self):
        super().__init__()
    
    def tick(self):
        running = True
        self.display.fill(self.interface.background_colour)
        
        img = self.interface.pages[1].img
        imgrect = img.get_rect()
        imgrect.center = (self.interface.sw/2, self.interface.sh/2)
        # Display the image
        self.display.blit(img, imgrect)
        
        text = 'Do you like the image?'
        self.display_text(text, (255,255,255),(self.interface.sw/2, self.interface.sh/10))
        
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

class Select_Image(Page):
    def __init__(self):
        super().__init__()
        global imgselect
        
        # Make a path to the folder of images
        self.imagespath = os.path.join(os.getcwd(), 'Images')
        # Make a list of all the images
        imagelist = os.listdir(self.imagespath)
        # Make the dropdown
        imgselect = dropdown((UI.sw/2,UI.sh/4), (400,50), imagelist, colour=(100,100,100), text = 'Select image')
        self.add(imgselect)
        
        self.imagename = None
    
    def tick(self):
        running = True
        
        if self.interface.pageinit:
            imagelist = os.listdir(self.imagespath)
            # Make the dropdown
            imgselect = dropdown((UI.sw/2,UI.sh/4), (400,50), imagelist, colour=(100,100,100), text = 'Select image')
            self.add(imgselect, index=0)
        
        self.display.fill(self.interface.background_colour)
        
        if self.imagename == None:
            text = 'Select an image'
        else:
            text = 'You have selected: ' + self.imagename
        self.display_text(text, (255,255,255),(self.interface.sw/2, self.interface.sh/5))
        
        button_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                button_up = True
        
        self.buttons[2].active = self.imagename != None
        
        # Iterate through every button
        for button in self.buttons:
            # Update and check if the button is hovering
            hovering = button.is_hovering()
            if hovering:
                if button_up:
                    if button.ID == self.buttons[0].ID:
                        self.imagename = button.click()
                        if self.imagename != None:
                            imagepath = os.path.join(self.imagespath, self.imagename)
                            self.img = pygame.image.load(imagepath)
                            #imgselect.active = True
                    else:
                        button.click()
                
            button.show()
        
        
        # Update the display
        pygame.display.flip()
        
        # Is the program still running?
        return running

class Display_Image_l(Page):
    def __init__(self):
        super().__init__()
    
    def tick(self):
        running = True
        self.display.fill(self.interface.background_colour)
        
        img = self.interface.pages[2].img
        img = pygame.transform.smoothscale(img, (400,400))
        imgrect = img.get_rect()
        imgrect.center = (self.interface.sw/2, self.interface.sh/2)
        # Display the image
        self.display.blit(img, imgrect)

        self.display_text('Do you like the image?', (255,255,255),(self.interface.sw/2, self.interface.sh/10))
        
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

class Model(Page):
    def __init__(self):
        super().__init__()
        self.gradcam = 0
        self.gradcamvalue = 1
    
    def tick(self):
        running = True
        self.display.fill(self.interface.background_colour)
        
        img = self.interface.pages[2].img
        img = pygame.transform.smoothscale(img, (500,500))
        
        array = pygame.surfarray.array3d(img)
        probabilities, labels, c = modelpage.run(array, self.gradcam)
        
        # Get the indexes of the sorted array
        indices = np.argsort(probabilities)
        # Order in descending order
        indices = indices[::-1]
        sorted_labels = labels[indices]
        sorted_prob = probabilities[indices]
        
        # Cumulative sum of probabilities
        cumsum = np.cumsum(sorted_prob)
        # Determine the threshold to be 90%
        threshold = 0.9
        # Determine index of threshold
        n = np.argmax(cumsum > threshold) + 1
        
        # Cut off the lowest 10%
        sorted_labels = sorted_labels[0:n]
        sorted_prob = sorted_prob[:n]
        
        c = cv2.resize(np.array(c),(500,500))
        newimage = c*(1-self.gradcamvalue) + array*(self.gradcamvalue)
        img = pygame.surfarray.make_surface(newimage)
        imgrect = img.get_rect()
        imgrect.center = (self.interface.sw/3, self.interface.sh/2)
        # Display the image
        self.display.blit(img, imgrect)
        
        self.display_text('Model output', (255,255,255),(self.interface.sw/3, self.interface.sh/5))
        
        i = 0
        # Iterate through the labels and probabilities
        for label, prob in zip(sorted_labels, sorted_prob):
            i += 1
            # Make the output text
            text = label + ': ' + str(round(prob,3)) + '%'
            # Display the text
            self.display_text(text, (100,100,200),(3*self.interface.sw/4, self.interface.sh/5+i*30), font_type='display')
        
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
            if type(button) == slider:
                if button.drag:
                    if button.ID == self.buttons[2].ID:
                        self.gradcam = button.follow(pygame.mouse.get_pos())
                    elif button.ID == self.buttons[1].ID: 
                        self.gradcamvalue = button.follow(pygame.mouse.get_pos())
                
            button.show()
                
        # Update the display
        pygame.display.flip()
        
        # Is the program still running?
        return running

class Name_Image(Page):
    def __init__(self):
        super().__init__()
        # Make a path to the folder of images
        self.imagespath = os.path.join(os.getcwd(), 'Images')
        self.imgname = ''
        self.cursor = False
        self.prevtime = time.time()
    
    def tick(self):
        running = True
        self.display.fill(self.interface.background_colour)
        
        currtime = time.time()
        if currtime - self.prevtime > 0.5:
            self.cursor = not self.cursor 
            self.prevtime = time.time()
        
        text_to_display = self.imgname
        if self.cursor:
            text_to_display += '_'
        
        self.img = captureimage.img
        self.display_text('What would you like to name the image?', (255,255,255), (self.interface.sw/2, self.interface.sh/4))
        self.display_text(text_to_display, (255,255,255), (self.interface.sw/2, self.interface.sh/3), font_type='display')
        
        button_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                button_up = True
            if event.type == pygame.KEYDOWN:
                character = event.unicode
                self.shift = False
                if not character.isprintable():
                    if event.key == pygame.K_BACKSPACE:
                        self.imgname = self.imgname[0:len(self.imgname)-1]
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.shift = True
                else:
                    if self.shift:
                        character = character.upper()
                    if character != '.':
                        self.imgname += character
                
        # Iterate through every button
        for button in self.buttons:
            # Update and check if the button is hovering
            hovering = button.is_hovering()
            if hovering and button_up:
                button.click()
                if button.ID == self.buttons[1].ID:
                    image_path = os.path.join(self.imagespath, self.imgname + '.jpg') # Store the image in the "Images" folder
                    pygame.image.save_extended(self.img, image_path) # Save the image with inputted name + .jpg
                
            button.show()
                
        # Update the display
        pygame.display.flip()
        
        # Is the program still running?
        return running

# Instantiate every page
home = Home()
captureimage = Capture_Image()
selectimage = Select_Image()
displayimage_c = Display_Image_c()
displayimage_l = Display_Image_l()
model_page = Model()
nameimage = Name_Image()

# Add each page to the UI
UI.add(home)
UI.add(captureimage)
UI.add(selectimage)
UI.add(displayimage_l)
UI.add(displayimage_c)
UI.add(model_page)
UI.add(nameimage)

# Path to the 'Button Images' directory
images = os.path.join(os.getcwd(),'Button Images')

# Get the images
right_arrow = pygame.image.load(os.path.join(images, 'right arrow.png'))
left_arrow = pygame.image.load(os.path.join(images, 'left arrow.png'))
camera_icon = pygame.image.load(os.path.join(images, 'camera icon.png'))
cross = pygame.image.load(os.path.join(images, 'cross.png'))
tick = pygame.image.load(os.path.join(images, 'tick.png'))
back_icon = pygame.image.load(os.path.join(images, 'back.png'))
home_icon = pygame.image.load(os.path.join(images, 'home.png'))
save_icon = pygame.image.load(os.path.join(images, 'save.png'))

# Instantiate the back button
back = Back((UI.sw/10, UI.sh/10), (100,100), image=back_icon)

# Instantiate navigation buttons
home_captureimage = navigation((UI.sw/5, 4*UI.sh/5), (200, 160), captureimage, image=left_arrow, text='Capture an image')
home_selectimage = navigation((4*UI.sw/5, 4*UI.sh/5), (200, 160), selectimage, image=right_arrow, text='Load an image')

take_image = navigation((UI.sw/2, 4*UI.sh/5), (200, 200), displayimage_c, image=camera_icon)
take_image.active = False
displayimagec_nameimage = navigation((2*UI.sw/3, 4*UI.sh/5), (80, 80), nameimage, image=tick)
disliketocapture = navigation((UI.sw/3, 4*UI.sh/5), (80, 80), captureimage, image=cross)
nameimage_home = navigation((4*UI.sw/5, 4*UI.sh/5), (150, 150), home, image=save_icon)

selectimage_displayimage_l = navigation((UI.sw/2, 4*UI.sh/5), (200, 160), displayimage_l, image=right_arrow, text='View the image')
displayimagel_model = navigation((2*UI.sw/3, 4*UI.sh/5), (80, 80), model_page, image=tick)
disliketoselect = navigation((UI.sh/3, 4*UI.sw/5), (80, 80), selectimage, image=cross)
model_home = navigation((UI.sh/3, 5*UI.sw/6), (150, 150), home, image=home_icon)

# Instantiate sliders
gradcam = slider((4*UI.sw/5-100, 4*UI.sh/5), (80,80), 0, 200,colour=(200,200,210))
gradcamvalue = slider((4*UI.sw/5-100, 4*UI.sh/5-100), (80,80), 0, 200,colour=(200,200,210))

# Give every page but the home page a back button
captureimage.add(back)
selectimage.add(back)
displayimage_c.add(back)
displayimage_l.add(back)
model_page.add(back)
nameimage.add(back)

# Add all navigation buttons
home.add(home_captureimage)
home.add(home_selectimage)

# Add all sliders
model_page.add(gradcam)
model_page.add(gradcamvalue)

captureimage.add(take_image)
displayimage_c.add(displayimagec_nameimage)
displayimage_c.add(disliketocapture)
nameimage.add(nameimage_home)

selectimage.add(selectimage_displayimage_l)
displayimage_l.add(displayimagel_model)
displayimage_l.add(disliketoselect)
model_page.add(model_home)