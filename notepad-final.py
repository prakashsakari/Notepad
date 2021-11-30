from tkinter import *
from tkinter import font, filedialog, messagebox, ttk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Creating screen screen
screen = Tk()
screen.title('Untitled - Prakash\'s Notepad')
screen.geometry('650x520')  # width = 800 and height = 600

# Loading screen icon
screen_icon = PhotoImage(file='images/notes.png')
screen.iconphoto(True, screen_icon)

# Creating text area
text_area = Text(screen, font=('Courier New', 16),
                 undo=True, bg='#FFFFFF', fg='#1e1e1e')
text_area.config(wrap='word', relief=FLAT)


file_name = ''


def new(event=None):
    screen.title('Untitled - Prakash\'s Notepad')
    text_area.delete(1.0, END)


def open_func(event=None):
    global file_name

    file_name = filedialog.askopenfilename(defaultextension='.txt',
                                           filetypes=[
                                               ('Text Documents', '*.txt'),
                                               ('Python Files', '*.py'),
                                               ('All Files', '*.*')
                                           ])
    # checking if no file is selected
    if file_name == '':
        file_name = ''
    else:
        screen.title(file_name + ' - Prakash\'s Notepad')
        text_area.delete(1.0, END)
        file = open(file_name, mode='r')
        data = file.read()
        text_area.insert(1.0, data)
        file.close()


def save(event=None):
    global file_name
    if file_name == '':
        file_name = filedialog.asksaveasfilename(defaultextension='.txt',
                                                 filetype=[
                                                     ('Text Documents', '*.txt'),
                                                     ('All Files', '*.*')
                                                 ])

        # checking if no file is selected
        if file_name == '':
            file_name = ''
        else:
            file = open(file=file_name, mode='w')
            data = text_area.get(1.0, END)
            file.write(data)
            file.close()
            screen.title(file_name + ' - Prakash\'s Notepad')
    else:
        file = open(file=file_name, mode='w')
        data = text_area.get(1.0, END)
        file.write(data)
        file.close()


def save_as(event=None):
    global file_name
    file_name = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=[
                                                 ('Text Documents', '*.txt'),
                                                 ('All Files', '*.*')
                                             ])
    if file_name == '':
        file_name = ''
    else:
        file = open(file=file_name, mode='w')
        data = text_area.get(1.0, END)
        file.write(data)
        file.close()
        screen.title(file_name + ' - Prakash\'s Notepad')


text = False


def wordin_textarea(event=None):
    global text
    if text_area.edit_modified():
        text = True


def close(event=None):
    global file_name, text

    data = text_area.get(1.0, END)
    # print('Type of data in text area =', type(data))
    # print('Data in text area =', data)

    # Checking if text area is modified
    if text == True and not data.isspace():
        box = messagebox.askyesnocancel('Prakash\'s Notepad',
                                        'Do you want to save this file?')

        # checking if the user clicked Yes button
        if box == True:
            if file_name == '':
                save_as()  # calling function to save the new file
                screen.destroy()  # close the window
            else:
                data = text_area.get(1.0, END)
                file = open(file=file_name, mode='w')
                file.write(data)
                file.close()
                screen.destroy()
        # checking if the user clicked No button
        elif box == False:
            screen.destroy()

    # checking if text area is not modified
    else:
        screen.destroy()


def cut():
    text_area.event_generate('<<Cut>>')


def copy():
    text_area.event_generate('<<Copy>>')


def paste():
    text_area.event_generate('<<Paste>>')


def clear_all(event=None):
    text_area.delete(1.0, END)


def find_replace(event=None):
    def find():
        word = find_entry_field.get()
        text_area.tag_remove('match', '1.0', END)
        if word:
            start_pos = '1.0'
            while True:
                start_pos = text_area.search(word, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f'{start_pos} + {len(word)}c'
                text_area.tag_add('match', start_pos, end_pos)
                start_pos = end_pos
                text_area.tag_config('match', foreground='blue', background='yellow')

    def replace():
        find_word = find_entry_field.get()
        replace_word = replace_entry_field.get()
        new_word = text_area.get(1.0, END).replace(find_word, replace_word)
        text_area.delete(1.0, END)
        text_area.insert(1.0, new_word)

    # Dialog Box
    dbox = Toplevel()
    dbox.geometry('450x220')
    dbox.title('Find & Replace')
    dbox.resizable(0, 0)

    fr_frame = ttk.LabelFrame(dbox, text='Find | Replace')
    fr_frame.pack(pady=20)

    find_label = ttk.Label(fr_frame, text='Find')
    find_label.grid(row=0, column=0, pady=5)

    find_entry_field = ttk.Entry(fr_frame, width=30)
    find_entry_field.grid(row=0, column=1, pady=5)

    replace_label = ttk.Label(fr_frame, text='Replace')
    replace_label.grid(row=1, column=0, pady=5)

    replace_entry_field = ttk.Entry(fr_frame, width=30)
    replace_entry_field.grid(row=1, column=1, pady=5)

    find_btn = ttk.Button(fr_frame, text='Find', command=find)
    find_btn.grid(row=2, column=0, pady=5, padx=5)

    replace_btn = ttk.Button(fr_frame, text='Replace', command=replace)
    replace_btn.grid(row=2, column=1, pady=5, padx=5)


def hide_tool_bar(event=None):
    global show_tool_bar
    if show_tool_bar:
        tool_bar_label.pack_forget()
        show_tool_bar = False
    else:
        text_area.pack_forget()
        tool_bar_label.pack(side=TOP, fill=X)
        text_area.pack(fill=BOTH, expand=True)
        show_tool_bar = True


def hide_status_bar():
    global show_status_bar
    if show_status_bar:
        status_bar_label.pack_forget()
        show_status_bar = False
    else:
        text_area.pack_forget()
        status_bar_label.pack(side=BOTTOM)
        text_area.pack(fill=BOTH, expand=True)
        show_status_bar = True


current_font = 'Courier New'
current_size = 16


# Changing font
def change_font(event=None):
    global current_font
    current_font = font_var.get()
    text_area.config(font=(current_font, current_size))


def change_font_size(event=None):
    global current_size
    current_size = size_var.get()
    text_area.config(font=(current_font, current_size))


# Creating Menu bar
menu_bar = Menu(screen)

# Creating file menu drop down
file_menu = Menu(menu_bar, tearoff=False)

new_file = PhotoImage(file='images/new_file.png')
open_file = PhotoImage(file='images/open_file.png')
save_file = PhotoImage(file='images/save_file.png')
exit_file = PhotoImage(file='images/exit_file.png')

file_menu.add_command(label='New', accelerator='Ctrl+N', image=new_file,
                      compound=LEFT, command=new)
file_menu.add_command(label='Open', accelerator='Ctrl+O', image=open_file,
                      compound=LEFT, command=open_func)
file_menu.add_command(label='Save', accelerator='Ctrl+S', image=save_file,
                      compound=LEFT, command=save)
file_menu.add_command(label='Save as', accelerator='Ctrl+Shift+S', image=save_file,
                      compound=LEFT, command=save_as)
file_menu.add_command(label='Exit', accelerator='Esc', image=exit_file,
                      compound=LEFT, command=close)

menu_bar.add_cascade(label='File', menu=file_menu)

# Creating edit menu
edit_menu = Menu(menu_bar, tearoff=False)

copy_file = PhotoImage(file='images/copy_file.png')
cut_file = PhotoImage(file='images/cut_file.png')
clear_file = PhotoImage(file='images/clear_file.png')
paste_file = PhotoImage(file='images/paste_file.png')
undo_file = PhotoImage(file='images/undo.png')
redo_file = PhotoImage(file='images/redo.png')
find_file_icon = PhotoImage(file='images/find.png')

edit_menu.add_command(label='Copy', accelerator='Ctrl+C', image=copy_file,
                      compound=LEFT, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', image=paste_file,
                      compound=LEFT, command=paste)
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', image=cut_file,
                      compound=LEFT, command=cut)
edit_menu.add_command(label='Clear All', accelerator='Ctrl+D', image=clear_file,
                      compound=LEFT, command=clear_all)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', image=redo_file,
                      compound=LEFT, command=text_area.edit_redo)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', image=undo_file,
                      compound=LEFT, command=text_area.edit_undo)
edit_menu.add_command(label='Find', image=find_file_icon, compound=LEFT,
                      accelerator='Ctrl+F', command=find_replace)

menu_bar.add_cascade(label='Edit', menu=edit_menu)

# Creating theme menu
# colors = {'theme_name': (fg color, bg color)}

color_var = StringVar()

colors = {
    'Light': ('#000000', '#FFFFFF'),
    'Dark': ('#c4c4c4', '#2d2d2d'),
    'Red': ('#2d2d2d', '#ffe8e8'),
    'Blue': ('#ededed', '#6b9dc2'),
    'Yellow': ('#440A0A', '#E2F56A')
}


def change_theme():
    theme = color_var.get()
    value = colors.get(theme)
    # print('Fg and Bg =', value)
    foreground, background = value
    # print('Foreground =', fg)
    # print('Background =', bg)
    text_area.config(bg=background, fg=foreground)  # fg is text color


light_theme = PhotoImage(file='images/white-circle.png')
dark_theme = PhotoImage(file='images/dark-circle.png')
red_theme = PhotoImage(file='images/red_circle.png')
blue_theme = PhotoImage(file='images/blue-circle.png')
yellow_theme = PhotoImage(file='images/yellow_theme.png')

color_theme = Menu(menu_bar, tearoff=False)

color_theme.add_radiobutton(label='Light', image=light_theme, variable=color_var,
                            compound=LEFT, command=change_theme)
color_theme.add_radiobutton(label='Dark', image=dark_theme, variable=color_var,
                            compound=LEFT, command=change_theme)
color_theme.add_radiobutton(label='Red', image=red_theme, variable=color_var,
                            compound=LEFT, command=change_theme)
color_theme.add_radiobutton(label='Blue', image=blue_theme, variable=color_var,
                            compound=LEFT, command=change_theme)
color_theme.add_radiobutton(label='Yellow', image=yellow_theme, variable=color_var,
                            compound=LEFT, command=change_theme)

menu_bar.add_cascade(label='Theme', menu=color_theme)

# Creating view menu drop down
tool_bar_icon = PhotoImage(file='images/tool_bar.png')
status_bar_icon = PhotoImage(file='images/status_bar.png')

# Creating tool bar label
tool_bar_label = Label(screen)
tool_bar_label.pack(side=TOP, fill=X)
show_tool_bar = BooleanVar()
show_tool_bar.set(True)

# Creating status bar label
status_bar_label = Label(screen, text='Status Bar')
status_bar_label.pack(side=BOTTOM, fill = X)
show_status_bar = BooleanVar()
show_status_bar.set(True)

view_menu = Menu(menu_bar, tearoff=False)
view_menu.add_checkbutton(label='Tool bar', onvalue=True, offvalue=False,
                          variable=show_tool_bar, image=tool_bar_icon, compound=LEFT,
                          command=hide_tool_bar)
view_menu.add_checkbutton(label='Status bar', onvalue=True, offvalue=False,
                          variable=show_status_bar, image=status_bar_icon, compound=LEFT,
                          command=hide_status_bar)
menu_bar.add_cascade(label='View', menu=view_menu)

##----- Creating Tool Bar Option -----------##
# Creating font name box
font_tup = font.families()
font_var = StringVar()
font_box = ttk.Combobox(tool_bar_label, width=30, textvariable=font_var, state='readonly')
font_box['values'] = font_tup
font_box.current(font_tup.index('Courier New'))
font_box.grid(row=0, column=0, padx=5, pady=5)

# Creating font size box
size_var = IntVar()
size_box = ttk.Combobox(tool_bar_label, width=20, textvariable=size_var, state='readonly')
size_box['values'] = tuple(range(8, 100, 2))
size_box.current(4)
size_box.grid(row=0, column=1, padx=5)

# Creating scroll bar
scroll_bar = Scrollbar(screen)
scroll_bar.pack(side=RIGHT, fill=Y)
text_area.focus_set()
text_area.pack(fill=BOTH, expand=True)
scroll_bar.config(command=text_area.yview)
text_area.config(yscrollcommand=scroll_bar.set)


screen.config(menu=menu_bar)
text_area.bind('<<Modified>>', wordin_textarea)
font_box.bind('<<ComboboxSelected>>', change_font)
size_box.bind('<<ComboboxSelected>>', change_font_size)
screen.bind('<Control-n>', new)
screen.bind('<Control-o>', open_func)
screen.bind('<Control-s>', save)
screen.bind('<Control-Shift-S>', save_as)
screen.bind('<Escape>', close)
screen.bind('<Control-d>', clear_all)
screen.bind('<Control-f>', find_replace)
screen.protocol("WM_DELETE_WINDOW", close)
screen.mainloop()
