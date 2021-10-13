import tkinter as tk
import webbrowser
from os import walk
from pathlib import Path
from tkinter import *
from pytube import Search
from pytube import YouTube

'''
Programme qui télécharge les bandes d'annonces de vos films

DEPOSEZ-VOS FILMS DANS LE DOSSIER series-films
'''

# CHANGER DE PATH OU MIGREZ VOS VIDEOS DANS CE DOSSIER
path_film = 'series-films/'
path_trailer = 'trailer/'
downloads_path = (str(Path.home() / "Downloads").replace("\\", "/") + '/')

listeFichiers = []
is_on = True


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.creer_widgets()


    def files_management(self):
        test = self.path_entry.get()
        for (repertoire, sousRepertoires, fichiers) in walk(test):
            listeFichiers.extend(fichiers)
            print(listeFichiers)
            print(self.path_entry.get())

            break
        else:
            print("Le chemin n'existe pas ou n'est pas bien indiqué")
            # Mettre une alerte box


    def download(self):
        for n in range(len(listeFichiers)):
            if not (not ('.mp4' in listeFichiers[n]) and not ('.avi' in listeFichiers[n]) and not (
                    '.mkv' in listeFichiers[n]) and not ('.mov' in listeFichiers[n]) and not (
                    '.webm' in listeFichiers[n]) and not ('.mpeg' in listeFichiers[n])):

                selection = str(listeFichiers[n][0:15])  # Nombre de caractères pris
                s = Search(selection + " Bande d'annonce VF")
                new = str((s.results[0]))

                with open('assets/stats.txt', 'r+') as files:
                    files.write(new + '\n')

                with open('assets/stats.txt', 'r+') as files:
                    ouverture = (files.readline(52).split('Id='))

                    id = (ouverture[+1])

                video = f"https://www.youtube.com/watch?v={id}"

                if is_on:
                    webbrowser.open(f"https://www.youtube.com/watch?v={id}")

                yt = YouTube(video)
                yt.streams \
                    .filter(progressive=True, file_extension='mp4') \
                    .order_by('resolution') \
                    .desc() \
                    .first() \
                    .download(self.path_entry2.get())


    def creer_widgets(self):
        background_image = PhotoImage(file="assets/Trailer2.png")
        self.background = Label(self, image=background_image)
        self.background.photo = background_image
        self.background.place(x=-16, y=0)

        self.my_label = Label(self,
                              text="Ouvrir les bande d'annonce via Youtube",
                              fg="green", bg='white',
                              font=("Arial", 15))

        self.my_label.place(x=200, y=150)

        # Image du switch
        self.on = tk.PhotoImage(file="assets/on.png")
        self.off = tk.PhotoImage(file="assets/off.png")

        # Button switch
        self.on_button = tk.Button(self, image=self.on, bd=0,
                                   command=self.switch, bg='WHITE', activebackground='WHITE')
        self.on_button.place(x=80, y=130)

        # Entry the path
        self.path_entry = tk.Entry(self, width=40)
        self.path_entry.insert(END, path_film)
        self.path_entry.configure(font=('Arial', 15))
        self.path_entry.place(x=100, y=270)

        self.path_entry2 = tk.Entry(self, width=40)
        self.path_entry2.insert(END, path_trailer)
        self.path_entry2.configure(font=('Arial', 15))
        self.path_entry2.place(x=100, y=380)

        # Button Start
        self.Start_image = PhotoImage(file='assets/Button.png')
        self.Button_start = tk.Button(self, command=self.start,
                                      image=self.Start_image, borderwidth=0, bg='WHITE',
                                      activebackground='WHITE')
        self.Button_start.place(x=210, y=450)

    def switch(self):
        global is_on
        # Determine is on or off
        if is_on:
            self.on_button.config(image=self.off)
            self.my_label.config(text="Ne pas ouvrir les bandes d'annonces via Youtube",
                                 fg="grey")
            is_on = False

        else:
            self.on_button.config(image=self.on)
            self.my_label.config(text="Ouvrir les bandes d'annonces via Youtube", fg="green")
            is_on = True


    def start(self):
        self.files_management()
        self.download()



def main():
    app = Application()
    app.title("Trailer Downloader")
    app.geometry('720x630')
    app.resizable(False, False)
    app.iconbitmap('assets/trailer.ico')

    app.mainloop()


# ------------------------------------------------

if __name__ == '__main__':
    main()
