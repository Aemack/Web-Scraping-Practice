import praw
import random
import tkinter as tk

reddit = praw.Reddit(client_id='client_id', client_secret='client-secret', user_agent='WritingPrompter')

root = tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()


def get_prompt():
    hot_posts = reddit.subreddit('WritingPrompts').hot(limit=100)
    prompts = []
    for post in hot_posts:
        prompts.append(post.title)
    randNum = random.randint(0,99)
    prompt = prompts[randNum]
    prompt = prompt[4:len(prompt)]
    return prompt

def message():
    prompt = get_prompt()
    label1 = tk.Label(root, text = prompt, fg = 'green', font = ('helvetica', 10, 'bold'), wraplength = 250)
    canvas1.create_window(150, 200, window=label1)

button1 = tk.Button(root, text = 'Prompt Me!', command = message, bg = 'brown', fg = 'white' )
canvas1.create_window(150,20, window = button1)

root.mainloop()
