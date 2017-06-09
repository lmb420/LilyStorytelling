from Tkinter import *
from PIL import Image, ImageTk

class GifLabel(Label):
    def __init__(self, master, filename):
        self.current_gif = self.getFrames(master, filename)
        self.count = 0
        self.idx = 0
        
        Label.__init__(self, master, image=self.current_gif[0])
        
        self.cancel = self.after(self.delay, self.play)
        
    def getFrames(self, master, filename):
        im = Image.open(filename)
        #resized = im.resize((width,height),Image.ANTIALIAS)
        seq = []
        try:
            while True:
                seq.append(im.copy())
                im.seek(len(seq))
                #resized = im.resize((width,height),Image.ANTIALIAS)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100
            
##        first = seq[0].convert('RGBA')
##        frames = [ImageTk.PhotoImage(first)]
##
##        temp = seq[0]
##        for image in seq[1:]:
##            temp.paste(image)
##            frame = temp.convert('RGBA')
##            frames.append(ImageTk.PhotoImage(frame))
        #scale image as large as possible within screen size limits
        im_w, im_h = im.size
        screen_w = master.winfo_screenwidth()
        screen_h = master.winfo_screenheight()
        scale_factor = min((screen_w/im_w), (screen_h/im_h))
        width = im_w * scale_factor
        height = im_h * scale_factor
        
        frames = []
        for frame in seq:
            frame = frame.resize((width,height),Image.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame.convert('RGB')))
        return frames
       
    def play(self):
        self.config(image=self.current_gif[self.idx])
        self.idx += 1
        if self.idx == len(self.current_gif):
            self.idx = 0
            self.count += 1
        self.cancel = self.after(self.delay, self.play)
        if self.count == 1:
            self.master.destroy()

def runGif(gif_name):
    root = Tk()
    photo = PhotoImage(file = "ZooGifs/zoobackground.pgm")
    backg = Label(root, image = photo)
    root.attributes("-topmost",1)
    root.geometry(str(root.winfo_screenwidth()) + "x" + str(root.winfo_screenheight()))
    anim = GifLabel(root, gif_name)
    backg.photo = photo
    backg.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    #anim.pack(padx = (root.winfo_screenwidth() - anim.current_gif[0].width())/2, pady = (root.winfo_screenheight() - anim.current_gif[0].height())/2)
    anim.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    root.mainloop()
