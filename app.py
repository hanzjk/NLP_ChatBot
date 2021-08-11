from tkinter import *
from chat import get_responce, bot_name

import pyttsx3 as pp
import speech_recognition as s
import threading

engine=pp.init()
voices=engine.getProperty('voices')
print(voices)
engine.setProperty('voice',voices[1].id)

#To make chatbot speak
def speak(word):
    engine.say(word)
    engine.runAndWait()

# take query: it takes audio as input from user and convert it into string
def takeQuery():
    sr = s.Recognizer()
    sr.pause_threshold = 1
    print("Your Bot is listening")
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            app._insert_message(query,"You")

        except Exception as e:
            print(e)
            err_response="I didn’t get that. Can you repeat again ? "
            speak(err_response)
            print(err_response)
            msg_init = f"{bot_name}: {err_response}\n\n"
            app.text_widget.configure(state=NORMAL)
            app.text_widget.insert(END, msg_init)
            app.text_widget.configure(staCte=DISABLED)

            app.text_widget.see(END)

def repeat():
        while True:
            takeQuery()

#Set Font and Background properties
BG_GRAY="#ABB2B9"
BG_COLOR="#002244"
TEXT_COLOR="#EAECEE"

FONT="Helvetica 11"
FONT_BOLD="Helvetica 11 bold"

class ChatApplication:


    def __init__(self):
        self.window=Tk()
        self._setup_main_window()

    def run(self):
        t = threading.Thread(target=repeat)
        t.start()
        self.window.mainloop()


    def _setup_main_window(self):
        self.window.title("Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=550,height=600,bg=BG_COLOR)

        #head label
        head_label=Label(self.window,bg=BG_COLOR,fg=TEXT_COLOR,text="Welcome to ABCD Store",font=FONT_BOLD,pady=10)
        head_label.place(relwidth=1)

        #tiny divider
        line=Label(self.window,width=480,bg=BG_GRAY)
        line.place(relwidth=1,rely=0.07,relheight=0.012)

        #text widget
        self.text_widget=Text(self.window,width=20,height=2,bg=BG_COLOR,fg=TEXT_COLOR,font=FONT,padx=5,pady=5)
        self.text_widget.place(relheight=0.745,relwidth=1,rely=0.08)
        self.text_widget.configure(cursor="arrow",state=DISABLED)

        #scroll bar
        scrollbar=Scrollbar(self.text_widget)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        #bottom label
        bottom_label=Label(self.window,bg=BG_GRAY,height=80)
        bottom_label.place(relwidth=1,rely=0.825)

        #message entry box
        self.msg_entry=Entry(bottom_label,bg="#B9D9EB",fg="#002244",font=FONT)
        self.msg_entry.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self._on_enter_pressed)

        #send button
        send_button=Button(bottom_label,text="Send",font=FONT_BOLD,width=20,bg=BG_GRAY,  command=lambda:self._on_enter_pressed(None))
        send_button.place(relx=0.77,rely=0.008, relheight=0.06, relwidth=0.22)

        init_response="Hello!! I am Bot who can assist your grocery shopping."
        msg_init = f"{bot_name}: {init_response}\n\n"
        # speak(init_response)
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg_init)
        self.text_widget.configure(state=DISABLED)

        init_response_2 = "Please enter your list of items one by one to get the shelf number"
        msg_init_2 = f"{bot_name}: {init_response_2}\n\n"
        # speak(init_response_2)
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg_init_2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)



    def _on_enter_pressed(self,event): #To send message when pressed on enter key
        msg=self.msg_entry.get()
        self._insert_message(msg,"You")

    def _insert_message(self,msg,sender):
        if not msg:
            return

        self.msg_entry.delete(0,END)
        msg1=f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END,msg1)
        self.text_widget.configure(state=DISABLED)

        response=get_responce(msg)
        msg2 = f"{bot_name}: {response}\n\n"
        speak(response)
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__=="__main__":
    app=ChatApplication()
    app.run()