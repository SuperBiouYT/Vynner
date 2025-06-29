import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import webbrowser
import winsound  # Windows only for beep

DECRYPTION_KEY = "SuperBiouYT"
TIMER_DURATION = 24 * 60 * 60  # 24 hours in seconds
MAX_ATTEMPTS = 3

incorrect_attempts = 0
bsod_shown = False
bsod_window = None

def play_tick_sound():
    # Beep : freq 1000Hz, duration 100ms
    winsound.Beep(1000, 100)

def bsod_animation(label):
    while True:
        for i in range(4):
            if not label.winfo_exists():
                return
            play_tick_sound()
            label.config(text="Collecting error info" + "." * i)
            label.update()
            time.sleep(1)

def show_bsod():
    global bsod_shown, bsod_window
    if bsod_shown:
        return
    bsod_shown = True

    # Désactive l'interface ransomware
    entry.config(state='disabled')
    button_unlock.config(state='disabled')
    button_pay.config(state='disabled')
    timer_label.config(text="💥 YOUR FILES HAVE BEEN LOST.")

    bsod_window = tk.Toplevel()
    bsod_window.title("Blue Screen of Death")
    bsod_window.attributes("-fullscreen", True)
    bsod_window.configure(bg="#0000AA")  # Bleu BSOD
    bsod_window.focus_set()
    bsod_window.grab_set()
    bsod_window.protocol("WM_DELETE_WINDOW", lambda: None)  # disable close

    message = (
        ":(\n\n"
        "Your PC ran into a problem and needs to restart.\n"
        "We're just collecting some error info, and then we'll restart for you.\n\n"
        "If you want to know more, you can search online later for this error:\n"
        "STOP CODE: FAKE_RANSOMWARE_ERROR\n\n"
        "ALL YOUR FILES HAVE BEEN ENCRYPTED USING STRONG ENCRYPTION.\n"
        "PAY THE RANSOM TO RECOVER THEM.\n\n"
        "Please wait..."
    )

    label = tk.Label(bsod_window, text=message, fg="white", bg="#0000AA", font=("Consolas", 24, "bold"), justify="center")
    label.pack(expand=True)

    anim_label = tk.Label(bsod_window, text="Collecting error info...", fg="white", bg="#0000AA", font=("Consolas", 20))
    anim_label.pack(pady=20)

    threading.Thread(target=bsod_animation, args=(anim_label,), daemon=True).start()

    # Ferme tout après 30 secondes
    def close_all():
        time.sleep(30)
        bsod_window.destroy()
        root.destroy()
    threading.Thread(target=close_all, daemon=True).start()

def check_key():
    global incorrect_attempts
    if bsod_shown:
        return
    user_key = entry.get().strip()
    if user_key == DECRYPTION_KEY:
        messagebox.showinfo("UNLOCKED", "✔ CORRECT KEY. YOUR FILES HAVE BEEN RECOVERED!")
        root.destroy()
        if bsod_window:
            bsod_window.destroy()
    else:
        incorrect_attempts += 1
        if incorrect_attempts >= MAX_ATTEMPTS:
            show_bsod()
        else:
            messagebox.showerror("ERROR", f"❌ INCORRECT KEY. ATTEMPT {incorrect_attempts} / {MAX_ATTEMPTS}.")

def disable_close():
    pass  # Disable closing window

def update_timer():
    remaining = TIMER_DURATION
    while remaining >= 0 and not bsod_shown:
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        secs = remaining % 60
        timer_label.config(text=f"TIME LEFT TO PAY: {hrs:02d}:{mins:02d}:{secs:02d}")
        time.sleep(1)
        remaining -= 1
    if not bsod_shown:
        show_bsod()

def open_rickroll():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    webbrowser.open(url)

root = tk.Tk()
root.title("vynner")
root.attributes("-fullscreen", True)
root.configure(bg="#222222")
root.protocol("WM_DELETE_WINDOW", disable_close)

frame = tk.Frame(root, bg="#222222")
frame.pack(expand=True, fill="both", padx=60, pady=40)

title_label = tk.Label(
    frame,
    text="🔒 Oops, your files are encrypted 🔒",
    fg="#888888",
    bg="#222222",
    font=("Courier New", 28, "bold"),
    justify="center",
)
title_label.pack(pady=(0, 30))

message_text = (
    "Your documents, photos and important files have been encrypted with AES-256 and RSA-2048.\n\n"
    "To recover your files, pay a ransom.\n\n"
    "Send exactly 300 bitcoins to the wallet address:\n"
    "1A2b3C4d5E6f7G8h9I0jK1L2mN3oP4QrS\n\n"
    "After payment, enter the decryption key you receive below and click UNLOCK.\n\n"
    "If you fail to pay within 24 hours, your files will be lost forever.\n\n"
    "Do not turn off your computer or remove the software.\n\n"
    "For help, search online with STOP CODE: RANSOMWARE_FAKE_ERROR\n\n"
    "Good luck."
)

scroll_txt = scrolledtext.ScrolledText(frame, width=80, height=8, font=("Courier New", 14),
                                      bg="#111111", fg="#FFD700",
                                      insertbackground="#FFD700", relief="flat", wrap="word")
scroll_txt.insert("1.0", message_text)
scroll_txt.config(state='disabled')
scroll_txt.pack(pady=(0, 20), fill="both", expand=True)

timer_label = tk.Label(frame, text="", fg="#FFD700", bg="#222222", font=("Courier New", 22, "bold"))
timer_label.pack(pady=(0, 20))

key_label = tk.Label(frame, text="ENTER DECRYPTION KEY:", fg="#FFD700", bg="#222222",
                     font=("Courier New", 18, "bold"))
key_label.pack(pady=(0, 8))

entry = tk.Entry(frame, font=("Courier New", 22, "bold"), justify="center", bg="#111111", fg="#00FF00",
                 insertbackground="#00FF00", relief="flat", width=35)
entry.pack(pady=(0, 30), ipady=10)

buttons_frame = tk.Frame(frame, bg="#222222")
buttons_frame.pack()

button_unlock = tk.Button(buttons_frame, text="🔐 UNLOCK", command=check_key,
                          font=("Courier New", 24, "bold"), bg="#00FF00", fg="#FFD700",
                          activebackground="#00CC00", activeforeground="#FFFF00",
                          relief="flat", width=25, height=2, cursor="hand2")
button_unlock.grid(row=0, column=0, padx=25)

button_pay = tk.Button(buttons_frame, text="PAY", command=open_rickroll,
                       font=("Courier New", 24, "bold"), bg="#00FF00", fg="#FFD700",
                       activebackground="#00CC00", activeforeground="#FFFF00",
                       relief="flat", width=25, height=2, cursor="hand2")
button_pay.grid(row=0, column=1, padx=25)

threading.Thread(target=update_timer, daemon=True).start()

root.mainloop()
