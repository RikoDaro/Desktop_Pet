import pyautogui
import random
import tkinter as tk
import sys
import threading
from PIL import Image, ImageSequence, ImageTk
from random import randint

INITIAL_Y = 940
window_height = 200

class spriteObject:    
    def __init__(self, x, y, initial_sprite):
        #fondmentali
        self.window = tk.Tk()
        self.event_number = 1
        self.x = x
        self.y = y
        #sprite
        self.sprite = initial_sprite
        self.cycle = 0
        self.halo_sprite = halo_void_sprite
        self.halo_cycle = 0
        self.halo_index = 0
        #movimento
        self.direction = -1
        self.destination = 0
        self.destination_reached = True
        self.walk_distance = 3
        #altri flag
        self.isFishing = False
        #self.has_halo = False

    def getFrame(self):
        frame = self.sprite.gif[self.cycle]

        if self.direction == -1:
            image = frame
        else:
            image = frame.transpose(Image.FLIP_LEFT_RIGHT)

        padded_image = Image.new("RGBA", (image.width, image.height + 50), (0, 0, 0, 0))
        padded_image.paste(image, (0, 50))

        y_position = window_height - image.height
        padded_image.paste(image, (0, y_position), image)

        self.tk_image = ImageTk.PhotoImage(image)
        return self.tk_image
    
    def isNextFrame(self):
        if self.cycle < len(self.sprite.gif):
            return True
        return False

class spriteGif:
    def __init__(self, gif, rate):
        self.gif = gif
        self.rate = rate
    
    def __str__(self):
        return f"oggetto spriteGif"

def loadGif(path):
    img = Image.open(path)
    frames = []

    for frame in ImageSequence.Iterator(img):
        frames.append(frame.convert('RGBA'))

    return frames

def pesca():
    pet.isFishing = True
    pet.destination_reached = True
    if random.choice([-1, 1]) > 0:
        if randint(0, 10) == 10:
            pet.sprite = fish_cought_legend_sprite
            #pet.has_halo = True
            pet.halo_index = 1
            '''
        elif randint(0, 10) == 10:
            #pet.sprite = fish_cought_dead_sprite
            #pet.has_halo = True
            pet.halo_index = 2
            '''
        else:
            pet.sprite = fish_cought_sprite
    else:
        pet.sprite = fish_not_cought_sprite
    pet.event_number = 17
    pet.cycle = 0

def getCombinedFrame(base_sprite, overlay_sprite, base_cycle, overlay_cycle, y_offset=-100):
    base_frame = base_sprite.gif[base_cycle]
    overlay_frame = overlay_sprite.gif[overlay_cycle]

    if pet.direction == 1:
        base_frame = base_frame.transpose(Image.FLIP_LEFT_RIGHT)

    window_height = 200
    combined = Image.new("RGBA", (base_frame.width, window_height), (0, 0, 0, 0))

    base_y = window_height - base_frame.height
    overlay_y = base_y + y_offset

    combined.paste(base_frame, (0, base_y), base_frame)
    combined.paste(overlay_frame, (0, overlay_y), overlay_frame)

    return ImageTk.PhotoImage(combined)

idle_num = [1, 2, 3, 4]
sleep_num = [5, 6, 7, 8]
walk_left_num = [9, 10]
walk_right_num = [11, 12]
idle_to_sleep_num = [13, 14]
sleep_to_idle_num = [15, 16]
fish_num = [17]

impath = 'C:\\Users\\riccardo.benetti\\Documents\\pet\\sprites\\'

idle = loadGif(impath + 'idle_duck.gif')[:4]
idle_sprite = spriteGif(idle, 150)

idle_to_sleep = loadGif(impath + 'idle_to_sleep_duck.gif')[:8]
idle_to_sleep_sprite = spriteGif(idle_to_sleep, 100)

sleep = loadGif(impath + 'sleep_duck.gif')[:12]
sleep_sprite = spriteGif(sleep, 300)

sleep_to_idle = loadGif(impath + 'sleep_to_idle_duck.gif')[:8]
sleep_to_idle_sprite = spriteGif(sleep_to_idle, 80)

walk_positive = loadGif(impath + 'walk_left_duck.gif')[:11]
walk_sprite = spriteGif(walk_positive, 70)

fall_left = loadGif(impath + 'fly_left_duck.gif')[:4]
fall_sprite = spriteGif(fall_left, 60)

fish_cought = loadGif(impath + 'fishing_cought_duck.gif')[:49]
fish_cought_sprite = spriteGif(fish_cought, 130)

fish_cought_legend = loadGif(impath + 'fishing_cought_legend_duck.gif')[:49]
fish_cought_legend_sprite = spriteGif(fish_cought_legend, 130)

fish_cought_dead = loadGif(impath + 'fishing_cought_dead_duck.gif')[:49]
fish_cought_dead_sprite = spriteGif(fish_cought_dead, 130)

fish_not_cought = loadGif(impath + 'fishing_not_cought_duck.gif')[:49]
fish_not_cought_sprite = spriteGif(fish_not_cought, 130)

halo_stars = loadGif(impath + 'halo_stars_duck.gif')[:4]
halo_stars_sprite = spriteGif(halo_stars, 60)

halo_soul = loadGif(impath + 'halo_soul_duck.gif')[:15]
halo_soul_sprite = spriteGif(halo_soul, 60)

halo_void = loadGif(impath + 'halo_void.gif')[:4]
halo_void_sprite = spriteGif(halo_void, 100)

placeholder = loadGif(impath + 'placeholder.gif')[:6]
placeholder_sprite = spriteGif(placeholder, 60)

def dragStart(event):
    global control

    widget = event.widget
    widget._dragStart_x = event.x_root - pet.window.winfo_x()
    widget._dragStart_y = event.y_root - pet.window.winfo_y()

    pet.event_number = 100
    control = 1
    pet.cycle = 0

def dragMotion(event):
    x = event.x_root - label._dragStart_x
    y = event.y_root - label._dragStart_y
    pet.x = x
    pet.y = y
    pet.window.geometry(f'+{x}+{y}')

def dragStop(event):
    def do_fall():
        global control
        if pet.y < INITIAL_Y:
            pet.y += 10  # fall speed
            pet.window.geometry(f'+{pet.x}+{pet.y}')
            pet.window.after(20, do_fall)
        else:
            pet.y = INITIAL_Y
            pet.event_number = 1
            pet.destination_reached = True
            control = 1
            pet.cycle = 0
    do_fall()

def terminal_command_listener():
    cmd_list = "Lista dei Comandi:\n\n\
aiuto: stampa la lista dei comandi\n\
dormi: Zzz\n\
centro: cammina fino al centro dello schermo\n\
cammina: cammina per sempre in una direzione casuale\n\
corri: corre per sempre in una direzione casuale\n\
pesca: speriamo di prendere qualcosa\n\
reset: pulisce ogni animazione sulla testa\n\
stop: termina ogni azione"
    print(cmd_list)
    while True:
        cmd = input("> ").strip().lower()

        if cmd == "test":
            print("comando eseguito")
        elif cmd == "dormi":
            if pet.event_number not in sleep_num:
                pet.destination_reached = True
                pet.sprite = idle_to_sleep_sprite
                pet.event_number = 101
                pet.cycle = 0
            print("Zzz")

        elif cmd == "centro":
            pet.destination_reached = False
            pet.walk_distance = 3
            pet.destination = pet.window.winfo_screenwidth()/2
            if pet.x < pet.destination:
                pet.event_number = 11
                pet.direction = 1
            else:
                pet.event_number = 9
                pet.direction = -1

            pet.sprite = walk_sprite
            pet.cycle = 0
            print("In marcia")

        elif cmd == "cammina":
            pet.destination_reached = False
            pet.walk_distance = 3
            pet.direction = random.choice([-1, 1])
            if pet.direction < 0:
                pet.destination = -9999
                pet.event_number = 9
                print("Cammino a sinistra")

            else:
                pet.destination = 9999
                pet.event_number = 11
                print("Cammino a destra")

            pet.sprite = walk_sprite
            pet.cycle = 0
        
        elif cmd == "corri":
            pet.destination_reached = False
            pet.walk_distance = 6
            pet.direction = random.choice([-1, 1])
            if pet.direction < 0:
                pet.destination = -9999
                pet.event_number = 9
                print("Corro a sinistra")

            else:
                pet.destination = 9999
                pet.event_number = 11
                print("Corro a destra")

            pet.sprite = walk_sprite
            pet.cycle = 0

        elif cmd == "pesca":
            if pet.event_number in sleep_num or pet.isFishing or pet.event_number == 101:
                print("Sshhh, non ora")
            else:
                print("Si va a pesca")
                pesca()

        elif cmd == "reset":
            pet.halo_sprite = halo_void_sprite
            #pet.has_halo = False
            pet.halo_index = 0

        elif cmd == "stop":
            if pet.event_number in sleep_num or pet.event_number == 101:
                pet.event_number = 15
                pet.sprite = sleep_to_idle_sprite
            else:
                pet.event_number = 1
                pet.sprite = idle_sprite

            pet.walk_distance = 3
            pet.destination_reached = True
            pet.cycle = 0

        elif cmd == "aiuto":
            print(cmd_list)

        else:
            print(f"Comando {cmd} non trovato")

control = 0
def refresh():
    global control
    
    if control == 0:
        combined_image = getCombinedFrame(pet.sprite, pet.halo_sprite, pet.cycle, pet.halo_cycle)
        label.configure(image=combined_image)
        label.image = combined_image

        pet.cycle += 1
        pet.halo_cycle += 1
        walk_sprite.rate = int(1.0/(float(pet.walk_distance))*210.0)

        if pet.event_number in walk_left_num:
            pet.x -= pet.walk_distance
            
            if pet.x <= pet.destination:
                pet.destination_reached = True

            if pet.x <= 0:
                pet.x = pet.window.winfo_screenwidth()-1

        elif pet.event_number in walk_right_num:
            pet.x += pet.walk_distance
            
            if pet.x >= pet.destination:
                pet.destination_reached = True
                
            if pet.x >= pet.window.winfo_screenwidth():
                pet.x = 1

        if not pet.isNextFrame():
            control = 1
            pet.cycle = 0
        if pet.halo_cycle >= len(pet.halo_sprite.gif):
            pet.halo_cycle = 0

    if control == 1:
        pet.isFishing = False
        
        #if pet.has_halo:
        if pet.halo_index == 0:
            pet.halo_sprite = halo_void_sprite
        elif pet.halo_index == 1:
            pet.halo_sprite = halo_stars_sprite
        elif pet.halo_index == 2:
            pet.halo_sprite = halo_soul_sprite
            
        if pet.event_number in idle_num:
            pet.event_number = random.choice(idle_num + idle_to_sleep_num + walk_left_num + walk_right_num + fish_num)

        elif pet.event_number in sleep_num:
            pet.event_number = random.choice(sleep_to_idle_num + sleep_num)

        elif pet.event_number in idle_to_sleep_num:
            pet.event_number = random.choice(sleep_num)

        elif pet.event_number in sleep_to_idle_num:
            pet.event_number = random.choice(idle_num)

        elif pet.event_number in walk_left_num and pet.destination_reached:
            pet.walk_distance = 3
            pet.event_number = random.choice(walk_left_num + walk_right_num + idle_num)

        elif pet.event_number in walk_right_num and pet.destination_reached:
            pet.walk_distance = 3
            pet.event_number = random.choice(walk_left_num + walk_right_num + idle_num)
        
        elif pet.event_number in fish_num:
            pet.event_number = 1
        
        control = 2

    if control == 2:
        if pet.event_number in idle_num:
            pet.sprite = idle_sprite

        elif pet.event_number in sleep_num:
            pet.sprite = sleep_sprite
        
        elif pet.event_number in idle_to_sleep_num:
            pet.sprite = idle_to_sleep_sprite

        elif pet.event_number in sleep_to_idle_num:
            pet.sprite = sleep_to_idle_sprite

        elif pet.event_number in walk_left_num:
            pet.sprite = walk_sprite
            pet.direction = -1

        elif pet.event_number in walk_right_num:
            pet.sprite = walk_sprite
            pet.direction = 1

        elif pet.event_number in fish_num:
            pesca()
        
        elif pet.event_number == 100:
            pet.sprite = fall_sprite
        
        elif pet.event_number == 101:
            pet.sprite = sleep_sprite

        control = 0
        
    pet.window.geometry(f'100x{window_height}+'+str(pet.x)+'+'+str(pet.y))
    pet.window.after(pet.sprite.rate, refresh)

pet = spriteObject(x = 1400, y = INITIAL_Y, initial_sprite = idle_sprite)

pet.window.config(highlightbackground='black')
pet.window.overrideredirect(True)
pet.window.wm_attributes('-transparentcolor','black')
pet.window.wm_attributes("-topmost", 1)

label = tk.Label(pet.window,bd=0,bg='black')

label.bind("<Button-1>", dragStart)
label.bind("<B1-Motion>", dragMotion)
label.bind("<ButtonRelease-1>", dragStop)
label.pack()

print("="*20+"\n    Desktop Pet\n"+"="*20)

threading.Thread(target=terminal_command_listener, daemon=True).start()

pet.window.after(1,refresh)
pet.window.mainloop()
