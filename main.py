from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
random_entry = {}
to_learn = {}


# ---------------------------- Create Flashcards ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- Add Card to Learned Words ------------------------------- #
def word_to_learn():
    to_learn.remove(random_entry)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    new_card()


# ---------------------------- New Card ------------------------------- #
def new_card():
    global random_entry, timer
    window.after_cancel(timer)
    random_entry = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_entry["French"], fill="black")
    canvas.itemconfig(canvas_image, image=flashcard_front)
    timer = window.after(5000, flip_card)


# ---------------------------- Flip Card ------------------------------- #
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_entry["English"], fill="white")
    canvas.itemconfig(canvas_image, image=flashcard_back)


# ---------------------------- UI Setup ------------------------------- #

# --- Window --- #
window = Tk()
window.title("Flashcard Exercise")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# window.eval("tk::PlaceWindow . center")
timer = window.after(5000, flip_card)


# --- Flashcard Canvas --- #
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
flashcard_front = PhotoImage(file="./images/card_front.png")
flashcard_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flashcard_front)
card_title = canvas.create_text(400, 150, text="text", font=("Arial", 35, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# --- Buttons --- #
x_image = PhotoImage(file="./images/wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=new_card)
x_button.grid(column=0, row=1)

check_image = PhotoImage(file="./images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=word_to_learn)
check_button.grid(column=1, row=1)


# --- New Card --- #
new_card()


# --- Loop --- #
window.mainloop()
