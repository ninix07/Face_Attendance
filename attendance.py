import tkinter as tk 
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import subprocess
import datetime

def button(window,text,color,command, fg='white'):
    button= tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg= fg,
        bg= color,
        command=command,
        height=2,
        width=20,
        font=('Helvetica bold',20)
    )
    return button

def img_label(window):
    label = tk.Label(window)
    label.grid(row=0,column=0)
    return label

def text_label(window,text):
    label = tk.Label(window, text= text)
    label.config(font=("sans-serif",21), justify= "left")
    return label

def entry_text(window):
    inputtxt= tk.Text(window,
            height=2,
            width= 15,
            font=("Arial",32))
    return inputtxt


class App:
    def __init__(self) :
        self.main_window= tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.login_button= button(self.main_window,'login','green', self.login)
        self.login_button.place(x=750,y=300)
        self.register_button= button(self.main_window,'Register new user','gray', self.register, fg='black')
        self.register_button.place(x=750,y=400)
        self.camera_window = img_label(self.main_window)
        self.camera_window.place(x=10,y=10,width=700,height= 500)

        self.add_webcam(self.camera_window)
        self.db_dir = './Data'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log_path = './log.csv'
      


    
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap= cv2.VideoCapture(0)
        
        self._label= label
        self.process_webcam()



    def process_webcam(self):
        ret,frame =self.cap.read()
        self.most_recent_capture_arr = frame
        img =cv2.cvtColor(self.most_recent_capture_arr,cv2.COLOR_BGR2RGB)
        self.recent_capture_pil=Image.fromarray(img)
        imgtk= ImageTk.PhotoImage(image= self.recent_capture_pil)
        self._label.imagtk = imgtk
        self._label.configure(image= imgtk)
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path='./.tmp.jpg'
        cv2.imwrite(unknown_img_path,self.most_recent_capture_arr)
        output= str(subprocess.check_output(['face_recognition', self.db_dir,unknown_img_path]))
        name=output.split(',')[1][:-3]
        os.remove(unknown_img_path)
        if name in ['unknown_person','no_persons_found']:
            messagebox.showerror("User Not Found", "Error! Please Register")
        else:
            messagebox.showinfo("Success","Attendance Successful!")
            with open (self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name,datetime.datetime.now() ))


        


    def register(self):
        self.register_window= tk.Toplevel(self.main_window)
        self.register_window.geometry("1200x520+370+120")
        self.accept_button = button(self.register_window,'Accept','green',self.accept_register)
        self.accept_button.place(x=750,y=300)
        self.try_again_button = button(self.register_window,'Try Again','red',self.try_again_register)
        self.try_again_button.place(x=750,y=400)
        self.camera_label= img_label(self.register_window)
        self.camera_label.place(x=10,y=10,width=700,height= 500)
        self.add_image(self.camera_label)
        self.text_label = text_label(self.register_window,"Input username:")
        self.text_label.place(x=720,y=70)
        self.text_entry = entry_text(self.register_window)
        self.text_entry.place(x=720,y=150)
       


    def add_image(self,label):
        
        imgtk= ImageTk.PhotoImage(image= self.recent_capture_pil)
        label.imagtk = imgtk
        label.configure(image= imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()


    def accept_register(self):

        name = self.text_entry.get(1.0,"end-1c")
        if name != '':
            cv2.imwrite(os.path.join(self.db_dir,'{}.jpg'.format(name)),self.register_new_user_capture)
            self.register_window.destroy()
            self.accept_window= tk.Toplevel(self.main_window)
            self.accept_window.geometry("600x520+350+100")
            self.text_label = text_label(self.accept_window,"Successfully Registered!")
            self.text_label.place(x=150,y=70)
            self.accept_button = button(self.accept_window,'Accept','green',self.try_again_accept)
            self.accept_button.place(x=150,y=120)
        else: 
            self.register_window.destroy()
            self.accept_window= tk.Toplevel(self.main_window)
            self.accept_window.geometry("600x520+350+100")
            self.text_label = text_label(self.accept_window,"Try Again!")
            self.text_label.place(x=120,y=70)
            self.try_again_button = button(self.accept_window,'Try Again','red',self.try_again_accept)
            self.try_again_button.place(x=120,y=120)



    def try_again_register(self):
        self.register_window.destroy()

    def try_again_accept(self):
        self.accept_window.destroy()
        
    def start(self):
        self.main_window.mainloop()


if __name__=='__main__':
    app=App()
    app.start()