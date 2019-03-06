import pygame, sys, easygui, os
import time
import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from PIL import *
from pylab import *

from OpenGL.GL import *
from pygame.locals import *
from pygame.constants import *
from OpenGL.GLU import *
 

fill = False
temp=[0, 0, 0]


class storer():
    def __init__(self, newone): #Define all the variables
        self.new = newone   
        self.color = [0, 0, 0] 
        self.bsize = 5
        
        self.brush = "Square" #Brush shape
        self.down = False #Bool of whether left mouse button is down
        self.down2 = False #Bool of whether right mouse button is down
        self.loadpic = False 
        self.imagename = "New File"
        self.saved = True
        self.bgcolor = [255, 255, 255]#Set of RGB values of the background. Currently not really that useful. ROFL!
       
        self.mousepos = [0, 0]
        self.fillcolor = [255, 255, 255]
        


    def objloader(self):
        PATH= 'E:'

        

        def MTL(filename):
            contents = {}
            mtl = None
            for line in open(PATH + filename, "r"):
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue
                if values[0] == 'newmtl':
                    mtl = contents[values[1]] = {}
                elif mtl is None:
                    raise ValueError, "mtl file doesn't start with newmtl stmt"
                elif values[0] == 'map_Kd':
                    
                    mtl[values[0]] = values[1]
                    surf = pygame.image.load(mtl['map_Kd'])
                    image = pygame.image.tostring(surf, 'RGBA', 1)
                    ix, iy = surf.get_rect().size
                    texid = mtl['texture_Kd'] = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, texid)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                        GL_LINEAR)
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                        GL_UNSIGNED_BYTE, image)
                else:
                    mtl[values[0]] = map(float, values[1:])
            return contents
 
        class OBJ:
            def __init__(self, filename, swapyz=False):
               
                self.vertices = []
                self.normals = []
                self.texcoords = []
                self.faces = []
 
                material = None
                for line in open(PATH + filename, "r"):
                    if line.startswith('#'): continue
                    values = line.split()
                    if not values: continue
                    if values[0] == 'v':
                        v = map(float, values[1:4])
                        if swapyz:
                            v = v[0], v[2], v[1]
                        self.vertices.append(v)
                    elif values[0] == 'vn':
                        v = map(float, values[1:4])
                        if swapyz:
                            v = v[0], v[2], v[1]
                        self.normals.append(v)
                    elif values[0] == 'vt':
                        self.texcoords.append(map(float, values[1:3]))
                    elif values[0] in ('usemtl', 'usemat'):
                        material = values[1]
                    elif values[0] == 'mtllib':
                        self.mtl = MTL(values[1])
                    elif values[0] == 'f':
                        face = []
                        texcoords = []
                        norms = []
                        for v in values[1:]:
                            w = v.split('/')
                            face.append(int(w[0]))
                            if len(w) >= 2 and len(w[1]) > 0:
                                texcoords.append(int(w[1]))
                            else:
                                texcoords.append(0)
                            if len(w) >= 3 and len(w[2]) > 0:
                                norms.append(int(w[2]))
                            else:
                                norms.append(0)
                        self.faces.append((face, norms, texcoords, material))
 
                self.gl_list = glGenLists(1)
                glNewList(self.gl_list, GL_COMPILE)
                glEnable(GL_TEXTURE_2D)
                glFrontFace(GL_CCW)
                for face in self.faces:
                    vertices, normals, texture_coords, material = face
 
                    mtl = self.mtl[material]
                    if 'texture_Kd' in mtl:
                       
                        glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                    else:
                       
                        glColor(*mtl['Kd'])
 
                    glBegin(GL_POLYGON)
                    for i in range(len(vertices)):
                        if normals[i] > 0:
                            glNormal3fv(self.normals[normals[i] - 1])
                        if texture_coords[i] > 0:
                            glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                        glVertex3fv(self.vertices[vertices[i] - 1])
                    glEnd()
                glDisable(GL_TEXTURE_2D)
                glEndList()


 
        pygame.init()
        viewport = (800,600)
        hx = viewport[0]/2
        hy = viewport[1]/2

        srf = pygame.display.set_mode(viewport,OPENGL | DOUBLEBUF)
        glClearColor(1.0, 1.0, 1.0, 0.0) # white
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)           
 
       

        if imgg[0]==1:
            objname=str(int(fno[0]))+"b"+".obj"
            
        elif imgg[1]==1:
            objname=str(int(fno[1]))+"b"+".obj"
        elif imgg[2]==1:
            objname=str(int(fno[2]))+"b"+".obj"
        elif imgg[3]==1:
            objname=str(int(fno[3]))+"b"+".obj"
        elif imgg[4]==1:
            objname=str(int(fno[4]))+"b"+".obj"


        print objname
        obj = OBJ(objname, swapyz=False)
 
        clock = pygame.time.Clock()
 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(60.0, width/float(height), 0.1, 1000.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)
 
        rx, ry = (0,0)
        tx, ty = (0,0)
        zpos = 5
        rotate = move = False
        a=0
        
        while 1:
            clock.tick(30)
            for e in pygame.event.get():
                if e.type == QUIT:
                    import drawN1
                    sys.exit()
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    sys.exit()
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 4: zpos = max(1, zpos-1)
                    elif e.button == 5: zpos += 1
                    elif e.button == 1: rotate = True
                    elif e.button == 3: move = True
                elif e.type == MOUSEBUTTONUP:
                    if e.button == 1: rotate = False
                    elif e.button == 3: move = False
                elif e.type == MOUSEMOTION:
                    i, j = e.rel
                    if rotate:
                        rx += i
                        ry += j
                    if move:
                        tx += i
                        ty -= j
                elif (e.type==pygame.KEYDOWN):
                        
                        
                        
                        if (e.key==K_SPACE):
                            
                            a=a+1
                            filename="screenshot"+ str(a)+ ".png" 
                            pygame.image.save(srf, filename)
                                            
 
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
 
            
            glTranslate(tx/20., ty/20., - zpos)
            glRotate(ry, 1, 0, 0)
            glRotate(rx, 0, 1, 0)
            glCallList(obj.gl_list)
 
            pygame.display.flip()

        cv2.waitKey()
        cv2.destroyAllWindows()




    def matcher(self):
        Flag[0]=0
        Flag[1]=0
        pygame.image.save(drawspace, 'sketch.png')
        
        hog = cv2.HOGDescriptor()

        img1 = cv2.imread('edgeshot1.png', 0)   # replace image for trials

        ht, wid = img1.shape[:2]
        scale = 2
        ht = ht/scale
        wid = wid/scale

        img2 = cv2.imread('sketch.png', 0)
        img2 = cv2.resize(img2, (wid, ht), interpolation=cv2.INTER_CUBIC)
        #cv2.imshow("IMAGE2", img2)


        p = hog.compute(img2, winStride=(64,128), padding=(0, 0))
        p=np.asarray(p)
        h22 = p/np.linalg.norm(p)

        h2 = h22[:,0]

        G1=np.zeros((153,5,45360))
        s=zeros(6)
        indexm=zeros(153)
        simm=zeros(153)
        b=1
        a=0
        c=0

        G1=np.load("3Darray.npy")

        while b<153:

            c=0
            a=a+1
        
            for i in range (0,5):
        
                s[i] = np.dot(G1[a,i,:], h2)  
#             print "similarity = %.3f" % s[i]

            indexm[b]=(np.argmax(s)+1)
            simm[b]= s.max()    
            b=b+1
   
        ind=simm.argsort()[-5:][::-1]
        #print "\nTop 10 Match indices"
        #print ind
        #print "\nTop 10 simmilarity values"
        #print simm[ind[:]]

        #print indexm


        cv2.imshow("Sketch",img2)
        a1=0
        c1=0
        c11=0
        #print "\nTop 10 Matches"
        for i in range(0,5):
            a1=ind[i]
            c1=indexm[ind[i]]
            c11=int(c1)
            output=str(a1)+ "/" + str(c11) + ".png"
        #   print output
            name= "OUTPUT"+str(i)
            fno[i]=a1
            imgno[i]=c11
            
            outimg = cv2.imread(output, 0)
            cv2.imshow(name,outimg)
        '''
        print time.clock() - start_time, "seconds"    
        cv2.waitKey()
        cv2.destroyAllWindows()
        '''
                      
    
    def save(self):
        extensionchoice = "Temp {.png}"
        if extensionchoice == "Temp {.png}":
            extension = ".png"
       
        savelocation = easygui.filesavebox()
        if savelocation == None:
            pass
        else:
            savelocation = os.path.splitext(savelocation)[0]
            pygame.image.save(drawspace, savelocation + extension)
            self.imagename = savelocation + extension
            pygame.display.set_caption("DrawN-" + store.imagename)
            self.saved = True
    
    def mainmenu(self):
        menuchoice = easygui.choicebox("Select a task", title = "Main Menu", choices = ["Save", "Open", "New"])
        if menuchoice == "Save":
            self.save()
        
        elif menuchoice == "Open":
            store.loadpic = True
            question = easygui.fileopenbox()
            if question == None:
                self.mainmenu()
            else:
                try:
                    store.pic = pygame.image.load(question)
                    store.new = store.pic.get_size()
                    screen = pygame.display.set_mode([store.new[0]+100, store.new[1]])
                    screen.fill([230, 230, 230])
                    drawspace = pygame.surface.Surface(store.new)
                    drawspace.fill(store.bgcolor)
                except:
                    easygui.msgbox("Not a supported file type. Supported file types are: .jpg, .gif, .png, .bmp, .tga, .pcx, .lbm, .xpm, and  .tif. Please select a different file.", title = "Open Error")
                    self.mainmenu()

        elif menuchoice == "New":
             import drawN1
             sys.exit()
             
            
    
    def getscore(self):
         Flag[0]=1
         Flag[1]=1
         pygame.image.save(drawspace, 'sketchscore.png')
         hog = cv2.HOGDescriptor()
         img1 = cv2.imread('sketchscore.png', 0)   
         ht, wid = img1.shape[:2]
         scale = 2
         ht = ht/scale
         wid = wid/scale
         #cv2.imshow('name1',img1)
         img1 = cv2.resize(img1, (wid, ht), interpolation=cv2.INTER_CUBIC)
         q = hog.compute(img1, winStride=(64,128), padding=(0, 0))
         q=np.asarray(q)
         q22= q/np.linalg.norm(q)
         q2= q22[:,0]


         filename1=str(int(fdis[0]))+ "/"+"shadow"+ str(int(imgdis[0]))+".png"
         img2 = cv2.imread(filename1, 0)
         img2 = cv2.resize(img2, (wid, ht), interpolation=cv2.INTER_CUBIC)
         #cv2.imshow('name2',img2)
         p = hog.compute(img2, winStride=(64,128), padding=(0, 0))
         p=np.asarray(p)
         p22 = p/np.linalg.norm(p)
         p2 = p22[:,0]

         s1= np.dot(q2, p2)  
         print "similarity = %.3f" % (s1*100)
         
             
            
    def matchscore(self):
          
         
         Flag[0]=1
         Flag[1]=1
         drawspace.fill([255, 255, 255])
         
         matchchoice = easygui.choicebox("Select a task", title = "MatchChoice", choices = ["Traced/shadow", "New"])

         if matchchoice == "Traced/shadow": 
                  
             if imgg[0]==1:
                #shadowfile=str(int(fno[0]))+ "/"+"shadow"+ str(int(imgno[0]))+ ".png"
                imgdis[0]=imgno[0]
                fdis[0]=fno[0]
             elif imgg[1]==1:
                #shadowfile=str(int(fno[0]))+ "/"+"shadow"+ str(int(imgno[1]))+ ".png"
                imgdis[0]=imgno[1]
                fdis[0]=fno[1]
             elif imgg[2]==1:
                #shadowfile=str(int(fno[0]))+ "/"+"shadow"+ str(int(imgno[2]))+ ".png"
                imgdis[0]=imgno[2]
                fdis[0]=fno[2]
             elif imgg[3]==1:
                #shadowfile=str(int(fno[0]))+ "/"+"shadow"+ str(int(imgno[3]))+ ".png"
                imgdis[0]=imgno[3]
                fdis[0]=fno[3]
             elif imgg[4]==1:
                #shadowfile=str(int(fno[0]))+ "/"+"shadow"+ str(int(imgno[4]))+ ".png"
                imgdis[0]=imgno[4]
                fdis[0]=fno[4]

         elif matchchoice == "New":
                store.loadpic = True
                question1 = easygui.fileopenbox()
                if question1 == None:
                    self.matchscore()
                else:
                    try:
                        newimage = pygame.image.load(question1)
                        newimage = question1
                    except:
                        easygui.msgbox("Not a supported file type. Supported file types are: .jpg, .gif, .png, .bmp, .tga, .pcx, .lbm, .xpm, and  .tif. Please select a different file.", title = "Open Error")
                        self.matchscore()
         elif matchchoice == "Exit":
                sys.exit()

          
  
    def shadow(self):
        Flag[0]=0
        Flag[1]=0
        drawspace.fill([255, 255, 255])
        if imgg[0]==1:
            shadowfile=str(int(fno[0]))+ "/"+"shadow"+ str(int(imgno[0]))+ ".png"
            
        elif imgg[1]==1:
            shadowfile=str(int(fno[1]))+ "/"+"shadow"+ str(int(imgno[1]))+ ".png"
        elif imgg[2]==1:
            shadowfile=str(int(fno[2]))+ "/"+"shadow"+ str(int(imgno[2]))+ ".png"
        elif imgg[3]==1:
            shadowfile=str(int(fno[3]))+ "/"+"shadow"+ str(int(imgno[3]))+ ".png"
        elif imgg[4]==1:
            shadowfile=str(int(fno[4]))+ "/"+"shadow"+ str(int(imgno[4]))+ ".png"
         
        pythonlogo = pygame.image.load(shadowfile).convert()
        pythonlogo=pygame.transform.scale(pythonlogo,(800,600))
        pythonlogo.set_alpha(120)
        drawspace.blit(pythonlogo, [0,0]) 
        
    def image1(self):
        imgg[0]=1
        imgg[1]=0
        imgg[2]=0
        imgg[3]=0
        imgg[4]=0
        
        
    def image2(self):
        imgg[0]=0
        imgg[1]=1
        imgg[2]=0
        imgg[3]=0
        imgg[4]=0
        
    def image3(self):
        imgg[0]=0
        imgg[1]=0
        imgg[2]=1
        imgg[3]=0
        imgg[4]=0

    def image4(self):
        imgg[0]=0
        imgg[1]=0
        imgg[2]=0
        imgg[3]=1
        imgg[4]=0

    def image5(self):
        imgg[0]=0
        imgg[1]=0
        imgg[2]=0
        imgg[3]=0
        imgg[4]=1
    
    
         
    def drawline(self, point_one, point_two, width):
        self.color = [0, 0, 0]
        pygame.draw.line(drawspace, self.color, point_one, point_two, width)

    def erase(self, point_one, point_two, width):
        self.color = [255, 255, 255]
        pygame.draw.line(drawspace, self.color, point_one, point_two, width)
        

title = "New file"

fieldValues = [600,800]

store = storer([])

def newfile():
    store.loadpic = False
    open_or_new = easygui.buttonbox("Welcome to DrawN", title = "DrawN: Sketch and Build", choices = ["New File", "Open", "Exit"])
    if open_or_new == "New File":
        store.loadpic = False
        
        if fieldValues == None:
            newfile()
        else:
            try:
                store.new = [int(fieldValues[1]), int(fieldValues[0])]
            except:
               newfile()
    elif open_or_new == "Open":
        store.loadpic = True
        question = easygui.fileopenbox()
        if question == None:
            newfile()
        else:
            try:
                store.pic = pygame.image.load(question)
                store.new = store.pic.get_size()
                store.imagename = question
            except:
                easygui.msgbox("Not a supported file type. Supported file types are: .jpg, .gif, .png, .bmp, .tga, .pcx, .lbm, .xpm, and  .tif. Please select a different file.", title = "Open Error")
                newfile()
    elif open_or_new == "Exit":
        sys.exit()

#Sets up the entire program----------------------------------------------------
newfile()
pygame.init()
imgno=zeros(5)
fno=zeros(5)
imgg=zeros(5)
Flag=zeros(2)
imgdis=zeros(1)
fdis=zeros(1)
'''
img1=0
img2=0
img3=1
img4=0
img5=0
'''

pygame.display.set_icon(pygame.image.load("folder1/draw.gif"))

if store.new[1] < 300:
    screen = pygame.display.set_mode([store.new[0]+245, store.new[1] + 300 - store.new[1]])
else:
    screen = pygame.display.set_mode([store.new[0]+245, store.new[1]])
screen.fill([230, 230, 230])
drawspace = pygame.surface.Surface(store.new)
drawspace.fill(store.bgcolor)

if store.loadpic == True:
    drawspace.blit(store.pic, [0, 0])
#Sets the caption
pygame.display.set_caption("DrawN: Interactive Freehand Sketching and Sketch Based 3D Object Retrieval- " + store.imagename)
#Creates the clock object
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 25)

brushbox = pygame.image.load("folder1/mat.gif")

toolbox = pygame.image.load("folder1/3d.gif")
menubox = pygame.image.load("folder1/menu.gif")
tracebox = pygame.image.load("folder1/trace.gif")
scorebox = pygame.image.load("folder1/game.jpg")
getbox = pygame.image.load("folder1/get.jpg")
'''
# Display images
file1="edgeshot"+ str(int(imgno[0]))+ ".png"
file2="edgeshot"+ str(int(imgno[1]))+ ".png"
file3="edgeshot"+ str(int(imgno[2]))+ ".png"
file4="edgeshot"+ str(int(imgno[3]))+ ".png"



show1=pygame.image.load(file1)
show2=pygame.image.load(file2)
show3=pygame.image.load(file3)
show4=pygame.image.load(file4)

show1=pygame.transform.scale(show1,(100,100))
show2=pygame.transform.scale(show2,(100,100))
show3=pygame.transform.scale(show3,(100,100))
show4=pygame.transform.scale(show4,(100,100))
'''

#The main loop-----------------------------------------------------------------
while 1:
    clock.tick(30)
    
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            if store.saved == False:
                exiting = easygui.buttonbox("You have unsaved changes. Quit anyway?", title = 'Unsaved work', choices = ["Yes", "No"])
                if exiting == "Yes":
                    sys.exit()
            else:
                sys.exit()
        elif event.type == pygame.USEREVENT:
            if store.down:
                testoldpos = testpos
                testpos = pygame.mouse.get_pos()
                store.drawline(testoldpos, testpos, store.bsize)
            elif store.down2:
                testoldpos = testpos
                testpos = pygame.mouse.get_pos()
                store.erase(testoldpos, testpos, store.bsize)
       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] < store.new[0]:
                    if event.button == 1:#Left mouse button(draw)
                        store.down = True
                        store.saved = False
                        testpos = pygame.mouse.get_pos()
                                    
                    elif event.button == 3:#Right mouse button(erase)
                        store.down2= True
                        store.saved = False
                        testpos = pygame.mouse.get_pos()
            else:
                if pygame.mouse.get_pos()[0]>store.new[0]+25 and pygame.mouse.get_pos()[0]<store.new[0]+75 and pygame.mouse.get_pos()[1]>10 and pygame.mouse.get_pos()[1]<60:
                    store.matcher()
                elif pygame.mouse.get_pos()[0]>store.new[0]+100 and pygame.mouse.get_pos()[0]<store.new[0]+150 and pygame.mouse.get_pos()[1]>10 and pygame.mouse.get_pos()[1]<60:
                    store.objloader()
               
                elif pygame.mouse.get_pos()[0]>store.new[0]+175 and pygame.mouse.get_pos()[0]<store.new[0]+225 and pygame.mouse.get_pos()[1]>10 and pygame.mouse.get_pos()[1]<60:
                    store.mainmenu()

                elif pygame.mouse.get_pos()[0]>store.new[0]+25 and pygame.mouse.get_pos()[0]<store.new[0]+75 and pygame.mouse.get_pos()[1]>80 and pygame.mouse.get_pos()[1]<130:
                    store.shadow()
                    
                elif pygame.mouse.get_pos()[0]>store.new[0]+100 and pygame.mouse.get_pos()[0]<store.new[0]+150 and pygame.mouse.get_pos()[1]>80 and pygame.mouse.get_pos()[1]<130:
                    store.matchscore()

                elif pygame.mouse.get_pos()[0]>store.new[0]+175 and pygame.mouse.get_pos()[0]<store.new[0]+225 and pygame.mouse.get_pos()[1]>80 and pygame.mouse.get_pos()[1]<130:
                    store.getscore()
                
                elif Flag[0]==0 and Flag[1]==0:                 # showing the images
                
                    if pygame.mouse.get_pos()[0]>store.new[0]+10 and pygame.mouse.get_pos()[0]<store.new[0]+110 and pygame.mouse.get_pos()[1]>170 and pygame.mouse.get_pos()[1]<270:
                        store.image1()

                    elif pygame.mouse.get_pos()[0]>store.new[0]+130 and pygame.mouse.get_pos()[0]<store.new[0]+250 and pygame.mouse.get_pos()[1]>170 and pygame.mouse.get_pos()[1]<270:
                        store.image2()    
    
                    elif pygame.mouse.get_pos()[0]>store.new[0]+10 and pygame.mouse.get_pos()[0]<store.new[0]+110 and pygame.mouse.get_pos()[1]>300 and pygame.mouse.get_pos()[1]<400:
                        store.image3()

                    elif pygame.mouse.get_pos()[0]>store.new[0]+130 and pygame.mouse.get_pos()[0]<store.new[0]+250 and pygame.mouse.get_pos()[1]>300 and pygame.mouse.get_pos()[1]<400:
                        store.image4()

                    elif pygame.mouse.get_pos()[0]>store.new[0]+50 and pygame.mouse.get_pos()[0]<store.new[0]+150 and pygame.mouse.get_pos()[1]>430 and pygame.mouse.get_pos()[1]<530:
                        store.image5()
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:#Left mouse button(draw)
                store.down = False
            elif event.button == 3:#Right mouse button(erase)
                store.down2 = False
                
                
        
    

    if Flag[0]==0 and Flag[1]==0:                 # 

        screen.fill([230, 230, 230])
        screen.blit(drawspace, [0, 0])
   
        screen.blit(brushbox, [store.new[0] + 25, 10])
        screen.blit(toolbox, [store.new[0] + 100, 10])
        screen.blit(menubox, [store.new[0] + 175, 10])
        screen.blit(tracebox, [store.new[0] + 25, 80])
        screen.blit(scorebox, [store.new[0] + 100, 80])
        screen.blit(getbox, [store.new[0] + 175, 80])

        # Display images
        file1=str(int(fno[0]))+"/"+"crop"+ str(int(imgno[0]))+ ".png"
        file2=str(int(fno[1]))+"/"+"crop"+ str(int(imgno[1]))+ ".png"
        file3=str(int(fno[2]))+"/"+"crop"+ str(int(imgno[2]))+ ".png"
        file4=str(int(fno[3]))+"/"+"crop"+ str(int(imgno[3]))+ ".png"
        file5=str(int(fno[4]))+"/"+"crop"+ str(int(imgno[4]))+ ".png"


        show1=pygame.image.load(file1)
        show2=pygame.image.load(file2)
        show3=pygame.image.load(file3)
        show4=pygame.image.load(file4)
        show5=pygame.image.load(file5)

        show1=pygame.transform.scale(show1,(100,100))
        show2=pygame.transform.scale(show2,(100,100))
        show3=pygame.transform.scale(show3,(100,100))
        show4=pygame.transform.scale(show4,(100,100))
        show5=pygame.transform.scale(show5,(100,100))
    
        #Putting the images
        screen.blit(show1, [store.new[0] + 10, 170]) 
        screen.blit(show2, [store.new[0] + 130, 170])
        screen.blit(show3, [store.new[0] + 10, 300])
        screen.blit(show4, [store.new[0] + 130, 300])
        screen.blit(show5, [store.new[0] + 70, 430])

    elif Flag[0]==1 and Flag[1]==1:
        
        screen.fill([230, 230, 230])
        screen.blit(drawspace, [0, 0])
   
        screen.blit(brushbox, [store.new[0] + 25, 10])
        screen.blit(toolbox, [store.new[0] + 100, 10])
        screen.blit(menubox, [store.new[0] + 175, 10])
        screen.blit(tracebox, [store.new[0] + 25, 80])
        screen.blit(scorebox, [store.new[0] + 100, 80])
        screen.blit(getbox, [store.new[0] + 175, 80])

        file1=str(int(fdis[0]))+ "/" +"crop"+ str(int(imgdis[0]))+ ".png"
        file2=str(int(fdis[0]))+ ".png"
        show1=pygame.image.load(file1)
        show2=pygame.image.load(file2)
        show1=pygame.transform.scale(show1,(230,220))
        show2=pygame.transform.scale(show2,(230,220))
        screen.blit(show1, [store.new[0] + 10, 150])
        screen.blit(show2, [store.new[0] + 10, 370])  
        
    pygame.display.flip()
