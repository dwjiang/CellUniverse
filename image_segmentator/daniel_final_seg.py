# importing the tkinter module and PIL 
# that is pillow module 
from tkinter import *
from PIL import ImageTk, Image 
from tkinter import messagebox, filedialog
import numpy as np
import colorsys
import PIL
from threading import Thread
import cv2
import skimage.color
import skimage.io
import skimage.viewer
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 
import pathlib

inited = 0
saturation = 0.1

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


def forward(): 
    # GLobal variable so that we can have 
    # access and change the variable 
    # whenever needed 
    global begin
    global end
    global image1 
    global image2 
    global image3 
    global image4 
    global image5 
    global image6 
    global image7 
    global image8 
    global scale_widget
    global button_forward 
    global button_back 
    global button_exit 
    global button_set
    global images

    begin += 12
    end += 12
    update_binary_image(begin, end, scale_widget.get())
    setup_images(begin, end)

    # This is for clearing the screen so that 
    # our next image can pop up 
    image1.grid_forget() 
    image2.grid_forget() 
    image3.grid_forget() 
    image4.grid_forget() 
    image5.grid_forget() 
    image6.grid_forget() 
    image7.grid_forget() 
    image8.grid_forget() 
    button_forward.grid_forget()
    button_back.grid_forget()
    draw_grid()

    # as the list starts from 0 so we are 
    # subtracting one 
  
    # img_no+1 as we want the next image to pop up 
    if end >= len(images) - 10: 
        button_forward = Button(root, text="Forward", command=forward, state=DISABLED) 
    else: 
        button_forward = Button(root, text="Forward", command=forward) 
    # img_no-1 as we want previous image when we click 
    # back button 
  
    button_back = Button(root, text="Back",command=back) 

    button_forward.grid(row=5, column=2,sticky = "w") 
    button_back.grid(row=5, column=1,sticky = "e") 

    # Placing the button in new grid 
    #button_back.grid(row=5, column=0) 
    #button_exit.grid(row=5, column=1) 
    #button_for.grid(row=5, column=2) 
  
def back(): 
    # We willl have global variable to access these 
    # variable and change whenever needed 
    global begin 
    global end
    global image1 
    global image2 
    global image3 
    global image4 
    global image5 
    global image6 
    global image7 
    global image8 
    global scale_widget
    global button_forward 
    global button_back 
    global button_exit 
    global button_set

    begin -= 12
    end -= 12

    update_binary_image(begin, end, scale_widget.get())
    setup_images(begin, end)

    # This is for clearing the screen so that 
    # our next image can pop up 
    image1.grid_forget() 
    image2.grid_forget() 
    image3.grid_forget() 
    image4.grid_forget() 
    image5.grid_forget() 
    image6.grid_forget() 
    image7.grid_forget() 
    image8.grid_forget() 
    button_forward.grid_forget()
    button_back.grid_forget()
    draw_grid()

    # back button disabled 
    if begin <= 10:
        button_back = Button(root, text="Back", state=DISABLED) 
    else:
        button_back = Button(root, text="Back", command=back) 
    button_forward = Button(root, text="Forward", command=forward) 

    button_forward.grid(row=5, column=2,sticky = "w") 
    button_back.grid(row=5, column=1,sticky = "e") 


  
#def segment_image(before_image):
def update_binary_image(begin,end,threshold): 
    global second_image
    global processed_images
    global images

    processed_images = []
    for i in range(begin,end+1,4):
        # Read image
        print("update_binary_image: i: ",i)
        src = cv2.imread(str(images[i].resolve()), cv2.IMREAD_GRAYSCALE)

        # Set threshold and maxValue
        thresh = threshold
        maxValue = 255 

        # Basic threshold example
        th, dst = cv2.threshold(src, thresh, maxValue, cv2.THRESH_BINARY_INV);      

        #plt.imshow(dst,'gray')
        im_pil = Image.fromarray(dst)
        second_image = ImageTk.PhotoImage(im_pil)
        processed_images.append(second_image)
    return second_image

def display_segmented_image(dum):
    print("Dum: ", dum)
    global scale_widget
    global s
    global image2
    global image4
    global image6
    global image8
    image2.grid_forget()
    image4.grid_forget()
    image6.grid_forget()
    image8.grid_forget()

    s = scale_widget.get()
    update_binary_image(begin, end, s)

    #assigning images
    image2 = Label(image=processed_images[0])
    image4 = Label(image=processed_images[1])
    image6 = Label(image=processed_images[2])
    image8 = Label(image=processed_images[3])
    
    #griding
    image2.grid(row=1, column=1)#, sticky="e") 
    image4.grid(row=1, column=3) 
    image6.grid(row=3, column=1) 
    image8.grid(row=3, column=3) 
    #image2.grid_columnconfigure(1, weight=1)
    #messagebox.showinfo("Message", "You have chosen value {}".format(scale_widget.get()))
 
def slider_thread(whatevs):
    thread = Thread(target=display_segmented_image)
    thread.start()
    return

def slider_command():
    #print("Dum: ", dum)
    #global scale_widget
    global s
    global image2
    image2.grid_forget()
    s = scale_widget.get()
    print("s: ",s)
    #s = float(dum)
    image2 = Label(image=update_binary_image(begin, end, s))
    image2.grid(row=1, column=1, sticky="e")
    image2.grid_columnconfigure(1, weight=1)

def setup_images(begin, end):
    global List_images
    global images

    List_images = [] 
    #Input Images
    #image_no_1 = ImageTk.PhotoImage(Image.open("0.png")) 

    for i in range(begin, end+1, 4):
        List_images.append(ImageTk.PhotoImage(Image.open(images[i])))

    print(List_images)

    # List of the images so that we traverse the list 
    #List_images = [image_no_1, image_no_2, image_no_3, image_no_4,image_no_5,image_no_6, image_no_7, image_no_8, image_no_9, image_no_10] 
   
def draw_grid():
    global image1
    global image2
    global image3
    global image4
    global image5
    global image6
    global image7
    global image8

    global q1_text
    global q2_text
    global q3_text
    global q4_text

    global begin_frame
    global end_frame

    if "image1" in globals():
        image1.grid_forget()
        image2.grid_forget()
        image3.grid_forget()
        image4.grid_forget()
        image5.grid_forget()
        image6.grid_forget()
        image7.grid_forget()
        image8.grid_forget()

    if "q1_text" in globals():
        q1_text.grid_forget()
        q2_text.grid_forget()
        q3_text.grid_forget()
        q4_text.grid_forget()

    im_phase = skimage.io.imread("0.png")
    hist_phase, bins_phase = skimage.exposure.histogram(im_phase)

    fig = plt.figure(figsize=(400,200)) 

    # Use matplotlib to make a pretty plot of histogram data
    fig, ax = plt.subplots(1, 1)
    
    ax.set_xlabel('pixel value')

    ax.set_ylabel('count')

    ratio = 0.001

    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()

    # the abs method is used to make sure that all numbers are positive
    # because x and y axis of an axes maybe inversed.
    #ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

    #ax.set_aspect('equal')
    #dispRatio = 0.5
    #ax.set_yscale('log')
    #ax.set(aspect=1.0/ax.get_data_ratio()*dispRatio, adjustable='box-forced')
    _ = ax.fill_between(bins_phase, hist_phase, alpha=0.75)


    graph = FigureCanvasTkAgg(fig) 
    image_graph= graph.get_tk_widget()
 

    #image_histo = Label(image=histogram) 
    #image_histo.grid(row=6, column=0)
    #Images
    image1 = Label(image=List_images[0]) 
    image2 = Label(image=processed_images[0]) 
    image3 = Label(image=List_images[1]) 
    image4 = Label(image=processed_images[1]) 
    
    image5 = Label(image=List_images[2]) 
    image6 = Label(image=processed_images[2]) 
    image7 = Label(image=List_images[3]) 
    image8 = Label(image=processed_images[3]) 

    #Texts
    q1_text = Label(root, text="Frame {}".format(begin_frame+begin+1))
    q2_text = Label(root, text="Frame {}".format(begin_frame+begin+4))
    q3_text = Label(root, text="Frame {}".format(begin_frame+begin+8))
    q4_text = Label(root, text="Frame {}".format(begin_frame+begin+12)) 

    #ROW 1
    image1.grid(row=1, column=0) 
    image2.grid(row=1, column=1) 
    image3.grid(row=1, column=2)
    image4.grid(row=1, column=3)
    q1_text.grid(row=0, column=0, columnspan=2) 
    q2_text.grid(row=0, column=2, columnspan=2) 

    #ROW 2 
    image5.grid(row=3, column=0)
    image6.grid(row=3, column=1)
    image7.grid(row=3, column=2)
    image8.grid(row=3, column=3)
    q3_text.grid(row=2, column=0, columnspan=2)
    q4_text.grid(row=2, column=2, columnspan=2)
    image_graph.grid(row=7,column=0,columnspan=6, rowspan=5, sticky="w") 
 

def choose_input():
    global input_dir
    global pattern
    global begin_frame
    global end_frame
    global images
    global scale_widget
    global button_forward

    global begin
    global end

    input_dir_dialog = filedialog.askdirectory(title='choose input directory', mustexist=True)
    if input_dir_dialog != None:
        print(input_dir_dialog)
        input_dir = pathlib.Path(input_dir_dialog)
        input_dialog = InputDialog(input_dir)
        input_dialog.show()
        if input_dialog.was_ok_clicked():
            pattern, begin_frame, end_frame, images = input_dialog.get_input()
            begin = 0
            end = 12

            button_forward.grid_forget()
            if end >= len(images): 
                button_forward = Button(root, text="Forward", command=forward, state=DISABLED) 
            else: 
                button_forward = Button(root, text="Forward", command=forward)
            button_forward.grid(row=5, column=2, sticky = "w")

            scale_widget.configure(command=display_segmented_image)
            setup_images(begin, end)
            update_binary_image(begin, end, scale_widget.get())
            draw_grid()
            display_segmented_image(scale_widget.get())


def choose_output():
    global scale_widget

    output_dir_dialog = filedialog.askdirectory(title='choose output directory', mustexist=True)
    if output_dir_dialog != None:
        print(output_dir_dialog)
        output_dir = pathlib.Path(output_dir_dialog)
        processed_images = []
        for i in range(len(images)):
            src = cv2.imread(str(images[i].resolve()), cv2.IMREAD_GRAYSCALE)
            thresh = scale_widget.get()
            maxValue = 255 

            th, dst = cv2.threshold(src, thresh, maxValue, cv2.THRESH_BINARY_INV);      

            im_pil = Image.fromarray(dst)
            im_pil.save(output_dir / images[i].name)


#### INITIAL VIEW BEGINS -----------  
def initial_view():
    global scale_widget
    global inited
    global begin
    global end
    global root
    global button_exit
    global button_back
    global button_forward
    global button_set

    # Window Setup 
    root = Tk() 
    root.title("Binarize Images") 
    root.geometry("1295x850") 

    menu = Menu(root)
    root["menu"] = menu
    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label='file', menu=file_menu)
    file_menu.add_command(label='open images', command=choose_input)
    file_menu.add_command(label='save segmented images', command=choose_output)

    global begin_frame
    global end_frame
    global images
    global pattern

    global List_images

    begin_frame = 0
    end_frame = 0
    images = []
    List_images = []
    pattern = ""

    begin = 0
    end = 12 

    # setup_images(begin,end)
    # update_binary_image(begin, end, 100) 
 
    # draw_grid() 

    #scale widget init
    scale_widget = Scale(root,label="Pick Threshold", orient="horizontal",length = 1295,  resolution=1, from_=0, to=254, tickinterval = 10)
    scale_widget.set(100)
    scale_widget.length = 1295 
    scale_widget.sliderlength = 1295 
    scale_widget.grid(row=4, column = 0, columnspan=4, sticky = "w")
    
    # We will have four button exit, back, forward, and save segmented images 
    button_back = Button(root, text="Back", command=back, state=DISABLED) 
    button_exit = Button(root, text="Exit", command=root.quit)
    button_forward = Button(root, text="Forward", command=forward) 
    button_set = Button(root, text="Segment Images", command=display_segmented_image)
     
    # grid function is for placing the buttons in the frame 
    button_exit.grid(row=5, column=1,sticky = "w") 
    button_back.grid(row=5, column=1,sticky = "e") 
    button_forward.grid(row=5, column=2,sticky = "w") 
    button_set.grid(row=5, column=2, sticky = "e")

    root.mainloop() 

if __name__ == '__main__':
    initial_view() 
