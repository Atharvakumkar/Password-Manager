from tkinter import *
from tkinter import messagebox

import customtkinter as ctk
import tkinter.font as ctkfont
from pymongo import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client.passwordManager
user_collection = db.userDetails

def login():
    userEmailCheck = loginEmailEntry.get()
    userPassCheck = loginPasswordEntry.get()

    loginDetailsCheck = db.userDetails.find_one({'email': userEmailCheck, 'pass': userPassCheck})
    
    if userEmailCheck == "" or userPassCheck == "":
        messagebox.showerror("Error", "Please enter all details!")
    elif loginDetailsCheck:
        messagebox.showinfo("Success", "Successfully logged in!")

ctk.set_appearance_mode("dark")

mainWindow = ctk.CTk()

my_font_heading = ctk.CTkFont(family="Rubik", size = 42, weight = "bold")
my_font_subheading = ctk.CTkFont(family="Rubik", size = 28)
my_font_label1 = ctk.CTkFont(family="Rubik", size = 25, weight = "bold")
my_font_label2 = ctk.CTkFont(family="Rubik", size = 22)
my_font_button = ctk.CTkFont(family="Rubik", size = 18)
mainWindow.title("Login Page")
mainWindow.geometry("1080x720")
mainWindow.resizable("false", "false")

mainFrame = ctk.CTkFrame(master = mainWindow,
                         height = 720,
                         width = 1080,
                         fg_color = "#FAF7F3",
                         bg_color = "#FAF7F3")
mainFrame.place(x = 0, y = 0)

heading = ctk.CTkLabel(master = mainFrame,
                       text = "Password Manager",
                       font = my_font_heading,
                       text_color = "#AF8260")
heading.place(x = 345, y = 30)

subHeading = ctk.CTkLabel(master = mainFrame,
                       text = "Manage all your passwords at one place!",
                       font = my_font_subheading,
                       text_color = "#AF8260")
subHeading.place(x = 270, y = 90)

subFrameLogin = ctk.CTkFrame(master = mainFrame,
                        height = 350,
                        width = 400,
                        fg_color = "#FFF2D7")
subFrameLogin.place(x = 330, y = 160)

loginText = ctk.CTkLabel(master = subFrameLogin,
                           text = "Login",
                           font = my_font_label1,
                           text_color = "#AF8260")
loginText.place(x = 170, y = 20)

loginEmailEntry = ctk.CTkEntry(master = subFrameLogin,
                          height = 50,
                          width = 360,
                          fg_color = "transparent",
                          border_width = 3,
                          border_color = "#AF8260",
                          placeholder_text = "Email",
                          placeholder_text_color = "#AF8260",
                          text_color = "#AF8260",
                          font = my_font_label2)
loginEmailEntry.place(x = 20, y = 70)

loginPasswordEntry = ctk.CTkEntry(master = subFrameLogin,
                          height = 50,
                          width = 360,
                          fg_color = "transparent",
                          border_width = 3,
                          border_color = "#AF8260",
                          placeholder_text = "Password",
                          placeholder_text_color = "#AF8260",
                          text_color = "#AF8260",
                          font = my_font_label2,
                         show = ".")
loginPasswordEntry.place(x = 20, y = 140)

loginSubmitButton = ctk.CTkButton(master = subFrameLogin,
                             height = 40,
                             width = 150,
                             text = "Submit",
                             font = my_font_button,
                             fg_color = "#AF8260",
                             text_color = "white",
                             hover_color = "#AF8320",
                             command = login)
loginSubmitButton.place(x = 120, y = 210)

loginButton = ctk.CTkButton(master = subFrameLogin,
                             height = 40,
                             width = 150,
                             text = "Already Signed Up? Login now",
                             font = my_font_button,
                             fg_color = "transparent",
                            text_color = "#AF8260",
                            hover_color = "white")
loginButton.place(x = 68, y = 280)


mainWindow.mainloop()