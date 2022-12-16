from PIL import Image, ImageTk
from tkinter import Label, StringVar, OptionMenu, Entry, GROOVE
import tkinter as tk
import cv2
import os
import numpy as np
from keras.models import model_from_json
import operator
import time
import sys, os
import matplotlib.pyplot as plt
import hunspell
from hunspell import Hunspell
from string import ascii_uppercase
from translate import Translator
from textToImage import switch_asl
from textToImageISL import switch_isl
 
class Main:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Sign language to Text Converter")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("925x900")
        self.panel = tk.Label(self.root)
        self.panel.place(x = 135, y = 10, width = 640, height = 640)
        self.panel2 = tk.Label(self.root) # initialize image panel
        self.panel2.place(x = 460, y = 95, width = 310, height = 310)
        
        tk.Entry(self.root, justify="center")
        
        self.T = tk.Label(self.root)
        self.T.place(x=31,y = 17, width=900, height=60)
        self.T.config(text = "Anuwaad",font=("Garamond",50,"bold", "italic"))
        self.panel3 = tk.Label(self.root, justify="center" )
        
        self.Tsub = tk.Label(self.root)
        self.Tsub.place(x=25,y = 80, width=900, height=60)
        self.Tsub.config(text = "Signs & Words, understand it all...",font=("Garamond",25, "italic"))
        self.panel4 = tk.Label(self.root, justify="center" )
        
        self.btasl = tk.Button(self.root,command = self.action_asl,height = 0,width = 0)
        self.btasl.config(text = "Recognise American Sign Language (ASL)",font = ("Cambria",15))
        self.btasl.place(x = 300, y = 200)
        
        self.btisl = tk.Button(self.root,command = self.action_isl,height = 0,width = 0, justify="center")
        self.btisl.config(text = "Recognise Indian Sign Language (ISL)",font = ("Cambria",15))
        self.btisl.place(x = 315, y = 300)
               
        self.btsplt = tk.Button(self.root,command = self.action_splt,height = 0,width = 0)
        self.btsplt.config(text = "Spoken Language Translate",font = ("Cambria",15))
        self.btsplt.place(x = 350, y = 400)
        
        self.bttiasl = tk.Button(self.root,command = self.action_tiasl,height = 0,width = 0)
        self.bttiasl.config(text = "Text to Image ASL",font = ("Cambria",15))
        self.bttiasl.place(x = 400, y = 500)
        
        self.bttiisl = tk.Button(self.root,command = self.action_tiisl,height = 0,width = 0)
        self.bttiisl.config(text = "Text to Image ISL",font = ("Cambria",15))
        self.bttiisl.place(x = 400, y = 600)
        
        self.btcall = tk.Button(self.root,command = self.action_call,height = 0,width = 0)
        self.btcall.config(text = "About",font = ("Cambria",15))
        self.btcall.place(x = 450, y = 700)
    
    # Function for 1) Recognise ASL
    def action_asl(self):
        self.directory = 'model'
        self.hs = hunspell.Hunspell('en_US')
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        
        self.json_file = open(self.directory+"//model-asl-bw.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(self.directory+"//model-asl-bw.h5")
        
        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        for i in ascii_uppercase:
          self.ct[i] = 0
        print("Loaded model from disk")
        self.root1 = tk.Toplevel(self.root)
        self.root1.title("American Sign language to Text Converter")
        self.root1.protocol('WM_DELETE_WINDOW', self.destructor1)
        self.root1.geometry("900x900")
        self.panel = tk.Label(self.root1)
        self.panel.place(x = 135, y = 10, width = 640, height = 640)
        self.panel2 = tk.Label(self.root1) # initialize image panel
        self.panel2.place(x = 460, y = 120, width = 310, height = 310)
        
        self.T = tk.Label(self.root1)
        self.T.place(x=31,y = 17)
        self.T.config(text = "American Sign Language to Text",font=("Cambria",40,"bold"))
        self.panel3 = tk.Label(self.root1) # Current SYmbol
        self.panel3.place(x = 500,y=660)
        self.T1 = tk.Label(self.root1)
        self.T1.place(x = 10,y = 660)
        self.T1.config(text="Character :",font=("Cambria",40,"bold"))
        
        self.bt1=tk.Button(self.root1, command=self.action1,height = 0,width = 0)
        self.bt1.place(x = 26,y=890)
        self.bt2=tk.Button(self.root1, command=self.action2,height = 0,width = 0)
        self.bt2.place(x = 325,y=890)
        self.bt3=tk.Button(self.root1, command=self.action3,height = 0,width = 0)
        self.bt3.place(x = 625,y=890)
        self.bt4=tk.Button(self.root1, command=self.action4,height = 0,width = 0)
        self.bt4.place(x = 125,y=950)
        self.bt5=tk.Button(self.root1, command=self.action5,height = 0,width = 0)
        self.bt5.place(x = 425,y=950)
        self.str=""
        self.word=""
        self.current_symbol="Empty"
        self.photo="Empty"
        self.video_loop()
    
    # Function for 2) Recognise ISL
    def action_isl(self):
        self.directory = 'model'
        self.hs = hunspell.Hunspell('en_US')
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        
        self.json_file = open(self.directory+"//model-bw.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(self.directory+"//model-bw.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        for i in ascii_uppercase:
          self.ct[i] = 0
        print("Loaded model from disk")
        self.root2 = tk.Toplevel(self.root)
        self.root2.title("Indian Sign language to Text Converter")
        self.root2.protocol('WM_DELETE_WINDOW', self.destructor2)
        self.root2.geometry("900x900")
        self.panel = tk.Label(self.root2)
        self.panel.place(x = 135, y = 10, width = 640, height = 640)
        self.panel2 = tk.Label(self.root2) # initialize image panel
        self.panel2.place(x = 460, y = 120, width = 310, height = 310)
        
        self.T = tk.Label(self.root2)
        self.T.place(x=31,y = 17)
        self.T.config(text = "Indian Sign Language to Text",font=("Cambria",40,"bold"))
        self.panel3 = tk.Label(self.root2) # Current SYmbol
        self.panel3.place(x = 500,y=660)
        self.T1 = tk.Label(self.root2)
        self.T1.place(x = 10,y = 660)
        self.T1.config(text="Character :",font=("Cambria",40,"bold"))
       
        self.bt1=tk.Button(self.root2, command=self.action1,height = 0,width = 0)
        self.bt1.place(x = 26,y=890)
        self.bt2=tk.Button(self.root2, command=self.action2,height = 0,width = 0)
        self.bt2.place(x = 325,y=890)
        self.bt3=tk.Button(self.root2, command=self.action3,height = 0,width = 0)
        self.bt3.place(x = 625,y=890)
        self.bt4=tk.Button(self.root2, command=self.action4,height = 0,width = 0)
        self.bt4.place(x = 125,y=950)
        self.bt5=tk.Button(self.root2, command=self.action5,height = 0,width = 0)
        self.bt5.place(x = 425,y=950)
        self.str=""
        self.word=""
        self.current_symbol="Empty"
        self.photo="Empty"
        self.video_loop()
    
    # Function for 3) Spoken Language Translation
    def action_splt(self):
         self.root3 = tk.Toplevel(self.root)
         self.root3.title("Spoken Language Translate")
         self.root3.protocol('WM_DELETE_WINDOW', self.destructor3)
         self.root3.geometry("900x900")
         print("###\t Multiple Spoken Language Translation \t###")
         InputLanguageChoice = StringVar()
         TranslateLanguageChoice = StringVar()
         LanguageChoices = {'Hindi','English','Kannada','Telugu','Marathi'}
         InputLanguageChoice.set('English')
         TranslateLanguageChoice.set('Hindi')
         
         self.T = tk.Label(self.root3)
         self.T.place(x=31,y = 17, width=900, height=40)
         self.T.config(text = "Anuwaad",font=("Garamond",30,"bold", "italic"))
         self.panel1 = tk.Label(self.root3, justify="center" )
         
         self.Tsub = tk.Label(self.root3)
         self.Tsub.place(x=25,y = 60, width=900, height=30)
         self.Tsub.config(text = "Signs & Words, understand it all...",font=("Garamond",15, "italic"))
         self.panel2 = tk.Label(self.root3, justify="center" )
         
         self.Tname = tk.Label(self.root3)
         self.Tname.place(x=25,y = 105, width=900, height=45)
         self.Tname.config(text = "Spoken Language Translation",font=("Garamond",20, "bold", "italic"))
         self.panel3 = tk.Label(self.root3, justify="center" )      
         
         self.sourceLang = tk.Label(self.root3,text="Source Language", font=("Cambria", 15,"underline"))
         self.sourceLang.place(x=190, y=175)
         self.InputLanguageChoiceMenu = tk.OptionMenu(self.root3,InputLanguageChoice,*LanguageChoices)
         self.InputLanguageChoiceMenu.place(x=230, y=210)
          
         #choice in which the language is to be translated
         self.targetLang = tk.Label(self.root3,text="Translated Language", font=("Cambria", 15, "underline"))
         self.targetLang.place(x=585, y=175)
         self.NewLanguageChoiceMenu = tk.OptionMenu(self.root3,TranslateLanguageChoice,*LanguageChoices)
         self.NewLanguageChoiceMenu.place(x=630, y=210)
         
         self.input = tk.Label(self.root3,text="Enter Text", font=("Cambria", 13))
         self.input.place(x=100, y=260)
         TextVar = StringVar()
         self.InputTextBox = tk.Entry(self.root3,textvariable=TextVar)
         self.InputTextBox.place(x=195,y=260, width=140, height=25)
          
         self.output = tk.Label(self.root3,text="Output Text", font=("Cambria", 13))
         self.output.place(x=500, y=260)
         OutputVar = StringVar()
         self.OutputTextBox = tk.Entry(self.root3,textvariable=OutputVar)
         self.OutputTextBox.place(x=600, y=260, width=140, height=25)
         
         self.bttr = tk.Button(self.root3, text="Translate",font=("Cambria", 15), command=lambda: self.Translate(InputLanguageChoice.get(),TranslateLanguageChoice.get(),TextVar.get(), OutputVar), relief = GROOVE)
         self.bttr.place(x=400, y=340)
         
    # Function for 4) Text to Sign ASL
    def action_tiasl(self):
        self.root4 = tk.Toplevel(self.root)
        self.root4.title("Text to Sign ASL")
        self.root4.protocol('WM_DELETE_WINDOW', self.destructor4)
        self.root4.geometry("900x900")
        
        self.T = tk.Label(self.root4)
        self.T.place(x=31,y = 17, width=900, height=40)
        self.T.config(text = "Anuwaad",font=("Garamond",30,"bold", "italic"))
        self.panel1 = tk.Label(self.root4, justify="center" )
        
        self.Tsub = tk.Label(self.root4)
        self.Tsub.place(x=25,y = 60, width=900, height=30)
        self.Tsub.config(text = "Signs & Words, understand it all...",font=("Garamond",15, "italic"))
        self.panel2 = tk.Label(self.root4, justify="center" )
        
        self.Tname = tk.Label(self.root4)
        self.Tname.place(x=25,y = 105, width=900, height=45)
        self.Tname.config(text = "Text to American Sign Language Translation",font=("Garamond",20, "bold", "italic"))
        self.panel3 = tk.Label(self.root4, justify="center" )
        
        self.InputLabel = tk.Label(self.root4,text="Enter Text",font=("Cambria", 13) )
        self.InputLabel.place(x=300, y=200)
        print("###\t Text to Signs Translation ASL \t###")
        TextVar = StringVar()
        self.InputTextBox = tk.Entry(self.root4,textvariable=TextVar)
        self.InputTextBox.place(x=400, y=200, height=25, width=250)
        
        self.bttiasl = tk.Button(self.root4,text="Translate", font=("Cambria", 15), command=lambda: self.TextToImage(TextVar,0), relief = GROOVE)
        self.bttiasl.place(x=400, y=300)
    
    # Function for 5) Text to Sign ISL
    def action_tiisl(self):
        self.root5 = tk.Toplevel(self.root)
        self.root5.title("Text to Sign ISL")
        self.root5.protocol('WM_DELETE_WINDOW', self.destructor5)
        self.root5.geometry("900x900")
                        
        self.T = tk.Label(self.root5)
        self.T.place(x=31,y = 17, width=900, height=40)
        self.T.config(text = "Anuwaad",font=("Garamond",30,"bold", "italic"))
        self.panel1 = tk.Label(self.root5, justify="center" )
        
        self.Tsub = tk.Label(self.root5)
        self.Tsub.place(x=25,y = 60, width=900, height=30)
        self.Tsub.config(text = "Signs & Words, understand it all...",font=("Garamond",15, "italic"))
        self.panel2 = tk.Label(self.root5, justify="center" )
        
        self.Tname = tk.Label(self.root5)
        self.Tname.place(x=25,y = 105, width=900, height=45)
        self.Tname.config(text = "Text to Indian Sign Language Translation",font=("Garamond",20, "bold", "italic"))
        self.panel3 = tk.Label(self.root5, justify="center" )
        
        self.InputLabel = tk.Label(self.root5,text="Enter Text",font=("Cambria", 13) )
        self.InputLabel.place(x=300, y=200)
        print("###\t Text to Signs Translation ISL \t###")
        TextVar = StringVar()
        self.InputTextBox = tk.Entry(self.root5,textvariable=TextVar)
        self.InputTextBox.place(x=400, y=200, height=25, width=250)
        
        self.bttiisl = tk.Button(self.root5,text="Translate", font=("Cambria", 15), command=lambda: self.TextToImage(TextVar,1), relief = GROOVE)
        self.bttiisl.place(x=400, y=300)
        
    # Function for 6) About  
    def action_call(self) :
        self.root6 = tk.Toplevel(self.root)
        self.root6.title("About")
        self.root6.protocol('WM_DELETE_WINDOW', self.destructor6)
        self.root6.geometry("900x900")
    
        self.tx = tk.Label(self.root6)
        self.tx.place(x = 330,y = 20)
        self.tx.config(text = "Project By", fg="red", font = ("Times",30,"bold"))
        
        self.tx = tk.Label(self.root6)
        self.tx.place(x = 150,y = 100)
        self.tx.config(text = "Sanjana N", fg="blue", font = ("Times",20,"italic"))
        
        self.tx = tk.Label(self.root6)
        self.tx.place(x = 550,y = 100)
        self.tx.config(text = "1RV19CS137", fg="green", font = ("Times",20,"italic"))
        
        self.tx = tk.Label(self.root6)
        self.tx.place(x = 150,y = 150)
        self.tx.config(text = "Sharayu Badiger", fg="blue", font = ("Times",20,"italic"))
        
        self.tx = tk.Label(self.root6)
        self.tx.place(x = 550,y = 150)
        self.tx.config(text = "1RV19CS145", fg="green", font = ("Times",20,"italic"))
    
    ### All the window destructor functions (0-6) ###
    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        
    def destructor1(self):
        print("Closing Recognition of ASL Application...\n")
        self.root1.destroy()
        
    def destructor2(self):
        print("Closing Recognition of iSL Application...\n")
        self.root2.destroy()
        
    def destructor3(self):
        print("Closing Spoken Language Translate Application...\n")
        self.root3.destroy()
    
    def destructor4(self):
        print("Closing Text to Sign ASL Application...\n")
        self.root4.destroy()
        
    def destructor5(self):
        print("Closing Text to Sign ISL Application...\n")
        self.root5.destroy()
    
    def destructor6(self):
        print("Closing About Application...")
        self.root6.destroy()
   
    ### Auxillary Functions ###
    
    # Aux function for sign text translation
    def video_loop(self):
        ok, frame = self.vs.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5*frame.shape[1])
            y1 = 10
            x2 = frame.shape[1]-10
            y2 = int(0.5*frame.shape[1])
            cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            cv2image = cv2image[y1:y2, x1:x2]
            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),2)
            th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            self.predict(res)
            self.current_image2 = Image.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.current_image2)
            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)
            self.panel3.config(text=self.current_symbol,font=("Cambria",50))
            self.panel4.config(text=self.word,font=("Cambria",40))
            
            predicts=self.hs.suggest(self.word)
            if(len(predicts) > 0):
                self.bt1.config(text=predicts[0],font = ("Cambria",20))
            else:
                self.bt1.config(text="")
            if(len(predicts) > 1):
                self.bt2.config(text=predicts[1],font = ("Cambria",20))
            else:
                self.bt2.config(text="")
            if(len(predicts) > 2):
                self.bt3.config(text=predicts[2],font = ("Cambria",20))
            else:
                self.bt3.config(text="")
            if(len(predicts) > 3):
                self.bt4.config(text=predicts[3],font = ("Cambria",20))
            else:
                self.bt4.config(text="")
            if(len(predicts) > 4):
                self.bt4.config(text=predicts[4],font = ("Cambria",20))
            else:
                self.bt4.config(text="")                
        self.root.after(30, self.video_loop)
        
    def predict(self,test_image):
        test_image = cv2.resize(test_image, (128,128))
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))
        prediction={}
        prediction['blank'] = result[0][0]
        inde = 0
        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1
        #LAYER 1
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]
        
        if(self.current_symbol == 'blank'):
            for i in ascii_uppercase:
                self.ct[i] = 0
        self.ct[self.current_symbol] += 1
        if(self.ct[self.current_symbol] > 60):
            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue
                tmp = self.ct[self.current_symbol] - self.ct[i]
                if tmp < 0:
                    tmp *= -1
                if tmp <= 20:
                    self.ct['blank'] = 0
                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return
            self.ct['blank'] = 0
            for i in ascii_uppercase:
                self.ct[i] = 0
            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1
                    if len(self.str) > 0:
                        self.str += " "
                    self.str += self.word
                    self.word = ""
            else:
                if(len(self.str) > 16):
                    self.str = ""
                self.blank_flag = 0
                self.word += self.current_symbol
   
    def action1(self):
    	predicts=self.hs.suggest(self.word)
    	if(len(predicts) > 0):
            self.word=""
            self.str+=" "
            self.str+=predicts[0]
    
    def action2(self):
    	predicts=self.hs.suggest(self.word)
    	if(len(predicts) > 1):
            self.word=""
            self.str+=" "
            self.str+=predicts[1]
    
    def action3(self):
    	predicts=self.hs.suggest(self.word)
    	if(len(predicts) > 2):
            self.word=""
            self.str+=" "
            self.str+=predicts[2]
    
    def action4(self):
    	predicts=self.hs.suggest(self.word)
    	if(len(predicts) > 3):
            self.word=""
            self.str+=" "
            self.str+=predicts[3]
    def action5(self):
    	predicts=self.hs.suggest(self.word)
    	if(len(predicts) > 4):
            self.word=""
            self.str+=" "
            self.str+=predicts[4]
                
    # Aux function for lang translation
    def Translate(ssd,fromlang, tolang, inputtext, outputtext):
        print("* "+ fromlang+" -> "+tolang)
        translator = Translator(from_lang=fromlang ,to_lang=tolang)
        Translation = translator.translate(inputtext)
        outputtext.set(Translation)
        print(inputtext+ " -> " +outputtext.get())
      
    # Aux function for text-image
    def TextToImage(ssd, TextVar, lang):
        sentence=TextVar.get()
        print("Word entered - "+ TextVar.get())
        sentence = sentence.upper()
        imgseq=[]
        letters=[]
        for i in sentence:
            if i.isalpha():
                letters.append(i)
                
        for i in letters:
            if(lang==0):
                img=switch_asl(i)
            if(lang==1):
                img=switch_isl(i)
            index=letters.index(i)
            if img=='nothing':
                continue
            imgseq.append(img)
        
        for i in imgseq:
            ind=imgseq.index(i)
            if ind==0:
                fimgpath=imgseq[0]
                fimg=cv2.imread(fimgpath)
            else:
                img=cv2.imread(i)
                fimg=np.concatenate((fimg, img), axis=1)
                
        cv2.imshow('OUTPUT',fimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

       
print("Starting Application...")
pba = Main()
pba.root.mainloop()
