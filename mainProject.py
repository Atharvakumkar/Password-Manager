from tkinter import messagebox
import customtkinter as ctk
from pymongo import MongoClient
import hashlib

uri = "mongodb://localhost:27017"
client = MongoClient(uri)
db = client.passwordManager
user_collection = db.userDetails

ctk.set_appearance_mode("dark")

current_user = None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_home_window():

    def submit_password():
        app_name = app_name_entry.get().strip()
        app_email = app_email_entry.get().strip()
        app_pass = password_entry.get().strip()

        if not app_name or not app_email or not app_pass:
            messagebox.showerror("Error", "Please enter all details!")
            return

        try:
            result = user_collection.update_one(
                {'email': current_user},
                {
                    '$push': {
                        'apps': {
                            'appName': app_name,
                            'appEmail': app_email,
                            'appPassword': app_pass
                        }
                    }
                }
            )

            if result.modified_count == 1:
                messagebox.showinfo("Success", "Password added successfully!")
                # Clear the fields
                app_name_entry.delete(0, 'end')
                app_email_entry.delete(0, 'end')
                password_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Failed to save password.")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save password: {e}")

    def delete_password():
        app_name = app_name_del.get().strip()
        app_email = app_email_del.get().strip()

        if not app_name or not app_email:
            messagebox.showerror("Error", "Please enter app name and email!")
            return

        try:
            result = user_collection.update_one(
                {'email': current_user},
                {
                    '$pull': {
                        'apps': {
                            'appName': app_name,
                            'appEmail': app_email
                        }
                    }
                }
            )

            if result.modified_count == 1:
                messagebox.showinfo("Success", "Password deleted successfully!")
                app_name_del.delete(0, 'end')
                app_email_del.delete(0, 'end')
                password_del.delete(0, 'end')
            else:
                messagebox.showerror("Error", "App not found or failed to delete.")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete password: {e}")

    def view_passwords():
        try:
            user_data = user_collection.find_one({'email': current_user})
            if user_data and 'apps' in user_data:
                apps = user_data['apps']
                if apps:

                    view_window = ctk.CTkToplevel()
                    view_window.title("Saved Passwords")
                    view_window.geometry("800x600")
                    view_window.resizable(False, False)

                    scrollable_frame = ctk.CTkScrollableFrame(view_window, width=760, height=560)
                    scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

                    for i, app in enumerate(apps):
                        app_frame = ctk.CTkFrame(scrollable_frame, height=100, width=700)
                        app_frame.pack(pady=10, padx=10, fill="x")

                        ctk.CTkLabel(app_frame, text=f"App: {app['appName']}", font=("Arial", 14, "bold")).pack(
                            anchor="w", padx=10, pady=5)
                        ctk.CTkLabel(app_frame, text=f"Email: {app['appEmail']}", font=("Arial", 12)).pack(anchor="w",
                                                                                                           padx=10)
                        ctk.CTkLabel(app_frame, text=f"Password: {app['appPassword']}", font=("Arial", 12)).pack(
                            anchor="w", padx=10)
                else:
                    messagebox.showinfo("Info", "No saved passwords found.")
            else:
                messagebox.showinfo("Info", "No saved passwords found.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to retrieve passwords: {e}")

    home_window = ctk.CTk()
    home_window.title("Password Manager - Home")
    home_window.geometry("1080x720")
    home_window.resizable(False, False)

    my_font_heading = ctk.CTkFont(family="Rubik", size=42, weight="bold")
    my_font_subheading = ctk.CTkFont(family="Rubik", size=28)
    my_font_label1 = ctk.CTkFont(family="Rubik", size=25, weight="bold")
    my_font_label2 = ctk.CTkFont(family="Rubik", size=22)
    my_font_button = ctk.CTkFont(family="Rubik", size=18)

    main_frame = ctk.CTkFrame(master=home_window, height=720, width=1080, fg_color="#FAF7F3", bg_color="#FAF7F3")
    main_frame.place(x=0, y=0)

    heading = ctk.CTkLabel(master=main_frame, text="Password Manager", font=my_font_heading, text_color="#AF8260")
    heading.place(x=345, y=30)

    subheading = ctk.CTkLabel(master=main_frame, text="Manage all your passwords at one place!",
                              font=my_font_subheading, text_color="#AF8260")
    subheading.place(x=270, y=90)

    add_frame = ctk.CTkFrame(master=main_frame, height=350, width=430, fg_color="#FFF2D7")
    add_frame.place(x=80, y=150)

    ctk.CTkLabel(master=add_frame, text="Add Password", font=my_font_label1, text_color="#AF8260").place(x=30, y=20)

    app_name_entry = ctk.CTkEntry(master=add_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                  border_color="#AF8260", placeholder_text="Enter app name",
                                  placeholder_text_color="#AF8260",
                                  text_color="#AF8260", font=my_font_label2)
    app_name_entry.place(x=30, y=80)

    app_email_entry = ctk.CTkEntry(master=add_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                   border_color="#AF8260", placeholder_text="Enter email id",
                                   placeholder_text_color="#AF8260",
                                   text_color="#AF8260", font=my_font_label2)
    app_email_entry.place(x=30, y=150)

    password_entry = ctk.CTkEntry(master=add_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                  border_color="#AF8260", placeholder_text="Enter password",
                                  placeholder_text_color="#AF8260",
                                  text_color="#AF8260", font=my_font_label2, show=".")
    password_entry.place(x=30, y=220)

    submit_button = ctk.CTkButton(master=add_frame, height=40, width=150, text="Submit", font=my_font_button,
                                  fg_color="#AF8260", text_color="white", hover_color="#AF8320",
                                  command=submit_password)
    submit_button.place(x=30, y=290)

    delete_frame = ctk.CTkFrame(master=main_frame, height=350, width=430, fg_color="#FFF2D7")
    delete_frame.place(x=550, y=150)

    ctk.CTkLabel(master=delete_frame, text="Delete Password", font=my_font_label1, text_color="#AF8260").place(x=30,
                                                                                                               y=20)

    app_name_del = ctk.CTkEntry(master=delete_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                border_color="#AF8260", placeholder_text="Enter app name",
                                placeholder_text_color="#AF8260",
                                text_color="#AF8260", font=my_font_label2)
    app_name_del.place(x=30, y=80)

    app_email_del = ctk.CTkEntry(master=delete_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                 border_color="#AF8260", placeholder_text="Enter email id",
                                 placeholder_text_color="#AF8260",
                                 text_color="#AF8260", font=my_font_label2)
    app_email_del.place(x=30, y=150)

    password_del = ctk.CTkEntry(master=delete_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                border_color="#AF8260", placeholder_text="Enter password",
                                placeholder_text_color="#AF8260",
                                text_color="#AF8260", font=my_font_label2, show=".")
    password_del.place(x=30, y=220)

    delete_button = ctk.CTkButton(master=delete_frame, height=40, width=150, text="Delete", font=my_font_button,
                                  fg_color="#AF8260", text_color="white", hover_color="#AF8320",
                                  command=delete_password)
    delete_button.place(x=30, y=290)

    view_frame = ctk.CTkFrame(master=main_frame, height=180, width=900, fg_color="#FFF2D7")
    view_frame.place(x=80, y=520)

    ctk.CTkLabel(master=view_frame, text="View Passwords", font=my_font_label1, text_color="#AF8260").place(x=350, y=10)

    view_button = ctk.CTkButton(master=view_frame, height=40, width=150, text="View All", font=my_font_button,
                                fg_color="#AF8260", text_color="white", hover_color="#AF8320", command=view_passwords)
    view_button.place(x=375, y=60)

    logout_button = ctk.CTkButton(master=view_frame, height=40, width=150, text="Logout", font=my_font_button,
                                  fg_color="#AF8260", text_color="white", hover_color="#AF8320",
                                  command=lambda: (home_window.destroy(), main()))
    logout_button.place(x=375, y=110)

    return home_window


def login_window():

    def login():
        global current_user
        user_email = login_email_entry.get().strip()
        user_pass = login_password_entry.get().strip()

        if not user_email or not user_pass:
            messagebox.showerror("Error", "Please enter all details!")
            return

        hashed_pass = hash_password(user_pass)

        login_details = user_collection.find_one({'email': user_email, 'password': hashed_pass})

        if login_details:
            current_user = user_email
            messagebox.showinfo("Success", "Successfully logged in!")
            login_win.destroy()
            home_win = create_home_window()
            home_win.mainloop()
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password.")

    login_win = ctk.CTk()
    login_win.title("Login Page")
    login_win.geometry("1080x720")
    login_win.resizable(False, False)

    my_font_heading = ctk.CTkFont(family="Rubik", size=42, weight="bold")
    my_font_subheading = ctk.CTkFont(family="Rubik", size=28)
    my_font_label1 = ctk.CTkFont(family="Rubik", size=25, weight="bold")
    my_font_label2 = ctk.CTkFont(family="Rubik", size=22)
    my_font_button = ctk.CTkFont(family="Rubik", size=18)

    main_frame = ctk.CTkFrame(master=login_win, height=720, width=1080, fg_color="#FAF7F3", bg_color="#FAF7F3")
    main_frame.place(x=0, y=0)

    heading = ctk.CTkLabel(master=main_frame, text="Password Manager", font=my_font_heading, text_color="#AF8260")
    heading.place(x=345, y=30)

    subheading = ctk.CTkLabel(master=main_frame, text="Manage all your passwords at one place!",
                              font=my_font_subheading, text_color="#AF8260")
    subheading.place(x=270, y=90)

    login_frame = ctk.CTkFrame(master=main_frame, height=350, width=400, fg_color="#FFF2D7")
    login_frame.place(x=330, y=160)

    ctk.CTkLabel(master=login_frame, text="Login", font=my_font_label1, text_color="#AF8260").place(x=170, y=20)

    login_email_entry = ctk.CTkEntry(master=login_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                     border_color="#AF8260", placeholder_text="Email", placeholder_text_color="#AF8260",
                                     text_color="#AF8260", font=my_font_label2)
    login_email_entry.place(x=20, y=70)

    login_password_entry = ctk.CTkEntry(master=login_frame, height=50, width=360, fg_color="transparent",
                                        border_width=3,
                                        border_color="#AF8260", placeholder_text="Password",
                                        placeholder_text_color="#AF8260",
                                        text_color="#AF8260", font=my_font_label2, show=".")
    login_password_entry.place(x=20, y=140)

    login_button = ctk.CTkButton(master=login_frame, height=40, width=150, text="Login", font=my_font_button,
                                 fg_color="#AF8260", text_color="white", hover_color="#AF8320", command=login)
    login_button.place(x=125, y=210)

    back_button = ctk.CTkButton(master=login_frame, height=40, width=150, text="Back to Sign-Up", font=my_font_button,
                                fg_color="transparent", text_color="#AF8260", hover_color="white",
                                command=main)
    back_button.place(x=125, y=260)

    login_win.mainloop()


def sign_up():

    user_name = name_entry.get().strip()
    user_email = email_entry.get().strip()
    user_pass = password_entry.get().strip()
    user_pass_check = password_entry2.get().strip()

    if not user_name or not user_email or not user_pass or not user_pass_check:
        messagebox.showerror("Error", "Please fill all the details!")
        return

    if user_pass != user_pass_check:
        messagebox.showerror("Error", "Passwords don't match!")
        return

    if user_collection.find_one({'email': user_email}):
        messagebox.showerror("Error", "Email already registered!")
        return

    hashed_password = hash_password(user_pass)

    sign_up_details = {
        'name': user_name,
        'email': user_email,
        'password': hashed_password,
        'apps': []
    }

    try:
        user_collection.insert_one(sign_up_details)
        messagebox.showinfo("Success", "Account Created Successfully!")
        home2_win = login_window()
        home2_win.mainloop()

        # Clear the fields
        name_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        password_entry2.delete(0, 'end')

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to sign up: {e}")


def main():
    global name_entry, email_entry, password_entry, password_entry2

    main_window = ctk.CTk()
    main_window.title("Password Manager - Sign Up")
    main_window.geometry("1080x720")
    main_window.resizable(False, False)

    my_font_heading = ctk.CTkFont(family="Rubik", size=42, weight="bold")
    my_font_subheading = ctk.CTkFont(family="Rubik", size=28)
    my_font_label1 = ctk.CTkFont(family="Rubik", size=25, weight="bold")
    my_font_label2 = ctk.CTkFont(family="Rubik", size=22)
    my_font_button = ctk.CTkFont(family="Rubik", size=18)

    main_frame = ctk.CTkFrame(master=main_window, height=720, width=1080, fg_color="#FAF7F3", bg_color="#FAF7F3")
    main_frame.place(x=0, y=0)

    heading = ctk.CTkLabel(master=main_frame, text="Password Manager", font=my_font_heading, text_color="#AF8260")
    heading.place(x=345, y=30)

    subheading = ctk.CTkLabel(master=main_frame, text="Manage all your passwords at one place!",
                              font=my_font_subheading, text_color="#AF8260")
    subheading.place(x=270, y=90)

    signup_frame = ctk.CTkFrame(master=main_frame, height=500, width=400, fg_color="#FFF2D7")
    signup_frame.place(x=330, y=160)

    ctk.CTkLabel(master=signup_frame, text="Sign-Up", font=my_font_label1, text_color="#AF8260").place(x=140, y=20)

    name_entry = ctk.CTkEntry(master=signup_frame, height=50, width=360, fg_color="transparent", border_width=3,
                              border_color="#AF8260", placeholder_text="Name", placeholder_text_color="#AF8260",
                              text_color="#AF8260", font=my_font_label2)
    name_entry.place(x=20, y=70)

    email_entry = ctk.CTkEntry(master=signup_frame, height=50, width=360, fg_color="transparent", border_width=3,
                               border_color="#AF8260", placeholder_text="Email", placeholder_text_color="#AF8260",
                               text_color="#AF8260", font=my_font_label2)
    email_entry.place(x=20, y=140)

    password_entry = ctk.CTkEntry(master=signup_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                  border_color="#AF8260", placeholder_text="Password", placeholder_text_color="#AF8260",
                                  text_color="#AF8260", font=my_font_label2, show=".")
    password_entry.place(x=20, y=210)

    password_entry2 = ctk.CTkEntry(master=signup_frame, height=50, width=360, fg_color="transparent", border_width=3,
                                   border_color="#AF8260", placeholder_text="Confirm Password",
                                   placeholder_text_color="#AF8260",
                                   text_color="#AF8260", font=my_font_label2, show=".")
    password_entry2.place(x=20, y=280)

    signup_button = ctk.CTkButton(master=signup_frame, height=40, width=150, text="Sign Up", font=my_font_button,
                                  fg_color="#AF8260", text_color="white", hover_color="#AF8320", command=sign_up)
    signup_button.place(x=125, y=350)

    login_button = ctk.CTkButton(master=signup_frame, height=40, width=200, text="Already have an account? Login",
                                 font=my_font_button, fg_color="transparent", text_color="#AF8260",
                                 hover_color="white", command=login_window)
    login_button.place(x=60, y=410)

    main_window.mainloop()


if __name__ == "__main__":
    main()
