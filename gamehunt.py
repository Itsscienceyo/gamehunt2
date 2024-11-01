from tkinter import *
from tkinter import scrolledtext
import requests
from PIL import Image, ImageTk
from io import BytesIO
import random 
from tkinter import messagebox
import sqlite3
from responses import responseses


screen=Tk()
screen.geometry("300x300+600+200")
screen.title("GameHunt")
screen.config(bg="#060917")
screen.resizable(FALSE,FALSE)

game_images = {}
current_page = 1  

print("hello")
conn = sqlite3.connect('gamehunt_users.db')
c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXTL,
    password TEXT
)
''')

conn.commit()
conn.close()


def signin():
    global gmailentry, paswordentryy, signinnn
    signinnn=Toplevel()
    signinnn.geometry("300x300+500+200")
    signinnn.config(bg="#060917")

    gmail=Label(signinnn,text="Enter your Username:",width=20,bg="#060917",fg="white",font="Ariel 12 bold")
    gmail.place(x=50,y=50)

    gmailentry=Entry(signinnn,width=30,border=3)
    gmailentry.place(x=60,y=90)

    password=Label(signinnn,text="Enter your Password:",width=20,bg="#060917",fg="white",font="Ariel 12 bold")
    password.place(x=50,y=140)

    paswordentryy=Entry(signinnn,width=30,border=3, show='*')
    paswordentryy.place(x=60,y=170)


    submitButton=Button(signinnn,text="Sign in",width=20,bg="#474747",fg="white",font="Ariel 10 bold",border=3,command=validate_signin)
    submitButton.place(x=70,y=210)

user_email = None

current_user_email = None
current_user_password = None

def validate_signin():
    global current_user_email, current_user_password,user_email
    email = gmailentry.get()
    password = paswordentryy.get()

    if email and password:
        try:
            conn = sqlite3.connect('gamehunt_users.db')
            c = conn.cursor()

            # Query to find the user with the entered email and password
            c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = c.fetchone()

            if user:
                messagebox.showinfo("Success", "Sign in successful!")
                current_user_email = email
                current_user_password = password  # Store the password in the global variable
                signinnn.destroy()
                mainscreen()
            else:
                messagebox.showerror("Error", "Invalid email or password.")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please fill in all fields!")




def add_to_favorites():
    game_name = favorite_entry.get().strip()
    if not game_name:
        messagebox.showerror("Error", "Please enter a game name.")
        return

    if not current_user_email:
        messagebox.showerror("Error", "You need to be signed in to add favorites.")
        return

    try:
        conn = sqlite3.connect('gamehunt_users.db')
        c = conn.cursor()
        
        # Create the favorites table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_name TEXT NOT NULL,
                user_email TEXT NOT NULL
            )
        ''')
        
        # Insert the game_name and the current user's email into the favorites table
        c.execute('INSERT INTO favorites (game_name, user_email) VALUES (?, ?)', (game_name, current_user_email))
        conn.commit()

        messagebox.showinfo("Success", f"'{game_name}' has been added to your favorites!")
        favorite_entry.delete(0, END)  # Clear the entry after adding

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"'{game_name}' is already in your favorites.")

    finally:
        conn.close()


def view_favorites():
    global current_user_email, favorites

    if not current_user_email:
        messagebox.showerror("Error", "You need to be signed in to view your favorites.")
        return

    try:
        conn = sqlite3.connect('gamehunt_users.db')
        c = conn.cursor()

        # Retrieve only the favorite games for the current user
        c.execute('SELECT game_name FROM favorites WHERE user_email = ?', (current_user_email,))
        favorites = c.fetchall()

        if favorites:
            favorites_list = "\n".join([game[0] for game in favorites])
            messagebox.showinfo("Your Favorites", favorites_list)
        else:
            messagebox.showinfo("Your Favorites", "You have no favorite games yet.")

    finally:
        conn.close()

def signup():
    global gmailentryy, paswordentry, signuplev
    signuplev=Toplevel()
    signuplev.geometry("300x300+500+200")
    signuplev.config(bg="#060917")

    gmaill=Label(signuplev,text="Enter your username:",width=20,bg="#060917",fg="white",font="Ariel 12 bold")
    gmaill.place(x=50,y=50)

    gmailentryy=Entry(signuplev,width=30,border=3)
    gmailentryy.place(x=60,y=90)

    passwordd=Label(signuplev,text="Choose a Password:",width=20,bg="#060917",fg="white",font="Ariel 12 bold")
    passwordd.place(x=50,y=140)

    paswordentry=Entry(signuplev,width=30,border=3, show='*')
    paswordentry.place(x=60,y=170)


    submitButtonn=Button(signuplev,text="Sign up",width=20,bg="#474747",fg="white",font="Ariel 10 bold",border=3,command=save_user_to_db)
    submitButtonn.place(x=70,y=210)

def save_user_to_db():
    global current_user_email, current_user_password,user_email
    email = gmailentryy.get()
    password = paswordentry.get()

    if email and password:
        try:
            conn = sqlite3.connect('gamehunt_users.db')
            c = conn.cursor()
            
            # Insert new user into the database
            c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()

            # Store email and password in global variables
            current_user_email = email
            current_user_password = password

            messagebox.showinfo("Success", "Sign up successful!")
            print(email, password)

            # Close the signup window and open the main screen
            signuplev.destroy()
            mainscreen()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "This email is already registered!")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Please fill in all fields!")

favorite_entry=None
def mainscreen():
    mainscreen=Toplevel()
    mainscreen.geometry("600x600+300+100")
    mainscreen.resizable(FALSE,FALSE)
    mainscreen.config(bg="#060917")



    navbar=Frame(mainscreen,width=600,height=60,bg="#393f4d")
    navbar.place(x=0,y=0)

    title=Label(mainscreen,text="GameHunt",fg="#58C525",bg="#393f4d",font="Ariel 20 bold")
    title.place(x=220,y=15)

    view_favorites_button = Button(
        mainscreen,
        text="View Favorites",
        border=2,
        font="Ariel 7 bold",
        bg="#46cf15",
        fg="black",
        command=view_favorites  # This will now work because view_favorites is defined
    )
    view_favorites_button.place(x=440, y=145)
    global favorite_entry

    favorite_entry = Entry(mainscreen, width=27, border=2)
    favorite_entry.place(x=350, y=115)


    add_favorite_button = Button(
        mainscreen,
        text="Add to Favorites",
        border=2,
        font="Ariel 7 bold",
        bg="#46cf15",
        fg="black",
        command=add_to_favorites
    )
    add_favorite_button.place(x=350, y=145)

    chat=Button(mainscreen,text="Chat",border=2,font="Ariel 10 bold",bg="#46cf15",fg="black",command=chatt)
    chat.place(x=20,y=80)

    profil=Button(mainscreen,text="Profil",border=2,font="Ariel 10 bold",bg="#46cf15",fg="black",command=profia)
    profil.place(x=140,y=120)

    aboutme=Button(mainscreen,text="About us",border=2,font="Ariel 10 italic bold",bg="#46cf15",fg="black",command=aboutse)
    aboutme.place(x=200,y=120)






    global current_page  # Use the global variable for current_page
    current_page = 1  # Reset to page 1 when mainscreen is opened

    API_KEY = '3837df8a8d474474a573f9c26b3e3f2e'

    def fetch_games(api_key, search_query='', page=1):
        url = 'https://api.rawg.io/api/games'
        params = {
            'key': api_key,
            'page_size': 5,  # Number of games per page
            'search': search_query,
            'page': page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['results']
    
    def fetch_game_details(api_key, game_id):
        url = f'https://api.rawg.io/api/games/{game_id}'
        params = {
            'key': api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def suggest_random_game():
        games = fetch_games(API_KEY)
        if not games:
            messagebox.showinfo("No Games Found", "No games available for suggestion.")
            return

        random_game = random.choice(games)  # Choose a random game
        game_details = fetch_game_details(API_KEY, random_game['id'])
        name = game_details['name']
        description = game_details.get('description_raw', 'No description available')
        image_url = game_details.get('background_image')

        if image_url:
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                img_data = response.content
                image = Image.open(BytesIO(img_data))
                
                image.thumbnail((300, 300)) 
                img = ImageTk.PhotoImage(image)

             
                game_window = Toplevel()
                game_window.title(f"Random Game Suggestion - {name}")
                game_window.geometry("400x500+600+200")
                game_window.config(bg="#060917")

          
                img_label = Label(game_window, image=img, bg="#060917")
                img_label.image = img 
                img_label.pack(pady=10)

           
                name_label = Label(game_window, text=name, font="Ariel 14 bold", fg="white", bg="#060917")
                name_label.pack(pady=5)

                description_label = Label(game_window, text=description, wraplength=350, justify=LEFT, fg="white", bg="#060917")
                description_label.pack(pady=10)

            except requests.RequestException as e:
                messagebox.showerror("Error", f"Failed to fetch image: {e}")
        else:
            messagebox.showinfo("No Image Available", "No image available for this game.")

            
    def display_games():
        global current_page
        search_query = search_var.get()
        games = fetch_games(API_KEY, search_query, current_page)
        text_area.delete(1.0, END)  
        for game in games:
            game_id = game['id']
            game_details = fetch_game_details(API_KEY, game_id)
            name = game_details['name']
            description = game_details.get('description_raw', 'No description available')

            image_url = game_details.get('background_image')
            if image_url:
                try:
                    if image_url not in game_images:  
                        response = requests.get(image_url)
                        response.raise_for_status()
                        img_data = response.content
                        image = Image.open(BytesIO(img_data))
                        image.thumbnail((300, 300))  
                        game_images[image_url] = ImageTk.PhotoImage(image)

                    img_label = Label(text_area, image=game_images[image_url], bg="#111224")
                    text_area.window_create(END, window=img_label)

                except requests.RequestException as e:
                    print(f"Failed to fetch image: {e}")

            text_area.insert(END, f"Name: {name}\n", 'name')
            text_area.insert(END, f"Description: {description}\n", 'description')
            text_area.insert(END, f"{'-'*50}\n", '-')




    def next_page():
        global current_page
        current_page += 1
        display_games()

    def previous_page():
        global current_page
        if current_page > 1:
            current_page -= 1
            display_games()

    search_frame = Frame(mainscreen)
    search_frame.pack(pady=80)

    search_var = StringVar()
    search_bar = Entry(search_frame, textvariable=search_var, width=56, border=2)
    search_bar.pack(side=LEFT, padx=5)

    search_button = Button(search_frame, text="Search Games", border=2, font="Ariel 8 bold", bg="#46cf15", fg="black", command=display_games)
    search_button.pack(side=LEFT, padx=0)

    suggest_game = Button(mainscreen, text="Random Game", border=2, font="Ariel 10 bold", bg="#46cf15", fg="black", command=suggest_random_game)
    suggest_game.place(x=20, y=120)

    frame = Frame(mainscreen)
    frame.pack(fill=BOTH, expand=True)
    frame.config(bg="#060917")

    text_area = scrolledtext.ScrolledText(frame, wrap=WORD, bg="#111224")
    text_area.pack(fill=BOTH, expand=True)

    text_area.tag_configure('name', foreground='white', font="Ariel 10 bold")
    text_area.tag_configure('description', foreground="white")
    text_area.tag_configure('-', foreground="white")

    nav_frame = Frame(mainscreen, bg="#060917")
    nav_frame.pack(pady=0)

    prev_button = Button(nav_frame, text="Previous",font="Ariel 15 bold",border=0,bg="#46cf15", fg="black", command=previous_page, state=DISABLED)
    prev_button.pack(side=LEFT, padx=5)

    next_button = Button(nav_frame, text="Next",font="Ariel 15 bold",width=8,border=0,bg="#46cf15", fg="black", command=next_page)
    next_button.pack(side=LEFT, padx=5)

    def update_nav_buttons():
        prev_button.config(state=NORMAL if current_page > 1 else DISABLED)

    def display_games():
        global current_page
        search_query = search_var.get()
        games = fetch_games(API_KEY, search_query, current_page)
        text_area.delete(1.0, END)
        for game in games:
            game_id = game['id']
            game_details = fetch_game_details(API_KEY, game_id)
            name = game_details['name']
            description = game_details.get('description_raw', 'No description available')

            image_url = game_details.get('background_image')
            if image_url:
                try:
                    if image_url not in game_images:
                        response = requests.get(image_url)
                        response.raise_for_status()
                        img_data = response.content
                        image = Image.open(BytesIO(img_data))
                        image.thumbnail((300, 300))
                        game_images[image_url] = ImageTk.PhotoImage(image)

                    img_label = Label(text_area, image=game_images[image_url], bg="#111224")
                    text_area.window_create(END, window=img_label)

                except requests.RequestException as e:
                    print(f"Failed to fetch image: {e}")

            text_area.insert(END, f"Name: {name}\n", 'name')
            text_area.insert(END, f"Description: {description}\n", 'description')
            text_area.insert(END, f"{'-'*50}\n", '-')

        update_nav_buttons()

def profia():
    global current_user_email,current_user_password
    profil_screen=Toplevel()
    profil_screen.geometry("500x300")
    profil_screen.title("Profil")
    profil_screen.resizable(FALSE,FALSE)
    profil_screen.config(bg="#060917")

  


    user_name=Label(profil_screen,text=f"User:  {current_user_email}",fg="#58C525",bg="#060917",font="Ariel 15 bold")
    user_name.place(x=10,y=10)

    user_password=Label(profil_screen,text=f"password:  {current_user_password}",fg="#58C525",bg="#060917",font="Ariel 15 bold")
    user_password.place(x=10,y=50)


    saved_games=Label(profil_screen,text="saved games:",fg="#58C525",bg="#060917",font="Ariel 15 bold")
    saved_games.place(x=10,y=90)

    saved_games_viev=Text(profil_screen,width=40,height=10,bg="#393f4d")
    saved_games_viev.place(x=10,y=130)

    try:
        
        conn = sqlite3.connect('gamehunt_users.db')
        c = conn.cursor()

        
        c.execute('SELECT game_name FROM favorites WHERE user_email = ?', (current_user_email,))
        favorites = c.fetchall()

        if favorites:
            for game in favorites:
                saved_games_viev.insert(END, game[0] +"\n") 
        else:
            saved_games_viev.insert(END, "No saved games yet.")

    finally:
        conn.close()


    saved_games_viev.config(state=DISABLED)



def aboutse():
        aboutke=Toplevel()
        aboutke.geometry("550x470")
        aboutke.resizable(FALSE,FALSE)
        aboutke.config(bg="#393f4d")

        me=Label(aboutke,text="Welcome to Gamehunt, your ultimate tool for discovering new and exciting games!\n"
            "Whether you're looking for something specific or want a random recommendation,\n"
            "Gamehunt is designed to help you find the perfect game for your next adventure.\n\n"
            "With Gamehunt, you can:\n\n"
            "- Search for Games: Easily find your favorite games by name or browse\n"
            "through our extensive library of titles. Whether you're in the mood for\n"
            "a classic or something new, we’ve got you covered!\n\n"
            "- Get Random Suggestions: Not sure what to play? Let us suggest a game\n"
            "based on your preferences, or discover something completely unexpected!\n\n"
            "- Save Games for Later: Found a game you're excited about? Save it to your list,\n"
            "so you can play whenever you're ready.\n\n"
            "- Chat with Our Game Bot: Unsure where to start or want to chat about games?\n"
            "Our friendly bot is here to assist you with recommendations and more.\n\n"
            "At Gamehunt, we believe finding the right game should be easy, fun, and\n"
            "personalized. Whether you're a casual player or a dedicated gamer,\n"
            "we're here to help you explore the gaming world and find your next\n"
            "favorite experience.\n\n"
            "Happy gaming!",fg="#58C525",bg="#393f4d",font="Ariel 10 bold")
        me.pack()



def chatt():
    chatscreen = Toplevel()
    chatscreen.geometry("320x250+600+200")
    chatscreen.resizable(FALSE,FALSE)
    chatscreen.title("Chat")
    chatscreen.config(bg="#393f4d")

    def gönder():
        user_message = inputt.get().strip()
        if user_message:
            chata.insert(END, "You: " + user_message + "\n")
            respond(user_message)
            inputt.delete(0, END)

    def gettextt(response):
        chata.insert(END, "Bot: " + response + "\n")

    def respond(user_message):
        print(f"User message: {user_message}")  
        
      
        bot_response = responseses.get(user_message, "Sorry, I don't understand that. Make sure to type properly and in full form!")
        
        print(f"Bot response: {bot_response}")  
        gettextt(bot_response)



    inputt = Entry(chatscreen, width=20)
    inputt.place(x=10, y=210)

    send = Button(chatscreen, text="Send", border=2, bg="#46cf15", fg="black", font="Ariel 10 bold", command=gönder)
    send.place(x=150, y=210)

    frame = Frame(chatscreen)
    frame.place(x=10, y=10)

    chata = Text(frame, width=35, height=12, bg="white")
    chata.pack(side=LEFT, fill=BOTH)

    scrollbar = Scrollbar(frame, command=chata.yview)
    scrollbar.pack(side=RIGHT, fill=X)

    chata.config(yscrollcommand=scrollbar.set) 



navbar=Frame(screen,width=300,height=40,bg="#393f4d")
navbar.place(x=0,y=0)

title=Label(screen,text="GameHunt",fg="#58C525",bg="#393f4d",font="Ariel 10 bold ")
title.place(x=110,y=10)

signinn=Button(screen,text="Sign in",width=20,bg="#46cf15",fg="black",font="Ariel 10 bold",command=signin)
signinn.place(x=65,y=110)

login=Button(screen,text="Sign up",width=20,bg="#46cf15",fg="black",font="Ariel 10 bold",border=3,command=signup)
login.place(x=65,y=150)







screen.mainloop()