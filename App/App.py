import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import numpy as np

from Model import Model
from ImageGetter import ImageGetter

class Dummy_image_getter:
    def getImage(self):
        return np.asarray(Image.open("test_image.png")).astype(np.uint8)

class Dummy_model:

    def preprocessImage(self, image):
        print("preprocessing")
        return "features"

    def predict(self, features):
        print("predicting")
        return "prediction"

class GUI_Model_Interface:

    def __init__(self, image_getter, model):
        self.image_getter = image_getter
        self.model = model

    def setGUI(self, GUI):
        self.GUI = GUI

    def setImage(self, image):
        image_box = self.GUI.changeImage(image)

    def analyse(self, expose_time):
        print(expose_time)
        self.current_image = self.image_getter.getImage(float(expose_time))
        self.setImage(self.current_image)

        regression, classification = self.model.predict(self.current_image)
        result = "prediction: " + str(classification) + " estimation du RA: " + str(regression)
        self.GUI.result.config(text=result)

class App:
    def __init__(self, root, GMI):
        self.GMI = GMI
        #setting title
        root.title("ra analysis")
        #setting window size
        width=600
        height=350
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        options = ('100', '200', "300", "400", "500", "600")
        options_tk = tk.StringVar(value=options)

        listbox=tk.Listbox(root,listvariable=options_tk,height=len(options))
        listbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        listbox["font"] = ft
        listbox["fg"] = "#333333"
        listbox["justify"] = "center"
        listbox.place(x=50,y=40,width=230)

        self.listbox = listbox

        button=tk.Button(root)
        button["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        button["font"] = ft
        button["fg"] = "#000000"
        button["justify"] = "center"
        button["text"] = "Capture"
        button.place(x=50,y=130,width=230,height=50)
        button["command"] = self.button_command

        result=tk.Label(root)
        result["activebackground"] = "#cccccc"
        result["activeforeground"] = "#e6e6e6"
        ft = tkFont.Font(family='Times',size=10)
        result["font"] = ft
        result["fg"] = "#333333"
        result["text"] = "prediction"
        result["relief"] = "ridge"
        result["wraplength"] = 190
        result.place(x=50,y=200,width=230,height=110)

        self.result = result

        disp_img = tk.Label()
        disp_img.place(x=300,y=40)
        self.disp_img = disp_img



    def changeImage(self, image):
        image = Image.fromarray(image)
        resize_img = image.resize((270, 270))
        img = ImageTk.PhotoImage(resize_img)
        self.disp_img.config(image=img)
        self.disp_img.image = img

    def button_command(self):
    	if len(self.listbox.curselection()) != 0:
            expose_time = self.listbox.get(self.listbox.curselection()[0])
            self.GMI.analyse(expose_time)

if __name__ == "__main__":
    root = tk.Tk()

    #dig = Dummy_image_getter()
    #dm = Dummy_model()

    dig = ImageGetter()
    dm = Model()

    image = np.asarray(Image.open('test_image.png')).astype(np.uint8)

    GMI = GUI_Model_Interface(dig, dm)
    app = App(root, GMI)
    GMI.setGUI(app)
    GMI.setImage(image)

    root.mainloop()
