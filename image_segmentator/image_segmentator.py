# importing the tkinter module and PIL 
# that is pillow module 
from tkinter import *
from PIL import ImageTk, Image 
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import colorsys
import PIL
from threading import Thread
import cv2
import pathlib

DEFAULT_FONT = ('Helvetica', 14)

class InputDialog:
    def __init__(self, input_dir):
        self.dialog_window = Toplevel()
        
        self.input_dir = input_dir
        self.ok_clicked = False
        self.pattern_input = StringVar()
        self.start_input = IntVar()
        self.end_input = IntVar()
        self.images = []

        pattern_input_label = Label(master=self.dialog_window, text="Input filename pattern (e.g. \"image%%03d.png\")", font=DEFAULT_FONT)
        pattern_input_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        pattern_input_entry = Entry(master=self.dialog_window, width=20, textvariable=self.pattern_input, font=DEFAULT_FONT)
        pattern_input_entry.grid(row=0, column=1, padx=10, pady=1, sticky=W+E)

        start_input_label = Label(master=self.dialog_window, text="Input start frame number", font=DEFAULT_FONT)
        start_input_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        start_input_entry = Spinbox(master=self.dialog_window, from_=0, increment=1, width=20, textvariable=self.start_input, font=DEFAULT_FONT)
        start_input_entry.grid(row=1, column=1, padx=10, pady=1, sticky=W+E)

        end_input_label = Label(master=self.dialog_window, text="Input end frame number", font=DEFAULT_FONT)
        end_input_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        end_input_entry = Spinbox(master=self.dialog_window, from_=0, increment=1, width=20, textvariable=self.end_input, font=DEFAULT_FONT)
        end_input_entry.grid(row=2, column=1, padx=10, pady=1, sticky=W+E)

        button_frame = Frame(master=self.dialog_window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ok_button = Button(master=button_frame, text="OK", font=DEFAULT_FONT, command=self.on_ok_button)
        ok_button.grid(row=0, column=0)
        cancel_button = Button(master=button_frame, text="Cancel", font=DEFAULT_FONT, command=self.on_cancel_button)
        cancel_button.grid(row=0, column=1)
        
    def validate_input(self):
        self.images = []
        if self.start_input.get() > self.end_input.get():
            raise ValueError('Invalid interval: start frame must be less than or equal to end frame')
        for i in range(self.start_input.get(), self.end_input.get() + 1):
            file = self.input_dir / pathlib.Path(self.pattern_input.get() % i)
            if file.exists() and file.is_file():
                self.images.append(file)
            else:
                raise ValueError(f'Input file not found "{file}"')

    def get_input(self):
        return self.pattern_input.get(), self.start_input.get(), self.end_input.get(), self.images

    def was_ok_clicked(self):
        return self.ok_clicked

    def show(self):
        self.dialog_window.grab_set()
        self.dialog_window.wait_window()
    
    def on_ok_button(self):
        try:
            self.validate_input()
            self.ok_clicked = True   
            self.dialog_window.destroy()
        except ValueError as e:
            self.images = []
            messagebox.showerror(title="Error", message=e)
    
    def on_cancel_button(self):
        self.dialog_window.destroy()


def forward(img_no): 
    print(img_no)
    # GLobal variable so that we can have 
    # access and change the variable 
    # whenever needed 
    global image1 
    global image2
    global button_forward 
    global button_back 
    global List_images
    global root

    image1.grid_forget() 
    image2.grid_forget() 
    # This is for clearing the screen so that 
    # our next image can pop up 
    image1 = Label(image=List_images[img_no-1]) 
    image2 = Label(image=update_binary_image(0.1))

    # as the list starts from 0 so we are 
    # subtracting one 
    image1.grid(row=1, column=0, columnspan=3) 

    #image1.grid(row=1, column=0, sticky="w") 
    image2.grid(row=1, column=1, sticky="e") 
    image1.grid_columnconfigure(0, weight=1)
    image2.grid_columnconfigure(1, weight=1)

    button_forward.configure(command=lambda: forward(img_no+1))
  
    # img_no+1 as we want the next image to pop up 
    if img_no == 4:
        button_forward.configure(state=DISABLED) 
  
    # img_no-1 as we want previous image when we click 
    # back button 
    button_back.configure(command=lambda: back(img_no-1))
  
  
def back(img_no): 
    # We willl have global variable to access these 
    # variable and change whenever needed 
    global image 
    global button_forward 
    global button_back 
    global button_exit 
    image.grid_forget() 
  
    # for clearing the image for new image to pop up 
    image = Label(image=List_images[img_no - 1]) 
    image.grid(row=1, column=0, columnspan=3) 
    button_forward = Button(root, text="forward", 
                            command=lambda: forward(img_no + 1)) 
    button_back = Button(root, text="Back", 
                         command=lambda: back(img_no - 1)) 
    print(img_no) 
  
    # whenever the first image will be there we will 
    # have the back button disabled 
    if img_no == 1: 
        button_back = Button(root, Text="Back", state=DISABLED) 
  
    image.grid(row=1, column=0, columnspan=3) 
    button_back.grid(row=5, column=0) 
    button_exit.grid(row=5, column=1) 
    button_for.grid(row=5, column=2) 
  
#def segment_image(before_image):
def update_binary_image(image, threshold): 
    width, height = image.size
    data = np.array(image)
    for x in range(height):
        for y in range (width):
            r, g, b = data[x][y]
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            if s > threshold / 255.0:
                data[x][y] = (255, 255, 255)
            else:
                data[x][y] = (0, 0, 0)
    return ImageTk.PhotoImage(Image.fromarray(data))

def slider_command(val):
    global scale_widget
    global curr_index
    global threshold
    global tk_processed
    global processed_image_holder
    global loaded_images

    threshold = scale_widget.get()
    print(threshold / 255.0)

    if len(processed_image_holder) == 0:
        return
    processed_image_holder = []
    offset = 0
    while offset < 4 and curr_index + offset * 4 < len(loaded_images):
        processed_image_holder.append(update_binary_image(loaded_images[curr_index + offset * 4], threshold))
        tk_processed[offset].configure(text="", image=processed_image_holder[-1])
        offset += 1

def choose_input():
    global input_dir
    global pattern
    global start_frame
    global end_frame
    global images
    global image_holder
    global processed_image_holder

    input_dir_dialog = filedialog.askdirectory(title='choose input directory', mustexist=True)
    if input_dir_dialog != None:
        print(input_dir_dialog)
        input_dir = pathlib.Path(input_dir_dialog)
        input_dialog = InputDialog(input_dir)
        input_dialog.show()
        if input_dialog.was_ok_clicked():
            pattern, start_frame, end_frame, images = input_dialog.get_input()
            load_images()
            return
    input_dir = ""
    pattern = ""
    start_frame = 0
    end_frame = 0
    images = []
    image_holder = []
    processed_image_holder = []

def choose_output():
    pass

def load_images():
    global images
    global no_images_label
    global loaded_images

    global tk_images
    global tk_processed
    global tk_text

    global start_frame
    global end_frame
    global threshold

    global image_holder
    global processed_image_holder

    no_images_label.grid_forget()

    for i in range(len(tk_images)):
        tk_images[i].grid_forget()
    for i in range(len(tk_processed)):
        tk_processed[i].grid_forget()
    for i in range(len(tk_text)):
        tk_text[i].grid_forget()

    if len(images) == 0:
        no_images_label.grid(row=1, column=0, rowspan=3, columnspan=4, sticky="nsew")
        return

    loaded_images = []
    image_holder = []
    processed_image_holder = []

    tk_images = []
    tk_processed = []
    tk_text = []
    curr_index = 0

    for image in images:
        loaded_images.append(Image.open(image))

    tk_text.append(Label(text="No Image"))
    tk_text[-1].grid(row=0, column=0, columnspan=2)
    tk_images.append(Label(text="No Image"))
    tk_images[-1].grid(row=1, column=0)
    tk_processed.append(Label(text="No Image"))
    tk_processed[-1].grid(row=1, column=1)

    tk_text.append(Label(text="No Image"))
    tk_text[-1].grid(row=0, column=2, columnspan=2)
    tk_images.append(Label(text="No Image"))
    tk_images[-1].grid(row=1, column=2)
    tk_processed.append(Label(text="No Image"))
    tk_processed[-1].grid(row=1, column=3)

    tk_text.append(Label(text="No Image"))
    tk_text[-1].grid(row=2, column=0, columnspan=2)
    tk_images.append(Label(text="No Image"))
    tk_images[-1].grid(row=3, column=0)
    tk_processed.append(Label(text="No Image"))
    tk_processed[-1].grid(row=3, column=1)

    tk_text.append(Label(text="No Image"))
    tk_text[-1].grid(row=2, column=2, columnspan=2)
    tk_images.append(Label(text="No Image"))
    tk_images[-1].grid(row=3, column=2)
    tk_processed.append(Label(text="No Image"))
    tk_processed[-1].grid(row=3, column=3)

    offset = 0
    while offset < 4 and curr_index + offset * 4 < len(loaded_images):
        # weird hack; need to keep tk image in memory or image gets garbage collected and doesnt show up
        tk_text[offset].configure(text="Frame {}".format(start_frame + curr_index + offset * 4))
        image_holder.append(ImageTk.PhotoImage(loaded_images[curr_index + offset * 4]))
        tk_images[offset].configure(text="", image=image_holder[-1])
        processed_image_holder.append(update_binary_image(loaded_images[curr_index + offset * 4], threshold))
        tk_processed[offset].configure(text="", image=processed_image_holder[-1])
        offset += 1
    
#### INITIAL VIEW BEGINS -----------  
def initial_view():
    global button_forward
    global button_back
    global scale_widget
    global root
    global no_images_label

    global tk_images
    global tk_processed
    global tk_text
    global image_holder
    global processed_image_holder

    global curr_index
    global loaded_images
    global threshold
    global start_frame
    global end_frame

    # Window Setup 
    root = Tk() 
    root.title("Binarize Images") 
    root.geometry("1295x750")
    root.rowconfigure((0,1,2,3,4), weight=1)
    root.columnconfigure((0,1,2,3,4), weight=1)

    menu = Menu(root)
    root["menu"] = menu
    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label='file', menu=file_menu)
    file_menu.add_command(label='open images', command=choose_input)
    file_menu.add_command(label='save segmented images', command=choose_output)

    no_images_label = Label(master=root, text="Please Load Images")
    no_images_label.grid(row=1, column=0, rowspan=3, columnspan=4, sticky="nsew")

    tk_images = []
    tk_processed = []
    tk_text = []
    loaded_images = []
    image_holder = []
    processed_image_holder = []
    start_frame = 0
    end_frame = 0
    curr_index = 0
    
    #scale widget init
    scale_widget = Scale(root,label="Pick Threshold", orient="horizontal",length = 1295,  resolution=1, from_=0, to=254, tickinterval = 10, command=slider_command)
    threshold = 30
    scale_widget.set(threshold) 
    scale_widget.length = 1295 
    scale_widget.sliderlength = 1295 
    scale_widget.grid(row=4, column = 0, columnspan=4, sticky = "w")
    
    # We will have three button back ,forward and exit 
    button_back = Button(root, text="Back", command=back, state=DISABLED) 
    button_exit = Button(root, text="Exit", command=root.quit) 
    button_forward = Button(root, text="Forward", command=lambda: forward(1)) 
     
    # grid function is for placing the buttons in the frame 
    button_exit.grid(row=5, column=1,sticky = "w") 
    button_back.grid(row=5, column=1,sticky = "e") 
    button_forward.grid(row=5, column=2,sticky = "w")

    root.mainloop() 

if __name__ == '__main__':
    initial_view() 
