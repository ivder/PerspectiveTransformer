from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np

class PerspectiveTransform():
    def __init__(self, master):
        self.parent = master
        self.coord = [] 	# x,y coordinate
        self.dot = []
        self.file = '' 	 	#image path
        self.filename ='' 	#image filename
        
        #setting up a tkinter canvas with scrollbars
        self.frame = Frame(self.parent, bd=2, relief=SUNKEN)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
        self.xscroll.grid(row=1, column=0, sticky=E+W)
        self.yscroll = Scrollbar(self.frame)
        self.yscroll.grid(row=0, column=1, sticky=N+S)
        self.canvas = Canvas(self.frame, bd=0, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        self.xscroll.config(command=self.canvas.xview)
        self.yscroll.config(command=self.canvas.yview)
        self.frame.pack(fill=BOTH,expand=1)
        self.addImage()
        
        #mouseclick event and button
        self.canvas.bind("<Button 1>",self.insertCoords)
        self.canvas.bind("<Button 3>",self.removeCoords)
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 0, column = 2, columnspan = 2, sticky = N+E)
        self.addImgBtn = Button(self.ctrPanel, text="Browse", command=self.addImage)
        self.addImgBtn.grid(row=0,column=2, pady = 5, sticky =NE)
        self.saveBtn = Button(self.ctrPanel, text="Save", command=self.saveImage)
        self.saveBtn.grid(row=1,column=2, pady = 5, sticky =NE)
    
    #adding the image
    def addImage(self):
        self.coord = []
        self.file = askopenfilename(parent=self.parent, initialdir="image/",title='Choose an image.')
        self.filename = self.file.split('/')[-1]
        self.filename = self.filename.rstrip('.jpg')
        self.img = ImageTk.PhotoImage(Image.open(self.file))
        self.canvas.create_image(0,0,image=self.img,anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL), width=self.img.width(), height=self.img.height())
        
    
    #Save coord according to mouse left click
    def insertCoords(self, event):
        #outputting x and y coords to console
        self.coord.append([event.x, event.y])
        r=3
        self.dot.append(self.canvas.create_oval(event.x - r, event.y - r, event.x + r, event.y + r, fill="#ff0000"))         #print circle
        if (len(self.coord) == 4):
            self.Transformer()
            self.canvas.delete("all")
            self.canvas.create_image(0,0,image=self.result,anchor="nw")
            self.canvas.image = self.result
    
    #remove last inserted coord using mouse right click
    def removeCoords(self, event=None):
        del self.coord[-1]
        self.canvas.delete(self.dot[-1])
        del self.dot[-1]
    
    def Transformer(self):   
        frame = cv2.imread(self.file)
        frame_circle = frame.copy()
        #points = [[480,90],[680,90],[0,435],[960,435]]
        cv2.circle(frame_circle, tuple(self.coord[0]), 5, (0, 0, 255), -1)
        cv2.circle(frame_circle, tuple(self.coord[1]), 5, (0, 0, 255), -1)
        cv2.circle(frame_circle, tuple(self.coord[2]), 5, (0, 0, 255), -1)
        cv2.circle(frame_circle, tuple(self.coord[3]), 5, (0, 0, 255), -1)
        
        widthA = np.sqrt(((self.coord[3][0] - self.coord[2][0]) ** 2) + ((self.coord[3][1] - self.coord[2][1]) ** 2))
        widthB = np.sqrt(((self.coord[1][0] - self.coord[0][0]) ** 2) + ((self.coord[1][1] - self.coord[0][1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
         
        heightA = np.sqrt(((self.coord[1][0] - self.coord[3][0]) ** 2) + ((self.coord[1][1] - self.coord[3][1]) ** 2))
        heightB = np.sqrt(((self.coord[0][0] - self.coord[2][0]) ** 2) + ((self.coord[0][1] - self.coord[2][1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
     
        print(self.coord)
        pts1 = np.float32(self.coord)    
        pts2 = np.float32([[0, 0], [maxWidth-1, 0], [0, maxHeight-1], [maxWidth-1, maxHeight-1]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        self.result_cv = cv2.warpPerspective(frame, matrix, (maxWidth,maxHeight))
         
        #cv2.imshow("Frame", frame_circle)
        #cv2.imshow("Perspective transformation", result_cv)
        
        result_rgb = cv2.cvtColor(self.result_cv, cv2.COLOR_BGR2RGB)
        self.result = ImageTk.PhotoImage(image = Image.fromarray(result_rgb))
        
    def saveImage(self):
        cv2.imwrite("result/"+self.filename+"_res.jpg", self.result_cv)
        print(self.filename+" is saved!")

#---------------------------------
if __name__ == '__main__':
    root = Tk()
    #root.geometry("1360x740")
    transformer = PerspectiveTransform(root)
    root.mainloop()
