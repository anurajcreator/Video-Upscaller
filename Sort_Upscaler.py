try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

import ui_support
from tkinter import filedialog

import cv2

from cv2 import dnn_superres


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    ui_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    ui_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("506x614+664+159")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1, 1)
        top.title("Video Upscaller")
        top.iconbitmap("icon\icon.ico")

        top.configure(background="#4f566a")
        self.intial = "C:\\"
        self.o_direct = "C:\\"
        self.flag = 0
        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.04, rely=0.049, height=31, width=194)
        self.Label1.configure(activebackground="#f0f0f0f0f0f0")
        self.Label1.configure(background="#4f566a")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Roboto} -size 12")
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(text='''//Choose Video File ...''')

        self.Button1 = tk.Button(top, command=self.get_video)
        self.Button1.place(relx=0.751, rely=0.114, height=34, width=77)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#7b8ece")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="-family {Roboto} -size 10")
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Browse''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.079, rely=0.114, height=31, width=324)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(cursor="fleur")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(justify='left')
        self.Label2.configure(text='''Path''')

        self.Button2 = tk.Button(top, command=self.upscaler)
        self.Button2.place(relx=0.079, rely=0.896, height=44, width=427)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#7b8ece")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font="-family {Roboto} -size 11 -weight bold")
        self.Button2.configure(foreground="#ffffff")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''START''')

        self.output_text = tk.Label(top)
        self.output_text.place(relx=0.059, rely=0.228, height=30, width=224)
        self.output_text.configure(activebackground="#f0f0f0f0f0f0")
        self.output_text.configure(activeforeground="black")
        self.output_text.configure(background="#4f566a")
        self.output_text.configure(disabledforeground="#a3a3a3")
        self.output_text.configure(font="-family {Roboto} -size 12")
        self.output_text.configure(foreground="#ffffff")
        self.output_text.configure(highlightbackground="#d9d9d9")
        self.output_text.configure(highlightcolor="black")
        self.output_text.configure(text='''//Choose  Output Directory...''')

        self.o_path = tk.Label(top)
        self.o_path.place(relx=0.079, rely=0.309, height=30, width=324)
        self.o_path.configure(activebackground="#f9f9f9")
        self.o_path.configure(activeforeground="black")
        self.o_path.configure(background="#d9d9d9")
        self.o_path.configure(disabledforeground="#a3a3a3")
        self.o_path.configure(foreground="#000000")
        self.o_path.configure(highlightbackground="#d9d9d9")
        self.o_path.configure(highlightcolor="black")
        self.o_path.configure(justify='left')
        self.o_path.configure(text='''Path''')

        self.o_browse = tk.Button(top, command=self.get_out_dir)
        self.o_browse.place(relx=0.751, rely=0.309, height=34, width=77)
        self.o_browse.configure(activebackground="#ececec")
        self.o_browse.configure(activeforeground="#000000")
        self.o_browse.configure(background="#7b8ece")
        self.o_browse.configure(disabledforeground="#a3a3a3")
        self.o_browse.configure(font="-family {Roboto} -size 10")
        self.o_browse.configure(foreground="#ffffff")
        self.o_browse.configure(highlightbackground="#d9d9d9")
        self.o_browse.configure(highlightcolor="black")
        self.o_browse.configure(pady="0")
        self.o_browse.configure(text='''Browse''')

        self.seq_progress = ttk.Progressbar(top)


        self.text_image_seq = tk.Label(top)
        self.text_image_seq.place(relx=0.059, rely=0.44, height=30, width=224)
        self.text_image_seq.configure(activebackground="#f0f0f0f0f0f0")
        self.text_image_seq.configure(activeforeground="black")
        self.text_image_seq.configure(background="#4f566a")
        self.text_image_seq.configure(cursor="fleur")
        self.text_image_seq.configure(disabledforeground="#a3a3a3")
        self.text_image_seq.configure(font="-family {Roboto} -size 12")
        self.text_image_seq.configure(foreground="#ffffff")
        self.text_image_seq.configure(highlightbackground="#d9d9d9")
        self.text_image_seq.configure(highlightcolor="black")


        self.text_image_seq_2 = tk.Label(top)
        self.text_image_seq_2.place(relx=0.277, rely=0.717, height=30, width=224)

        self.text_image_seq_2.configure(activebackground="#f0f0f0f0f0f0")
        self.text_image_seq_2.configure(activeforeground="black")
        self.text_image_seq_2.configure(background="#4f566a")
        self.text_image_seq_2.configure(disabledforeground="#a3a3a3")
        self.text_image_seq_2.configure(font="-family {Roboto} -size 12")
        self.text_image_seq_2.configure(foreground="#ffffff")
        self.text_image_seq_2.configure(highlightbackground="#d9d9d9")
        self.text_image_seq_2.configure(highlightcolor="black")


    def get_video(self):

        self.filename = filedialog.askopenfilename(initialdir=self.intial, title="Selecfile",
                                                   filetypes=(("video", "*.mp4"), ("all files", " *.*")))
        if self.filename == "":
            self.Label2.configure(text="No Video Detected")
        else:
            print(self.filename)
            self.intial = self.filename
            self.Label2.configure(text=self.filename)
            self.vid = cv2.VideoCapture(self.filename)
            self.T_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
            print(self.T_frames)

    def get_out_dir(self):
        self.o_direct = filedialog.askdirectory(initialdir=self.intial, title="Select Directory")

        if self.o_direct == "":
            self.o_path.configure(text="Choose a Valid Directory")
        else:
            self.o_path.configure(text=self.o_direct)
            self.intial = self.o_direct

    def upscaler(self):
        try:
            self.vid = cv2.VideoCapture(self.filename)
            self.text_image_seq.configure(text='Upscaling Video', anchor='w')

            self.seq_progress.place(relx=0.099, rely=0.505, relwidth=0.791
                                    , relheight=0.0, height=22)
            self.seq_progress.configure(length="400")

            self.pvalue = 100 / self.T_frames
            self.text_image_seq_2.configure(text='''''')
            root.update_idletasks()


            imgs = []
            sr = dnn_superres.DnnSuperResImpl_create()
            path = "datamodel\\ESPCN_x2.pb"
            sr.readModel(path)
            sr.setModel("espcn", 2)
            for i in range(1, self.T_frames + 1):
                ret, frame = self.vid.read()
                upimg = sr.upsample(frame)
                height, width, layers = upimg.shape
                size = (width, height)
                imgs.append(upimg)
                self.seq_progress['value'] += self.pvalue
                root.update_idletasks()
                root.update()

            self.text_image_seq_2.configure(text='''----Upscalling Done----''')
            self.seq_progress['value'] = 0
            print("Exporting Video....")
            self.text_image_seq.configure(text='Exporting Video....', anchor='w')
            root.update_idletasks()

            output = cv2.VideoWriter(str(self.o_direct) + '\\output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, size)

            for i in range(self.T_frames):
                # print(i)
                output.write(imgs[i])
                self.seq_progress['value'] += self.pvalue
                root.update_idletasks()
                root.update()

            self.text_image_seq_2.configure(text='''----Video Exported----''')
            print("Video Exported.")


        except:
            self.text_image_seq_2.configure(text='''----Provide a valid Video File----''')
            self.text_image_seq.configure(text='', anchor='w')
            root.update_idletasks()

if __name__ == '__main__':
    vp_start_gui()
