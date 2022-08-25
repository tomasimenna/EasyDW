from cgitb import text
import sys, threading, pyodbc, observer, datetime
from turtle import width
from tkinter.tix import AUTO
from tkinter import filedialog, messagebox
from tkinter import *
from tkinter.scrolledtext import ScrolledText
   

class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", f'''{text}''')  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class MainGUI(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.folder_set = False
        self.server_set = False
        self.a = 1

        def path_variable():
            self.path_to_monitor = filedialog.askdirectory()
            path_entry.config(text=self.path_to_monitor)
            self.folder_set = True
            enable_start()
        
        def server_variable():
            self.server_to_connect = str(server_entry.get())
            
            if self.a == 1:
                self.status_label = Label(top_left_column, text='Checking connection...')
                self.status_label.grid(row=3, column=2, padx=(10), pady=(5), sticky=W)
                self.a = 2
            else:
                self.status_label.config(text='Checking connection...', fg = 'black')
                
            try:
                self.start_button.config(state=DISABLED)
                conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' f'Server={self.server_to_connect};' f'Database=master;' 'Trusted_Connection=yes;' 'ColumnEncryption=Enabled')
                conn.close()
                self.status_label.config(text='Connection Successful', fg='green')
                self.server_set = True
                server_button.config(state=NORMAL)
                enable_start()

            except:
                self.start_button.config(state=DISABLED)
                self.status_label.config(text='Connection Failed', fg='red')
                self.server_set = False
                server_button.config(state=NORMAL)

        def conn_to_server():
            self.server_set = False
            server_button.config(state=DISABLED)
            t = threading.Thread(target = server_variable)
            t.start()

        def enable_start():
            if self.folder_set == True and self.server_set == True:
                self.start_button.config(state=NORMAL)

        def hide_widget():
            if self.ex_status == 'visible':
                self.ex_log_label.grid_forget()
                self.ex_log_widget.grid_forget()
                logs_frame.columnconfigure(1, weight=0)
                ex_hide_button.config(text='Show Ex.')
                self.ex_status = 'hidden'
            else:
                self.ex_log_label.grid(row=0, column=1, padx=(10), pady=(10))
                self.ex_log_widget.grid(row=1, column=1, padx=(10), pady=(0), sticky=E+W+N+S)
                logs_frame.columnconfigure(1, weight=1)
                ex_hide_button.config(text='Hide Ex.')
                self.ex_status = 'visible'

        self.title('EasyDW')
        self.icon = PhotoImage(file = r'media\logo.png')
        self.iconphoto(False, self.icon)

        self.geometry('1000x400')
        self.minsize(700, 400)

    # Left Column
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = Frame(self)
        main_frame.grid(row=0, column=0, sticky=W+E+N+S)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        top_row = Frame(main_frame)
        top_row.grid(column=0, row=0, sticky=W+E+N)
        top_row.columnconfigure(0, weight=1)

        top_left_column = Frame(top_row)
        top_left_column.grid(row=0, column=0, sticky=W+E+N)

        top_left_column.columnconfigure(0, weight=1)
        top_left_column.rowconfigure(0, weight=1)
        top_left_column.rowconfigure(1, weight=1)

        path_label = Label(top_left_column, text = 'Please select a local folder to monitor')
        path_label.grid(row=0, column=0, padx=(10), pady=(5), sticky=W)
        path_entry = Label(top_left_column, text = '')
        path_entry.grid(row=1, column=0, padx=(10), pady=(5), sticky=W)
        path_button = Button(top_left_column, text="Select Folder", command=path_variable)
        path_button.grid(row=1, column=1, padx=(10), pady=(5), sticky=W)

        server_label = Label(top_left_column, text = 'Insert server of the database')
        server_label.grid(row=2, column=0, padx=(10), pady=(5), sticky=W)
        server_entry_text = StringVar()
        server_entry = Entry(top_left_column, width = 30, textvariable = server_entry_text)
        server_entry.grid(row=3, column=0, padx=(10), pady=(5), sticky=W+E)
        server_button= Button(top_left_column, text="Check & Set", command=conn_to_server)
        server_button.grid(row=3, column=1, padx=(10), pady=(5), sticky=W)

        monitor_frame = Frame(main_frame)
        monitor_frame.grid(row=1, column=0, sticky=W+E+N)
        monitor_frame.columnconfigure(0, weight=1)
        monitor_frame.columnconfigure(1, weight=1)

        monitor_frame_left = Frame(monitor_frame)
        monitor_frame_left.grid(row=0, column=0, sticky=W+E)
        monitor_frame_left.columnconfigure(0, weight=1)

        self.start_button = Button(monitor_frame_left, text="Start Monitoring", command=self.monitor, state=DISABLED)
        self.start_button.grid(row=0, column=0, padx=(10), pady= (10), sticky=E)

        monitor_frame_right = Frame(monitor_frame)
        monitor_frame_right.grid(row=0, column=1, sticky=W+E)
        monitor_frame_right.columnconfigure(0, weight=1)

        self.stop_button = Button(monitor_frame_right, text="Stop Monitoring", command=self.stop_monitor, state=DISABLED)
        self.stop_button.grid(row=0, column=0, padx=(10), pady= (10), sticky=W)

        logs_frame = LabelFrame(main_frame)
        logs_frame.grid(row=2, column=0, padx=(10), pady=(0), sticky=W+E+N+S)

        op_log_label = Label(logs_frame, text = "Operation's log")
        op_log_label.grid(row=0, column=0, padx=(10), pady=(5))
        op_log_widget = ScrolledText(logs_frame, width=10, height=10,  font=("consolas", "8", "normal"))
        op_log_widget.grid(row=1, column=0, padx=(10), pady=(0), sticky=E+W+N+S)
        op_logger = PrintLogger(op_log_widget)
        sys.stdout = op_logger
        ex_hide_button= Button(logs_frame, text= "Hide Ex.", command= lambda:hide_widget())
        ex_hide_button.grid(row=0, column=0, padx=(10), pady=(5), sticky=E)

        def save_log(log_widget):

            def reset_op_log():
                log_widget.configure(state="normal")
                log_widget.delete('1.0', END)
                log_widget.configure(state="disabled")

            def ask_if_reset():
                ans = messagebox.askquestion("Form", "Do you want reset the log?")
                if ans == 'yes':
                    reset_op_log()
                else:
                    pass

            cur_inp = log_widget.get("1.0", END)
            save_path = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
            if save_path:
                fl = open(save_path.name, "w")
                fl.write(cur_inp)
                ask_if_reset()
            else:
                pass

        save_logs_frame = Frame(logs_frame)
        save_logs_frame.grid(row=0, column=0, padx=(0), pady=(0), sticky=W)
        save_op_log_button = Button(save_logs_frame, text="Save Op. Log", command= lambda:save_log(op_log_widget))
        save_op_log_button.grid(row=0, column=0, padx=(10), pady=(5), sticky=W)
        save_ex_log_button = Button(save_logs_frame, text="Save Ex. Log", command= lambda:save_log(self.ex_log_widget))
        save_ex_log_button.grid(row=0, column=1, padx=(10), pady=(5), sticky=W)

        self.ex_status = 'visible'
        self.ex_log_label = Label(logs_frame, text = "Exception's log")
        self.ex_log_label.grid(row=0, column=1, padx=(10), pady=(5))
        self.ex_log_widget = ScrolledText(logs_frame, width=10, height=10, font=("consolas", "8", "normal"))
        self.ex_log_widget.grid(row=1, column=1, padx=(10), pady=(0), sticky=E+W+N+S)
        ex_logger = PrintLogger(self.ex_log_widget)
        sys.stderr = ex_logger

        logs_frame.columnconfigure(0, weight=4)
        logs_frame.columnconfigure(1, weight=1)
        logs_frame.rowconfigure(1, weight=1)


        top_right_col = Frame(top_row)
        top_right_col.grid(row=0, column=1, sticky=E)

        self.img = PhotoImage(file = r'media\image.png')
        self.imgLabel = Label(top_right_col, image=self.img)
        self.imgLabel.grid(row=0, column=0, padx=(20), pady=(10), sticky=S)
        team_label = Label(top_right_col, text='Reporting tools')
        team_label.grid(row=1, column=0, padx = (20), pady=(5), sticky=N)

    def monitor(self):
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        def Worker():
            observer.start_monitoring(path_to_monitor = self.path_to_monitor, server_to_connect=self.server_to_connect)

        class Monitorthread(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
            def run(self):
                Worker()

        Monitorthread.daemon=True
        Monitorthread().start()
        

    def stop_monitor(self):
        observer.stop_monitoring()
        print(f'''{str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'))}: Monitoring stopped''')
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED) 

if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
