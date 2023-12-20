import tkinter as tk
import AppKit

# Function to create tkinter window and canvas
def create_canvas(x, y, width, height):
    root = tk.Tk()
    root.geometry(f"{int(width)}x{int(height)}+{int(x)}+{int(y)}")  # Cast values to integers
    root.attributes('-alpha', 0.5)  # Adjust transparency level
    canvas = tk.Canvas(root, width=width, height=height, bg="black")
    canvas.pack(fill="both", expand=True)
    return root, canvas

def take_screenshot(self,event):
         targetString = self.textentry.get()
         print("Searching on Screen: {}".format(targetString))
         im = grab(bbox=(0, 0, self.screen_width, self.screen_height))
         im.save('screenshot.png')
         # windows
         # pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
         # macos
         pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
         im = Image.open('screenshot.png')
         # imb = im.convert('1') # convert image to black and white
         # imb.save('bandw.png')
         textStrings = pytesseract.image_to_string(im)
         textZones = pytesseract.image_to_data(im, output_type=Output.DICT)
         # print(textZones)
         with open('ocr.txt', 'w') as file:
            file.write(textStrings)
         with open('ocrboxes.txt', 'w') as fp:
            fp.write('\n'.join('%s' % x for x in textZones))
         n_boxes = len(textZones['level'])
         count = 0
         for i in range(n_boxes):
            (x, y, w, h, confi, text) = (textZones['left'][i], textZones['top'][i], textZones['width'][i], textZones['height'][i], textZones['conf'][i], textZones['text'][i])
            print(text)
            if(-1!=int(confi)):
               if(text.find(targetString) != -1):
                  print("Here: {} {} {} {} {} {}".format(x,y,w,h,confi,text))
                  self.zonebox.append(self.canvas.create_rectangle( x,  y-50, x+w, y-50+h, fill="yellow"))
                  count = count + 1
         #self.root.attributes('-alpha', 1)
         self.canvas.update()
         print("Target {} found {} times.".format(targetString,count))

# Run on macOS
if __name__ == "__main__":
    main_screen, extended_screen = None, None
    screens = AppKit.NSScreen.screens()
    print(screens)

    for screen in screens:
        if screen.frame().origin == AppKit.NSScreen.mainScreen().frame().origin:
            main_screen = screen
            main_origin = screen.frame().origin
        else:
            extended_screen = screen
            break  # Only one extended screen expected
    main_resolution = main_screen.frame().size
    extended_resolution = extended_screen.frame().size

    print(f"Main screen resolution: {main_resolution}")
    print(f"Extended screen resolution: {extended_resolution}")
    roots = []

    # Create and position canvases on each monitor
    for screen_index, screen in enumerate(screens):
        frame = screen.frame()  # Get monitor bounds
        x, y, width, height = frame.origin.x, frame.origin.y, frame.size.width, frame.size.height
        if screen_index == 0 or extended_screen is None:  # Main monitor or single monitor case
        # Use frame for positioning and dimensions
            root, canvas = create_canvas(x, y, width, height)
        else:  # Extended monitor
        # Use extended_screen.frame() for positioning and dimensions
            if extended_screen.frame().origin.y < main_screen.frame().origin.y:
            # Extended monitor lower
                canvas_y = extended_screen.frame().origin.y

            else:
                # Extended monitor higher
                canvas_y = extended_screen.frame().origin.y - extended_screen.frame().size.height
            frame = extended_screen.frame()
            x, y, width, height = frame.origin.x, frame.origin.y, frame.size.width, frame.size.height
            root, canvas = create_canvas(x, canvas_y, width, height)
        roots.append(root)

    # Start Tkinter event loop for all windows
    for root in roots:
        root.mainloop()
