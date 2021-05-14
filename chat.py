import datetime
import tkinter
import tkinter.scrolledtext
import threading

class Chat(tkinter.Tk):
    def __init__(self, on_message):
        super().__init__()
        self.title("Chat")
        self.resizable(0,0)

        self.draw = super().update
        self.on_message = on_message
        self.logs = []

        self.elements = self.create()

    def create(self):
        elements = {}

        elements["console"] = tkinter.scrolledtext.ScrolledText(self, state="disabled", font=("Roboto", 11), width=40, bg="#35393f", fg="white", wrap=tkinter.WORD)
        elements["console"].pack()

        elements["entry"] = tkinter.scrolledtext.ScrolledText(self, height=0, font=("Roboto", 11), fg="white", width=40, bg="#3f444b", insertbackground="white", wrap=tkinter.WORD)
        elements["entry"].pack()

        elements["console"].tag_config("author", font=('Roboto', 11, 'bold'))
        elements["console"].tag_config("time", foreground="grey")
        elements["console"].tag_config("message_separator", font=("Roboto", 6))

        elements["entry"].bind("<Key>", self.KeyPress)

        return elements

    def update(self, chat):
        if chat == self.logs:
            return

        self.elements["console"].config(state='normal')
        self.elements["console"].delete("1.0", "end")

        text = "\n\n".join(["{}  {}\n{}\n".format(a, t, '\n\n'.join(msgs)) for a, t, msgs in chat])
        self.elements["console"].insert("1.0", text)
        self.elements["console"].see("end")

        line = 1.0
        for author, time, contents in chat:
            for content in contents:
                line += content.rstrip().count("\n")

            time = str(time)
            self.elements["console"].tag_add("author", str(line), str(line + float(f"0.{len(author)}")))
            self.elements["console"].tag_add("time", str(line + float(f"0.{len(author) + 2}")), str(line + float(f"0.{len(author) + 2 + len(time)}")))

            for content in contents:
                line += 2 + content.lstrip().count("\n")
                self.elements["console"].tag_add("message_separator", str(line), str(line + 1))

            line += 2

        self.elements["console"].config(state='disabled')
        self.logs = chat

    def KeyPress(self, event):
        message = self.elements["entry"].get(0.0, "end")
        if "shift" not in str(event).lower() and "return" in str(event).lower() and message.strip():
            threading.Thread(target=self.on_message, args=(message.rstrip(),)).start()
            self.elements["entry"].delete('1.0', "end")
            return "break"

    def add_message(self, author, message):
        chat = [[a, b, [d for d in c]] for a,b,c in self.logs]
        time = datetime.datetime.now().time().replace(second=0, microsecond=0)

        if not len(self.logs):
            self.update([[author, time, [message]]])
        else:
            last_message = chat[-1]

            if author == last_message[0] and last_message[1] == time:
                last_message[2].append(message)
                self.update(chat)
            else:
                self.update(self.logs + [[author, time, [message]]])