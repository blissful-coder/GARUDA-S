# Assuming Python 2.x
# For Python 3.x support change print -> print(..) and Tkinter to tkinter
from tkinter import *
from pyscreenshot import grab
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from pytesseract import Output
import time
from ctypes import windll
user32 = windll.user32
user32.SetProcessDPIAware()

class alien(object):
      def __init__(self):
         self.root = Tk()
         self.screen_width = self.root.winfo_screenwidth()
         self.screen_height = self.root.winfo_screenheight()
         self.canvas = Canvas(self.root, width= self.screen_width, height = self.screen_height, background="black")
         self.canvas.pack()
         self.zone = self.canvas.create_oval(20, 260, 35, 275, outline='black', fill='white')
         self.textentry = Entry(self.canvas,bg="white",fg="black",bd=5,font=("Courier", 44))
         self.textwindow = self.canvas.create_window(self.root.winfo_screenwidth()-400, self.root.winfo_screenheight()-50, window=self.textentry, height=50, width=400)
         #self.textwindow.attributes('-alpha', 1)
         self.searchbarvisible = True
         self.zonebox = []
         self.zonex = 0
         self.zoney = 0
         self.canvas.pack()
         self.root.attributes('-alpha', 0.4)
         self.fullScreen = True
         self.root.attributes("-fullscreen", self.fullScreen)
         self.root.bind("<Button-1>", self.drawOnClick)
         self.root.bind('<Escape>',self.toggle_geom)        #Toggle Full Screen
         self.root.bind('<Control-f>',self.toggle_searchbar)   #Show Text Input Window
         self.root.bind('<F11>',self.take_screenshot)     #Search in Screen
         self.root.mainloop()
      
      def drawOnClick(self,event):
         self.zonex, self.zoney = event.x, event.y
         print('{}, {}'.format(self.zonex, self.zoney))
         current = self.canvas.coords(self.zone)
         self.canvas.move(self.zone, self.zonex-current[0]-10, self.zoney-current[1]-10)
         self.canvas.update()

      def toggle_geom(self,event):
         self.fullScreen = not self.fullScreen
         self.root.attributes("-fullscreen", self.fullScreen)
         self.canvas.update()

      def toggle_searchbar(self,event):
         self.searchbarvisible = not self.searchbarvisible
         self.textentry.visible = self.searchbarvisible
         self.textwindow.visible = self.searchbarvisible
         self.canvas.update()

      def take_screenshot(self,event):
         targetString = self.textentry.get()
         print("Searching on Screen: {}".format(targetString))
         im = grab(bbox=(0, 0, self.screen_width, self.screen_height))
         im.save('screenshot.png')
         pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
         im = Image.open('screenshot.png')
         # imb = im.convert('1') # convert image to black and white
         # imb.save('bandw.png')
         textStrings = pytesseract.image_to_string(im)
         textZones = pytesseract.image_to_data(im, output_type=Output.DICT)
         with open('ocr.txt', 'w') as file:
            file.write(textStrings)
         with open('ocrboxes.txt', 'w') as fp:
            fp.write('\n'.join('%s' % x for x in textZones))
         n_boxes = len(textZones['level'])
         count = 0
         for i in range(n_boxes):
            (x, y, w, h, confi, text) = (textZones['left'][i], textZones['top'][i], textZones['width'][i], textZones['height'][i], textZones['conf'][i], textZones['text'][i])
            if(-1!=int(confi)):
               if(text == targetString):
                  print("Here: {} {} {} {} {} {}".format(x,y,w,h,confi,text))
                  self.zonebox.append(self.canvas.create_rectangle( x,  y, x+w, y+h, fill="yellow"))
                  count = count + 1
         #self.root.attributes('-alpha', 1)
         self.canvas.update()
         print("Target {} found {} times.".format(targetString,count))

alien()


