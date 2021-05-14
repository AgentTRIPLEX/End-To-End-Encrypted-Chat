import tkinter
import tkinter.messagebox

def showinfo(title, message):
    window = tkinter.Tk()
    window.withdraw()
    window.attributes('-topmost', 1)
    tkinter.messagebox.showinfo(title, message)
    window.destroy()
    window.quit()

def showerror(title, message):
    window = tkinter.Tk()
    window.withdraw()
    window.attributes('-topmost', 1)
    tkinter.messagebox.showerror(title, message)
    window.destroy()
    window.quit()

def askyesno(title, message):
    window = tkinter.Tk()
    window.withdraw()
    window.attributes('-topmost', 1)
    ans = tkinter.messagebox.askyesno(title, message)
    window.destroy()
    window.quit()
    return ans

def askyesnocancel(title, message):
    window = tkinter.Tk()
    window.withdraw()
    window.attributes('-topmost', 1)
    ans = tkinter.messagebox.askyesnocancel(title, message)
    window.destroy()
    window.quit()
    return ans

def showwarning(title, message):
    window = tkinter.Tk()
    window.withdraw()
    window.attributes('-topmost', 1)
    tkinter.messagebox.showwarning(title, message)
    window.destroy()
    window.quit()