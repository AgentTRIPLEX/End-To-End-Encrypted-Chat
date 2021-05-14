import tkinter
import threading
import messagebox
import network
import encryption
from chat import Chat

CHAT_NAME = "Chat"

class Selector(tkinter.Tk):
    def __init__(self, on_name, title):
        self.on_name = on_name
        super().__init__()
        self.title(title)
        self.resizable(0,0)
        self.draw()

    def draw(self):
        self.config(bg="black")
        name_entry = tkinter.Entry(self, font=("Rockwell", 20), bg="gray", fg="white", insertbackground="white")
        name_entry.pack()
        tkinter.Button(self, text="Submit", bg="black", fg="red", font=("Goudy Stout", 15), width=11, borderwidth=0,
                       activebackground="black", activeforeground="red", command=lambda e=name_entry: self.handle_name(e)).pack()

    def handle_name(self, entry):
        name = entry.get()
        entry.delete(0, "end")
        self.on_name(name)

class App:
    def __init__(self, host, port):
        self._isRunning = False

        try:
            self.client = network.Client(port, host)
        except:
            messagebox.showerror("Server Offline", "The server is offline. Please try again later.")
            return

        if not self.name_window() or not self.code_window():
            return

        self._isRunning = True
        self.win = Chat(lambda m: self.client.send("chat.send", encryption.encrypt(m.encode(), self.encryption_code)))
        self.chat = None

    def name_window(self):
        def on_name(name):
            if not name.strip():
                messagebox.showerror("Empty Name", "The name cannot be empty!")
                return

            if self.client.sendrecv("chat.name.set", name)[0] == "200":
                isRunning["data"] = False
            else:
                messagebox.showerror("Invalid Name", "That name is already being used!")

        win = Selector(on_name, f"{CHAT_NAME} | Name")
        isRunning = {"data": True}

        while isRunning["data"]:
            try:
                win.update()
            except:
                win.quit()
                self.client.send("chat.close")
                self.client.close()
                return False

        win.destroy()
        win.quit()

        return True

    def code_window(self):
        def on_code(code):
            if not code.strip():
                messagebox.showerror("Empty Code", "The code cannot be empty!")
                return
            self.encryption_code, _ = self.client.sendrecv("chat.connect", code)
            isRunning["data"] = False

        win = Selector(on_code, f"{CHAT_NAME} | Code")
        isRunning = {"data": True}

        while isRunning["data"]:
            try:
                win.update()
            except:
                win.quit()
                self.client.send("chat.close")
                self.client.close()
                return False

        win.destroy()
        win.quit()

        return True

    def run(self):
        threading.Thread(target=self.get_transmissions).start()

        while self._isRunning:
            if self.chat is not None:
                self.win.update(self.chat)
                self.chat = None

            try:
                self.win.draw()
            except:
                self.win.quit()
                self._isRunning = False
                self.client.send("chat.close")
                self.client.close()

    def get_transmissions(self):
        while self._isRunning:
            try:
                transmission = self.client.recv()
                threading.Thread(target=self.handle_transmission, args=(transmission,)).start()
            except:
                break

    def handle_transmission(self, transmission):
        content, args = transmission.content, transmission.args

        if content == "chat.update":
            self.chat = [(encryption.decrypt(a, self.encryption_code).decode().title(), t, [encryption.decrypt(m, self.encryption_code).decode() for m in msgs]) for a, t, msgs in args[0]]

if __name__ == "__main__":
    app = App("3.129.61.89", 7615)
    app.run()
