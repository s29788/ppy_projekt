"""
Moduł zarządzający główną logiką i interfejsem aplikacji.

Global variables:
    pets (list[str]): Lista z nazwami plików obrazów dostępnych zwierzaków.
    selected_pet_index (int): Index aktualnie wyświetlanego zwierzaka z listy "pets".
    mode (str): Tryb gry. ("select", "game")"""
import tkinter as tk
from PIL import Image, ImageTk

import pet

pets = ["assets/pillbug.png", "assets/beetle1.png", "assets/beetle2.png", "assets/cicada.png"]

selected_pet_index = 0

mode = "select" # "select", "game"

def load_asset(canvas, bg, asset, x=0, y=0):
    """
    Wkleja podany asset na podane tło i wyświetla go na podanym płótnie.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlany jest obraz.
        bg (Image.Image): Tło, do którego doklejany jest asset.
        asset (Image.Image): Element doklejany do tła.
        x (int): Opcjonalna wartość, o jaką asset jest przesuwany w prawo.
        y (int): Opcjonalna wartość, o jaką asset jest przesuwany w górę.
    """
    h, w = asset.size
    bg.paste(im=asset, box=(int(215-w/2)+x, int(220-h/2)-1+y), mask=asset)
    image = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=image, anchor=tk.NW)
    canvas.image = image

def load_pet(canvas, bg_file, pet_index, x=0, y=0):
    """Funkcja do wyświetlania podanego zwierzaka.

    Usuwa wszystkie elementy z płótna, po czym wyświetla, na podanym płótnie, obraz zwierzaka o podanym indeksie na podanym tle.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlany jest obraz.
        bg_file (str): Nazwa pliku, który jest tłem, do którego doklejany jest obraz zwierzaka.
        pet_index (int): Index zwierzaka z listy "pets", który ma zostać wyświetlony.
        x (int): Opcjonalna wartość, o jaką obraz zwierzaka jest przesuwany w prawo.
        y (int): Opcjonalna wartość, o jaką obraz zwierzaka jest przesuwany w górę.
    """
    canvas.delete("all")
    bg = Image.open(bg_file).convert("RGBA")
    pet = Image.open(pets[pet_index]).convert("RGBA")
    load_asset(canvas, bg, pet, x, y)

def animate_pet(window, canvas, bg_file, pet_index):
    """Funckja do animacji obrazu zwierzaka.

    Funkcja wewnętrzna "pet_animation()" rekurencyjnie, co sekundę, jeśli zmienna globalna "mode" ma wartość "game" i stan zwierzaka "pet.state" ma wartość "none", wyświetla na podanym płótnie obraz zwierzaka o podanym indeksie,
    zmieniając jego pozycję przy każdym wywołaniu, na zmianę przesuwając go w górę i w dół.

    Args:
        window (tk.Tk): Główne okno aplikacji, na którym wywoływana jest metoda after().
        canvas (tk.Canvas): Płótno, na którym wyświetlana jest animacja.
        bg_file (str): Nazwa pliku, który jest tłem, na którym wyświetlana jest animacja.
        pet_index (int): Index zwierzaka z listy "pets", który ma zostać wyświetlony.
    """
    if mode == "game" and pet.state == "none":
        _canvas_image = canvas.image
        def pet_animation(x):
            if mode == "game" and pet.state == "none":
                canvas.delete("all")
                canvas.image = _canvas_image
                if x % 2 == 0:
                    load_pet(canvas, bg_file, pet_index)
                else:
                    load_pet(canvas, bg_file, pet_index, 0, 2)
                pet.load_stats(canvas)
                x += 1
                window.after(1000, lambda: pet_animation(x))
        window.after(0, lambda: pet_animation(0))

def on_click_right(canvas):
    """
    Zmienia obraz zwierzaka na podanym płótnie na następnego zwierzaka, jeśli taki jest, z listy zwierzaków do wyboru.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlany jest zwierzak do wyboru.
    """
    global selected_pet_index
    if selected_pet_index < 3:
        selected_pet_index += 1
        load_pet(canvas, "assets/select_bg.png", selected_pet_index)

def on_click_left(canvas):
    """
    Zmienia obraz zwierzaka na podanym płótnie na poprzedniego zwierzaka, jeśli taki jest, z listy zwierzaków do wyboru.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlany jest zwierzak do wyboru.
    """
    global selected_pet_index
    if selected_pet_index > 0:
        selected_pet_index -= 1
        load_pet(canvas, "assets/select_bg.png", selected_pet_index)

def on_enter(event, window, canvas):
    """Funkcja obsługująca wciśnięcie klawisza Enter w trybie wyboru zwierzaka.

    Realizuje przejście z trybu wyboru zwierzaka do trybu gry.

    Args:
        event: Obiekt zdarzenia przekazany przez tkinter.
        window (tk.Tk): Główne okno aplikacji, przekazane jako argument w funkcji update().
        canvas (tk.Canvas): Płótno przekazane jako argument w funkcji update().
    """
    global mode
    if mode == "select":
        mode = "game"
    update(window, canvas)

def select(window, canvas):
    """Funkcja realizująca tryb wyboru zwierzaka.

    Funkcja ustawia zmienną globalną "selected_pet_index" na 0, anuluje wszystkie istniejące timery, restartuje statystyki zwierzaka i ustawia stan zwierzaka "pet.state" na "none".
    Funkcja usuwa wszystkie widgety z podanego okna, oprócz obiektów klasy tk.Canvas i załadowuje na podanym płótnie pierwszego zwierzaka z listy zwierzaków do wyboru.
    Funkcja tworzy i umieszcza na podanym oknie przyciski odpowiadające za poruszanie się po dostępnych zwierzakach i dodaje do okna obsługę wciśnięcia klawisza Enter w tym trybie.

    Args:
        window (tk.Tk): Główne okno aplikacji.
        canvas (tk.Canvas): Płótno, na którym wyświetlane są grafiki gry.
    """
    global selected_pet_index
    selected_pet_index = 0

    pet.cancel_timers(window)
    pet.restart_stats()
    pet.set_state("none")

    for widget in window.winfo_children():
        if not isinstance(widget, tk.Canvas):
            widget.destroy()

    load_pet(canvas, "assets/select_bg.png", selected_pet_index)
    canvas.pack()

    button_right = tk.Button(window, width=9, text=">>", fg="#0d0b00", bg="#e3e2e1", bd=1, command=lambda: on_click_right(canvas))
    button_right.place(x=300, y=380)
    button_left = tk.Button(window, width=9, text="<<", fg="#0d0b00", bg="#e3e2e1", bd=1, command=lambda: on_click_left(canvas))
    button_left.place(x=60, y=380)

    window.bind("<Return>", lambda e: on_enter(e, window, canvas))

def feed(window, canvas):
    """Funkcja realizująca karmienie zwierzaka.

    Jeśli zwierzak jest w stanie "eating", funkcja wewnętrzna "feed_animation()" wyświetla po kolei serię grafik imitujących zjadane jedzenie, z odstępem 1 sekundy,
    po czym zwiększa poziom głodu, ustawia stan zwierzaka na "none" i aktualizuje interface gry.

    Args:
        window (tk.Tk): Główne okno aplikacji.
        canvas (tk.Canvas): Płótno, na którym wyświetlane są grafiki gry.
    """
    if pet.state == "eating":
        _canvas_image = canvas.image

        def feed_animation(x):
            if pet.state == "eating":
                canvas.delete("all")
                canvas.image = _canvas_image
                bg = ImageTk.getimage(canvas.image).convert("RGBA")
                if x >= 3:
                    load_pet(canvas, "assets/game_bg.png", selected_pet_index)
                    pet.increase_hunger(canvas)
                    pet.set_state("none")
                    update(window, canvas)
                    return
                if x == 0:
                    food = Image.open("assets/food1.png").convert("RGBA")
                elif x == 1:
                    food = Image.open("assets/food2.png").convert("RGBA")
                else:
                    food = Image.open("assets/food3.png").convert("RGBA")
                load_asset(canvas, bg, food)
                pet.load_stats(canvas)
                x += 1
                window.after(1000, lambda: feed_animation(x))

        feed_animation(0)

def play(window, canvas):
    """Funkcja realizująca zabawę ze zwierzakiem.

    Jeśli zwierzak jest w stanie "playing", funkcja wewnętrzna "play_animation()", 2 razy, co sekundę, wyświetla na zmianę 2 grafiki,
    po czym zwiększa poziom nudy, ustawia stan zwierzaka na "none" i aktualizuje interface gry.

    Args:
        window (tk.Tk): Główne okno aplikacji.
        canvas (tk.Canvas): Płótno, na którym wyświetlane są grafiki gry.
    """
    if pet.state == "playing":
        _canvas_image = canvas.image

        def play_animation(x):
            if pet.state == "playing":
                if x >= 4:
                    load_pet(canvas, "assets/game_bg.png", selected_pet_index)
                    pet.increase_fun(canvas)
                    pet.set_state("none")
                    update(window, canvas)
                    return
                canvas.delete("all")
                canvas.image = _canvas_image
                bg = ImageTk.getimage(canvas.image).convert("RGBA")
                if x % 2 == 0:
                    star = Image.open("assets/star1.png").convert("RGBA")
                else:
                    star = Image.open("assets/star2.png").convert("RGBA")
                load_asset(canvas, bg, star)
                pet.load_stats(canvas)
                x += 1
                window.after(1000, lambda: play_animation(x))

        play_animation(0)

def sleep(window, canvas):
    """Funkcja realizująca zasypianie zwierzaka.

    Jeśli zwierzak jest w stanie "sleeping", funkcja wewnętrzna "sleep_animation()", rekurencyjnie, co sekundę, wyświetla na zmianę 2 grafiki imitujące sen.

    Args:
        window (tk.Tk): Główne okno aplikacji.
        canvas (tk.Canvas): Płótno, na którym wyświetlane są grafiki gry.
    """
    if pet.state == "sleeping":
        _canvas_image = canvas.image
        def sleep_animation(x):
            if pet.state == "sleeping":
                canvas.delete("all")
                canvas.image = _canvas_image
                bg = ImageTk.getimage(canvas.image).convert("RGBA")
                if x % 2 == 0:
                    z = Image.open("assets/z1.png").convert("RGBA")
                else:
                    z = Image.open("assets/z2.png").convert("RGBA")
                load_asset(canvas, bg, z)
                pet.load_stats(canvas)
                x += 1
                window.after(1000, lambda: sleep_animation(x))
        window.after(0, lambda: sleep_animation(0))

def on_feed(window, canvas):
    """
    Jeśli stan zwierzaka jest inny niż "eating", zmienia wartość zmiennej "pet.state" na "eating", i aktualizuje interface gry.

    Args:
        window (tk.Tk): Główne okno aplikacji, przekazane jako argument w funkcji update().
        canvas (tk.Canvas): Płótno przekazane jako argument w funkcji update().
    """
    if not pet.state == "eating":
        pet.set_state("eating")
        update(window, canvas)

def on_play(window, canvas):
    """
    Jeśli stan zwierzaka jest inny niż "playing", zmienia wartość zmiennej "pet.state" na "playing", i aktualizuje interface gry.

    Args:
        window (tk.Tk): Główne okno aplikacji, przekazane jako argument w funkcji update().
        canvas (tk.Canvas): Płótno przekazane jako argument w funkcji update().
    """
    if not pet.state == "playing":
        pet.set_state("playing")
        update(window, canvas)

def on_sleep(window, canvas):
    """
    Jeśli stan zwierzaka jest "sleeping" zmienia wartość zmiennej "pet.state" na "none", w przeciwnym wypadku, zmienia jej wartość na "sleeping", i aktualizuje interface gry.

    Args:
        window (tk.Tk): Główne okno aplikacji, przekazane jako argument w funkcji update().
        canvas (tk.Canvas): Płótno przekazane jako argument w funkcji update().
    """
    if pet.state == "sleeping":
        pet.set_state("none")
    else:
        pet.set_state("sleeping")
    update(window, canvas)

def on_change_pet(window, canvas):
    """
    Realizuje przejście z trybu gry do trybu wyboru zwierzaka.

    Args:
        window (tk.Tk): Główne okno aplikacji, przekazane jako argument w funkcji update().
        canvas (tk.Canvas): Płótno przekazane jako argument w funkcji update().
    """
    global mode
    mode = "select"
    pet.set_state("none")
    update(window, canvas)

def game(window, canvas):
    """Funkcja realizująca tryb gry.

    Funkcja usuwa wszystkie widgety z podanego okna, oprócz obiektów klasy tk.Canvas i załadowuje na podane płótno wybranego zwierzaka.
    Funkcja tworzy i umieszcza na podanym oknie przyciski odpowiadające za karmienie, zabawę, sen oraz zmianę zwierzaka.
    Wyświetla na podanym płótnie statystyki zwierzaka i uruchamia jego animację, po czym zaczyna obniżać statystki zwierzaka.
    Jeśli zmienna globalna "pet.state" ma wartość "eating", funkcja realizuje karmienie, jeśli "playing", realizuje zabawę, jeśli "sleeping", realizuje sen i zaczyna zwiększać poziom zmęczenia.

    Args:
        window (tk.Tk): Główne okno aplikacji.
        canvas (tk.Canvas): Płótno, na którym wyświetlane są grafiki gry.
    """
    for widget in window.winfo_children():
        if not isinstance(widget, tk.Canvas):
            widget.destroy()

    load_pet(canvas, "assets/game_bg.png", selected_pet_index)

    feed_button = tk.Button(window, width=9, text="feed", fg="#0d0b00", bg="#e3e2e1", bd=1, command=lambda: on_feed(window, canvas))
    feed_button.place(x=38, y=394)
    play_button = tk.Button(window, width=9, text="play", fg="#0d0b00", bg="#e3e2e1", bd=1, command=lambda: on_play(window, canvas))
    play_button.place(x=127, y=394)
    sleep_button = tk.Button(window, width=9, text="sleep", fg="#0d0b00", bg="#e3e2e1", bd=1, command=lambda: on_sleep(window, canvas))
    sleep_button.place(x=216, y=394)
    change_button = tk.Button(window, width=11, text="change pet", fg="#0d0b00", bg="#e3e2e1", bd=1, command=lambda: on_change_pet(window, canvas))
    change_button.place(x=309, y=394)

    pet.load_stats(canvas)
    animate_pet(window, canvas, "assets/game_bg.png", selected_pet_index)

    pet.start_decrease(window, canvas)

    if pet.state == "eating":
        feed(window, canvas)

    if pet.state == "playing":
        play(window, canvas)

    if pet.state == "sleeping":
        sleep(window, canvas)
        pet.increase_sleep(window, canvas)

    canvas.pack()

def update(window, canvas):
    """Funkcja aktualizująca interface aplikacji w zależności od trybu gry.

    Jeśli zmienna globalna "mode" ma wartość "select", funkcja realizuje tryb wyboru zwierzaka, jeśli ma wartość "game", realizuje tryb gry.

    Args:
        window (tk.Tk): Główne okno aplikacji, przekazane jako argument w funkcjach select() i game().
        canvas (tk.Canvas): Płótno przekazane jako argument w funkcjach select() i game().
    """
    if mode == "select":
        select(window, canvas)
    if mode == "game":
        game(window, canvas)

def main():
    """
    Tworzy główne okno aplikacji, ustawia jego tytuł, rozmiar i właściwości, tworzy płótno, po czym uruchamia główną pętlę programu.
    """
    window = tk.Tk()
    window.geometry("430x440")
    window.resizable(False, False)

    canvas = tk.Canvas(window, width=430, height=440)

    window.after(0, lambda: update(window, canvas))
    window.mainloop()

if __name__ == "__main__":
    main()