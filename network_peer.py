import os
import json
import socket
import threading
import time
import random
from base import Base
 
# GUI
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from PIL import ImageTk 

# aid
from hash_function import MD5_hash
import asset

# ----CONSTANT----#
FORMAT = "utf-8"
BUFFER_SIZE = 2048
OFFSET = 10000

## ====================GUI IMPLEMENT======================##


def display_noti(title, content):
    tkinter.messagebox.showinfo(title, content)


class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.chatroom_textCons = None

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, RegisterPage, LoginPage, ChatPage):
            frame = F(container, self)
            # initializing frame of that object from
            # startpage, registerpage, loginpage, chatpage respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg='white')
        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Welcome to WeChat", bg="#bf8bff", fg="white",
                 height="2", font=("Verdana", 13)).pack(fill='x')
        tk.Label(self, text="", bg='white').pack()

        # Set port label
        tk.Label(self, text="Set Port (1 -> 9999)", bg='white').pack()
        # Set port entry
        self.port_entry = tk.Entry(
            self, width="20", font=("Verdana", 11))
        self.port_entry.pack()
        tk.Label(self, text="", bg='white').pack()

        # create a register button
        tk.Button(self, text="Register", height="2", width="30", bg="#5D0CB5", fg="white", command=lambda: self.enter_app(
            controller=controller, port=self.port_entry.get(), page=RegisterPage)).pack()
        tk.Label(self, text="", bg='white').pack()

        # create a login button
        tk.Button(self, text="Login", height="2", width="30", bg="#A021E2", fg="white", command=lambda: self.enter_app(
            controller=controller, port=self.port_entry.get(), page=LoginPage)).pack()

    def enter_app(self, controller, port, page):
        try:
            # get peer current ip address -> assign to serverhost
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)  

            # init server
            global network_peer
            network_peer = NetworkPeer(serverhost=IPAddr, serverport=int(port))
           
            # A child thread for receiving message
            recv_t = threading.Thread(target=network_peer.input_recv)
            recv_t.daemon = True
            recv_t.start()

            # A child thread for receiving file
            recv_file_t = threading.Thread(target=network_peer.recv_file_content)
            recv_file_t.daemon = True
            recv_file_t.start()
            controller.show_frame(page)
        except:
            self.port_entry.delete(0, tk.END)
            display_noti("Port Error",  "Port has been used or null!")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Sign Up Image
        signup_pic = ImageTk.PhotoImage(asset.signup_image)
        signupImg = tk.Label(self, image=signup_pic, bg='white')
        signupImg.image = signup_pic
        signupImg.place(x=50, y=50)

        # Title
        tk.Label(self, text='Sign Up',
                 fg='#bf8bff', bg='white',
                 font=("Roboto", 24, 'bold')).place(x=670, y=100)
        # Username
        tk.Label(self, text='Username', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=175)
        self.username_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10))
        self.username_entry.place(x=675, y=200)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=225)

        # Password
        tk.Label(self, text='Password', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=250)
        self.password_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10), show='*')
        self.password_entry.place(x=675, y=275)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=300)

        # Submit
        tk.Button(self, width=39, pady=7, text='Sign Up', bg='#bf8bff',
                  fg='white', border=0, command=lambda: self.register_user(self.username_entry.get(), self.password_entry.get())).place(x=675, y=325)
        tk.Label(self, text="Already have an account ?",
                 fg='black', bg='white', font=("Roboto", 10)).place(x=675, y=375)
        tk.Button(self, width=6, text='Sign in', border=0,
                  bg='white', cursor='hand2', fg='#57a1f8', command=lambda: controller.show_frame(LoginPage)).place(x=670, y=400)

    def register_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        network_peer.send_register()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Login Image
        login_pic = ImageTk.PhotoImage(asset.login_image)
        loginImg = tk.Label(self, image=login_pic, bg='white')
        loginImg.image = login_pic
        loginImg.place(x=50, y=50)

        # Title
        tk.Label(self, text='Login',
                 fg='#bf8bff', bg='white',
                 font=("Roboto", 24, 'bold')).place(x=670, y=100)

        # Username
        tk.Label(self, text='Username', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=175)
        self.username_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10))
        self.username_entry.place(x=675, y=200)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=225)

        # Password
        tk.Label(self, text='Password', bg='white',
                 fg='#57a1f8', font=("Roboto", 11)).place(x=670, y=250)
        self.password_entry = tk.Entry(self, width=25, fg='black', border=0,
                                       bg='white', font=("Roboto", 10), show='*')
        self.password_entry.place(x=675, y=275)
        tk.Frame(self, width=275, height=2, bg='#777777').place(x=675, y=300)

        # Submit
        tk.Button(self, width=39, pady=7, text='Login', bg='#bf8bff',
                  fg='white', border=0, command=lambda: self.login_user(username=self.username_entry.get(), password=self.password_entry.get())).place(x=675, y=325)
        tk.Label(self, text="Don't have an account ?",
                 fg='black', bg='white', font=("Roboto", 10)).place(x=675, y=375)
        tk.Button(self, width=6, text='Sign up', border=0,
                  bg='white', cursor='hand2', fg='#57a1f8', command=lambda: controller.show_frame(RegisterPage)).place(x=670, y=400)

    def login_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        network_peer.send_login()


class PrivateChatPage(tk.Frame):
    def __init__(self, parent, controller, friend_name):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.friend_name = friend_name
        self.msg = ""

        tk.Label(self, bg="#573d9c", fg="#ffffff", text=friend_name,
                 font="Helvetica 17 bold", pady=15).grid(row=0, column=0, columnspan=2, sticky="news")

        chatroom_icon = ImageTk.PhotoImage(asset.chatroom_icon)
        chatroom_button = tk.Button(self, image=chatroom_icon, border=0,
                                  background="#573d9c", activebackground="#573d9c",
                                  command=lambda: self.open_chatroom())
        chatroom_button.image = chatroom_icon
        chatroom_button.grid(row=0, column=2, columnspan=3, sticky="news")

        self.message_area = tk.Text(
            self, bg="#f2f0f6", fg="#1b142c", font="Helvetica 13", width=1, padx=15, pady=15)
        self.message_area.grid(row=1, column=0, columnspan=3, sticky="news")
        self.message_area.config(cursor="arrow")
        self.message_area.config(state=tk.DISABLED)

        self.entry_msg = tk.Entry(
            self, bg="#ffffff", font="Helvetica 13", highlightthickness=2, highlightcolor="#cbc9ff")
        self.entry_msg.grid(row=2, column=0, sticky="news")

        tk.Button(self, text="Text", width=6, height=1, pady=5,
                  bg="#462d86", fg='#ffffff', font="Helvetica 14 bold",
                  command=lambda: self.sendText(str(self.entry_msg.get()))).grid(row=2, column=1, sticky="news")

        tk.Button(self, text="File", width=6, height=1, pady=5,
                  bg="#ffffff", fg='#462d86', font="Helvetica 14 bold",
                  command=lambda friend=friend_name: self.sendFile(friend)).grid(row=2, column=2, sticky="news")

        # create a scroll bar
        text_scrollbar = tk.Scrollbar(self, orient='vertical')
        text_scrollbar.grid(row=1, column=3, sticky='nse')
        self.message_area.config(yscrollcommand=text_scrollbar.set)
        # Attach the scrollbar with the text widget
        text_scrollbar.config(command=self.message_area.yview)

        self.grid(row=0, column=0, sticky="nsew")

    def sendText(self, msg):
        if msg != "":
            self.msg = msg
            self.entry_msg.delete(0, tk.END)
            st_t = threading.Thread(
                target=network_peer.send_chat_message, args=(self.friend_name, self.msg))
            st_t.daemon = True
            st_t.start()
            # insert messages to text box
            message = network_peer.name + ": " + self.msg
            self.message_area.config(state=tk.NORMAL)
            self.message_area.insert(tk.END, message+"\n\n")
            self.message_area.config(state=tk.DISABLED)
            self.message_area.see(tk.END)

    def sendFile(self, friend_name):
        file_path = tkinter.filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("all files", "*.*")))
        file_name = os.path.basename(file_path)
        msg_box = tkinter.messagebox.askquestion('File Explorer', 'Are you sure to send {} to {}?'.format(file_name, friend_name),
                                                 icon="question")
        if msg_box == 'yes':
            sf_t = threading.Thread(
                target=network_peer.transfer_file, args=(self.friend_name, file_path))
            sf_t.daemon = True
            sf_t.start()
            tkinter.messagebox.showinfo(
                "File Transfer", '{} has been sent to {}!'.format(file_name, friend_name))
    
    def open_chatroom(self): 
        chatroom = tk.Toplevel(app)
     
        chatroom.title("Chat room")
        
        chatroom.geometry("470x550")

        labelHead = tk.Label(chatroom,
                               bg="#17202A",
                               fg="#EAECEE",
                               text="WeChat Public Room",
                               font="Helvetica 13 bold",
                               pady=5)
 
        labelHead.place(relwidth=1)
        line = tk.Label(chatroom,
                          width=450,
                          bg="#ABB2B9")
 
        line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
        
     

        app.chatroom_textCons = tk.Text(chatroom,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
 
        app.chatroom_textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        labelBottom = tk.Label(chatroom,
                                 bg="#ABB2B9",
                                 height=80)
 
        labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = tk.Entry(labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
 
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # create a Send Button
        self.buttonMsg = tk.Button(labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9", command=lambda: self.sendPublicChatButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        app.chatroom_textCons.config(cursor="arrow")
 
        # create a scroll bar
        scrollbar = tk.Scrollbar(app.chatroom_textCons)
 
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=app.chatroom_textCons.yview)
 
        app.chatroom_textCons.config(state=tk.DISABLED)
    
        # Display until closed manually
        chatroom.mainloop()
    
    # function to send public messages
    def sendPublicChatButton(self, msg):
        app.chatroom_textCons.config(state=tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        snd = threading.Thread(target=network_peer.sendPublicMessage, args=(self.msg,))
        snd.daemon = True
        snd.start()
 

class ChatPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.frame_list = {}

        self.f1 = tk.Frame(self, background="bisque")
        self.f2 = tk.Frame(self, background="yellow")
        self.f3 = tk.Frame(self, background="pink")

        self.f1.grid(row=0, column=0, sticky="nsew")
        self.f2.grid(row=0, column=1, sticky="nsew")
        self.f3.grid(row=0, column=2, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # chat area
        self.f2.grid_columnconfigure(0, weight=1)
        self.f2.grid_rowconfigure(0, weight=1)

        chat_frame = PrivateChatPage(
            parent=self.f2, controller=self, friend_name="MyPrivateMessage")
        self.frame_list["MyPrivateMessage"] = chat_frame
        self.frame_list["MyPrivateMessage"].tkraise()

        # request chat area
        self.f3.grid_columnconfigure(0, weight=1)
        self.f3.grid_rowconfigure(1, weight=1)

        request_label = tk.Label(self.f3, text="Request For Chat", bg="#8372f2",
                                 fg="#e6e6fa", font="Helvetica 13 bold", pady=5, height=2, width=1)
        request_label.grid(row=0, column=0, sticky="news")

        logout_icon = ImageTk.PhotoImage(asset.logout_icon)
        logout_button = tk.Button(self.f3, image=logout_icon, border=0,
                                  background="#8372f2", activebackground="#6a54f7",
                                  command=lambda: self.log_out())
        logout_button.image = logout_icon
        logout_button.grid(row=0, column=1, sticky="news")

        wrapper = tk.Frame(self.f3)
        wrapper.grid(row=1, column=0, columnspan=2, sticky="news")

        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(0, weight=1)

        mycanvas = tk.Canvas(wrapper, background="#f0f0ff", width=1)
        mycanvas.grid(row=0, column=0, sticky="news")

        yscrollbar = tk.Scrollbar(
            wrapper, orient="vertical", command=mycanvas.yview)
        yscrollbar.grid(row=0, column=1, sticky='ns')

        mycanvas.configure(yscrollcommand=yscrollbar.set)

        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(
            scrollregion=mycanvas.bbox('all')))

        online_frame = tk.Frame(mycanvas)
        mycanvas.create_window((0, 0), window=online_frame)

        reload_icon = ImageTk.PhotoImage(asset.reload_icon)
        reload_button = tk.Button(online_frame, image=reload_icon, border=0,
                                  background="#f0f0ff", activebackground="#eeedff",
                                  command=lambda: self.update_online_user_list())
        reload_button.image = reload_icon
        reload_button.grid(row=0, column=0, sticky="news")

        tk.Label(online_frame, text="Update", background="#f0f0ff", pady=25,
                 font="Helvetica 15 bold").grid(row=0, column=1, sticky="news")

        request_img = ImageTk.PhotoImage(asset.request_image)
        self.user_name_frame = []
        for i in range(1, 100):
            user_img = tk.Label(
                online_frame, image=request_img, background="#f0f0ff")
            user_img.grid(row=i, column=0, sticky="news")
            user_img.image = request_img

            user_name = tk.Button(online_frame, text="Load to see...", width=12, pady=20, background="#f0f0ff",
                                  activebackground="#eeedff", border=0, highlightcolor="#f0f0ff", font="Helvetica 10", fg="#1b142c")
            user_name.grid(row=i, column=1, sticky="news")
            self.user_name_frame.append(user_name)

        # friend area
        self.f1.grid_columnconfigure(0, weight=1)
        self.f1.grid_rowconfigure(1, weight=1)

        send_label = tk.Label(self.f1, text="My Friend List", bg="#cca3ff",
                              fg="#7f00ff", font="Helvetica 13 bold", pady=5, height=2, width=1)
        send_label.grid(row=0, column=0, sticky="nwe")

        wrapper_2 = tk.Frame(self.f1)
        wrapper_2.grid(row=1, column=0, sticky="news")

        wrapper_2.grid_columnconfigure(0, weight=1)
        wrapper_2.grid_rowconfigure(0, weight=1)

        mycanvas_2 = tk.Canvas(wrapper_2, background="#f1e8fc", width=1)
        mycanvas_2.grid(row=0, column=0, sticky="news")

        yscrollbar_2 = tk.Scrollbar(
            wrapper_2, orient="vertical", command=mycanvas_2.yview)
        yscrollbar_2.grid(row=0, column=1, sticky='ns')

        mycanvas_2.configure(yscrollcommand=yscrollbar_2.set)
        mycanvas_2.bind('<Configure>', lambda e: mycanvas_2.configure(
            scrollregion=mycanvas_2.bbox('all')))

        friend_frame = tk.Frame(mycanvas_2)
        mycanvas_2.create_window((0, 0), window=friend_frame)

        reload_button_2 = tk.Button(friend_frame, image=reload_icon, border=0,
                                    background="#f1e8fc", activebackground="#eee3fa",
                                    command=lambda: self.update_friend_list())
        reload_button_2.image = reload_icon
        reload_button_2.grid(row=0, column=0, sticky="news")

        tk.Label(friend_frame, text="Update", background="#f1e8fc", pady=25,
                 font="Helvetica 15 bold").grid(row=0, column=1, sticky="news")

        friend_img = ImageTk.PhotoImage(asset.friend_image)
        self.friend_name_frame = []
        for i in range(1, 100):
            friend_img_container = tk.Label(
                friend_frame, image=friend_img, background="#f1e8fc")
            friend_img_container.image = friend_img
            friend_img_container.grid(row=i, column=0, sticky="news", ipadx=10)

            friend_name = tk.Button(friend_frame, text="Load to see...", width=12, pady=20, background="#f1e8fc",
                                    activebackground="#eee3fa", border=0, highlightcolor="#f0f0ff", font="Helvetica 10", fg="#1b142c")
            friend_name.grid(row=i, column=1, sticky="news")
            self.friend_name_frame.append(friend_name)

    def update_online_user_list(self):
        # request getting online user list
        network_peer.send_listpeer()
        time.sleep(0.1)
        
        for j in range(0, len(self.user_name_frame)):
            self.user_name_frame[j].config(text="Load to see...")
            self.user_name_frame[j].config(command=None)
        
        if len(network_peer.onlinelist) > 0:
            i = 0
            for online_user in network_peer.onlinelist:
                self.user_name_frame[i].config(text=online_user)
                self.user_name_frame[i].config(
                    command=lambda online_user=online_user: self.make_chat_request(online_user))
                i = i+1

    def make_chat_request(self, online_user):
        network_peer.send_request(online_user)

    def update_friend_list(self):
        i = 0
        for key, value in network_peer.friendlist.items():
            self.friend_name_frame[i].config(text=key)
            self.friend_name_frame[i].config(
                command=lambda friend=key: self.raise_private_chat(friend))
            i = i+1

    def raise_private_chat(self, friend):
        chat_frame = PrivateChatPage(
            parent=self.f2, controller=self, friend_name=friend)
        self.frame_list[friend] = chat_frame
        self.frame_list[friend].tkraise()
    
    def log_out(self):
        app.show_frame(LoginPage)
        network_peer.send_logout_request()
## =======================================================##

## ====================CORE IMPLEMENT======================##


class NetworkPeer(Base):
    def __init__(self, serverhost='localhost', serverport=30000, server_info=('192.168.1.8', 40000)):
        super(NetworkPeer, self).__init__(serverhost, serverport)

        # init host and port of central server
        self.server_info = server_info

        # peer name
        self.name = ""
        # peer password
        self.password = ""

        # all peers it can connect (network peers)
        self.connectable_peer = {}
        self.onlinelist = []
        # peers it has connected (friend)
        self.friendlist = {}

        self.message_format = '{peername}: {message}'
        # file buffer
        self.file_buf = []

        # define handlers for received message of network peer
        handlers = {
            'REGISTER_SUCCESS': self.register_success,
            'REGISTER_ERROR': self.register_error,
            'LOGIN_SUCCESS': self.login_success,
            'LOGIN_ERROR': self.login_error,
            'LIST_ONLINE_USER': self.get_online_users,
            'CHAT_REQUEST': self.chat_request,
            'CHAT_ACCEPT': self.chat_accept,
            'CHAT_REFUSE': self.chat_refuse,
            'CHAT_MESSAGE': self.recv_message,
            'CHAT_PUBLIC': self.recv_public_message,
        }
        for msgtype, function in handlers.items():
            self.add_handler(msgtype, function)

    ## ==========implement protocol for user registration - network peer==========##
    def send_register(self):
        """ Send a request to server to register peer's information. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_REGISTER', msgdata=peer_info)

    def register_success(self, msgdata):
        """ Processing received message from server: Successful registration on the server. """
        display_noti('Register Noti', 'Register Successful.')
        print('Register Successful.')

    def register_error(self, msgdata):
        """ Processing received message from server: Registration failed on the server. """
        display_noti('Register Noti',
                     'Register Error. Username existed or null!')
        print('Register Error. Username existed. Login!')
    ## ===========================================================##

    ## ==========implement protocol for authentication (log in) - network peer==========##
    def send_login(self):
        """ Send a request to server to login. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGIN', msgdata=peer_info)

    def login_success(self, msgdata):
        """ Processing received message from server: Successful login on the server. """
        print('Login Successful.')
        display_noti('Login Noti', 'Login Successful.')
        app.geometry("1100x600")
        app.resizable(False, False)
        app.show_frame(ChatPage)

    def login_error(self, msgdata):
        """ Processing received message from server: Login failed on the server. """
        display_noti('Login Noti', 'Login Error. Username not existed!')
        print('Login Error. Username not existed. Register!')
    ## ===========================================================##

    ## ==========implement protocol for getting online user list - network peer==========##
    def send_listpeer(self):
        """ Send a request to server to get all online peers. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LIST', msgdata=peer_info)

    def get_online_users(self, msgdata):
        """ Processing received message from server:
            Output username of all peers that have been registered on the server and are online."""
        self.connectable_peer.clear()
        for key, value in msgdata['online_user_list'].items():
            self.connectable_peer[key] = tuple(value)
        if self.name in self.connectable_peer:
            self.connectable_peer.pop(self.name)
        self.onlinelist = [key for key, value in self.connectable_peer.items()]
    ## ===========================================================##

    ## ==========implement protocol for chat request (can upgrade to friend request)==========##
    def send_request(self, peername):
        """ Send a chat request to an online user. """
        if peername not in self.friendlist:
            try:
                server_info = self.connectable_peer[peername]
            except KeyError:
                display_noti("Chat Request Error",
                             'This peer ({}) is not available.'.format(peername))
            else:
                data = {
                    'peername': self.name,
                    'host': self.serverhost,
                    'port': self.serverport
                }
                self.client_send(
                    server_info, msgtype='CHAT_REQUEST', msgdata=data)
        else:
            display_noti("Chat Request Error",
                         'You have already connected to {}.'.format(peername))

    def chat_request(self, msgdata):
        """ Processing received chat request message from peer. """
        peername = msgdata['peername']
        host, port = msgdata['host'], msgdata['port']
        msg_box = tk.messagebox.askquestion('Chat Request', 'Do you want to accept {} - {}:{}?'.format(peername, host, port),
                                            icon="question")
        if msg_box == 'yes':
            # if request is agreed, connect to peer (add to friendlist)
            data = {
                'peername': self.name,
                'host': self.serverhost,
                'port': self.serverport
            }
            self.client_send((host, port), msgtype='CHAT_ACCEPT', msgdata=data)
            display_noti("Chat Request Accepted",
                         "Update to get in touch with new friend!")
            self.friendlist[peername] = (host, port)
        else:
            self.client_send((host, port), msgtype='CHAT_REFUSE', msgdata={})

    def chat_accept(self, msgdata):
        """ Processing received accept chat request message from peer.
            Add the peer to collection of friends. """
        peername = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        display_noti("Chat Request Result",
                     'CHAT ACCEPTED: {} --- {}:{}. Update to get in touch with new friend!'.format(peername, host, port))
        self.friendlist[peername] = (host, port)

    def chat_refuse(self, msgdata):
        """ Processing received refuse chat request message from peer. """
        display_noti("Chat Request Result", 'CHAT REFUSED!')
    ## ===========================================================##

    ## ==========implement protocol for public messaging==========##
    def sendPublicMessage(self, message):
        """ Send a chat message to public community. """
        try:
            data = {
                'name': self.name,
                'message': message
            }
            self.client_send(self.server_info, msgtype='PUBLIC_CHAT', msgdata=data)
        except KeyError:
            display_noti("Public Messaging Result", 'Cannot send message!')
    
    def recv_public_message(self, msgdata):
        """ Processing received public chat message from central server."""
        # insert messages to text box
        message = msgdata['name'] + ": " + msgdata['message']
        app.chatroom_textCons.config(state=tk.NORMAL)
        app.chatroom_textCons.insert(tk.END, message+"\n\n")
        app.chatroom_textCons.config(state=tk.DISABLED)
        app.chatroom_textCons.see(tk.END)
    ## ===========================================================##

    ## ==========implement protocol for text messaging==========##
    def send_chat_message(self, friend, message):
        """ Send a chat message to friend. """
        try:
            peer_info = self.friendlist[friend]
        except KeyError:
            display_noti("Text Messaging Result", 'Friend does not exist!')
        else:
            data = {
                'friend_name': self.name,
                'message': message
            }
            self.client_send(peer_info, msgtype='CHAT_MESSAGE', msgdata=data)

    def recv_message(self, msgdata):
        """ Processing received chat message from peer."""
        friend_name = msgdata['friend_name']
        if friend_name in self.friendlist:
            # insert messages to text box
            message = friend_name + ": " + msgdata['message']
            app.frames[ChatPage].frame_list[friend_name].message_area.config(
                state=tk.NORMAL)
            app.frames[ChatPage].frame_list[friend_name].message_area.insert(
                tk.END, message+"\n\n")
            app.frames[ChatPage].frame_list[friend_name].message_area.config(
                state=tk.DISABLED)
            app.frames[ChatPage].frame_list[friend_name].message_area.see(
                tk.END)
    ## ===========================================================##

    ## ==========implement protocol for file tranfering==========##
    def transfer_file(self, peer, file_path):
        """ Transfer a file to friend. """
        try:
            peer_info = self.friendlist[peer]
        except KeyError:
            display_noti("File Transfer Result", 'Friend does not exist!')
        else:
            file_name = os.path.basename(file_path)
            def fileThread(filename):
                file_sent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                file_sent.connect((peer_info[0], peer_info[1]+OFFSET))

                # send filename and friendname
                fileInfo = {
                    'filename': filename,
                    'friendname': peer,
                }

                fileInfo = json.dumps(fileInfo).encode(FORMAT)
                file_sent.send(fileInfo)
                
                msg = file_sent.recv(BUFFER_SIZE).decode(FORMAT)
                print(msg)

                with open(file_path, "rb") as f:
                    while True:
                        # read the bytes from the file
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        file_sent.sendall(bytes_read)
                file_sent.shutdown(socket.SHUT_WR)
                file_sent.close()
                display_noti("File Transfer Result", 'File has been sent!')
                return
            t_sf = threading.Thread(target=fileThread,args=(file_name,))
            t_sf.daemon = True
            t_sf.start()

    def recv_file_content(self):
        """ Processing received file content from peer."""
        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to our local address
        self.file_socket.bind((self.serverhost, int(self.serverport) + OFFSET))
        self.file_socket.listen(5)

        while True:
            conn, addr = self.file_socket.accept()
            buf = conn.recv(BUFFER_SIZE)
            message = buf.decode(FORMAT)

            # deserialize (json type -> python type)
            recv_file_info = json.loads(message)

            conn.send("Filename received.".encode(FORMAT))
            print(recv_file_info)

            file_name = str(random.randint(1, 100000000))+ "_" + recv_file_info['filename']
            friend_name = recv_file_info['friendname']

            with open(file_name, "wb") as f:
                while True:
                    bytes_read = conn.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)

            conn.shutdown(socket.SHUT_WR)
            conn.close()

            display_noti("File Transfer Result", 'You receive a file with name ' + file_name + ' from ' + friend_name)
    
    ## ===========================================================##
    
    ## ==========implement protocol for log out & exit ===================##

    def send_logout_request(self):
        """ Central Server deletes user out of online user list """
        peer_info = {
            'peername': self.name,
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGOUT', msgdata=peer_info)

    ## ===========================================================##

## ===========================================================##
## ===========================================================##
app = tkinterApp()
app.title('Chat App')
app.geometry("1024x600")
app.resizable(False, False)

def handle_on_closing_event():
    if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
app.mainloop()
