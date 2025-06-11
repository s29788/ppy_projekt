"""
Moduł zarządzający statystykami i stanem zwierzaka.

Global variables:
    hunger (int): Poziom głodu zwierzaka (0-100).
    fun (int): Poziom nudy zwierzaka (0-100).
    sleep (int): Poziom zmęczenia zwierzaka (0-100).
    state (str): Stan, w którym znajduje się zwierzak ("none", "eating", "playing", "sleeping").
    started (bool): Boolean, którego wartość informuje, czy gra się zaczęła.
    hunger_timer (int): Id timera kontrolującego spadek poziomu głodu.
    fun_timer (int): Id timera kontrolującego spadek poziomu nudy.
    sleep_timer (int): Id timera kontrolującego spadek i wzrost poziomu zmęczenia."""
hunger = 100
fun = 100
sleep = 100

state = "none" # "none", "eating", "playing", "sleeping"
started = False

hunger_timer = None
fun_timer = None
sleep_timer = None

def load_hunger(canvas):
    """
    Wyświetla wartość poziomu głodu zwierzaka na podanym płótnie.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlony jest poziom głodu.
    """
    canvas.create_text(104, 17, text=f"{hunger}", font="Pixeled 8 bold", fill="#B6766A", tags="stat")

def load_fun(canvas):
    """
    Wyświetla wartość poziomu nudy zwierzaka na podanym płótnie.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlony jest poziom nudy.
    """
    canvas.create_text(183, 17, text=f"{fun}", font="Pixeled 8 bold", fill="#B6766A", tags="stat")

def load_sleep(canvas):
    """
    Wyświetla wartość poziomu zmęczenia zwierzaka na podanym płótnie.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlony jest poziom zmęczenia.
    """
    canvas.create_text(278, 17, text=f"{sleep}", font="Pixeled 8 bold", fill="#B6766A", tags="stat")

def load_stats(canvas):
    """
    Wyświetla wszystkie statystyki zwierzaka na podanym płótnie.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlone są statystyki.
    """
    load_hunger(canvas)
    load_fun(canvas)
    load_sleep(canvas)

def update_stats(canvas):
    """Funkcja aktualizująca statystyki zwierzaka.

    Funkcja usuwa wszystkie statystyki na podanym płótnie, po czym wyświetla na nim aktualne statystyki.

    Args:
        canvas (tk.Canvas): Płótno, na którym wyświetlone są zaktualizowane statystyki.
    """
    canvas.delete("stat")
    load_stats(canvas)

def restart_stats():
    """
    Zmienia wartości poziomu głodu, nudy i zmęczenia zwierzaka na początkowe (100), a zmiennej globalnej "started" przypisuje wartość "False".
    """
    global hunger, fun, sleep, started
    hunger = 100
    fun = 100
    sleep = 100
    started = False

def decrease_hunger(window, canvas):
    """Funkcja do cykliczngo odniżania poziomu głodu zwierzaka.

    Funkcja co 45 sekund wywołuje zdefiniowaną wewnątrz funkcję "decrease()".
    Funkcja wewnętrzna "decrease()" rekurencyjnie, co 45 sekund, jeśli wartość poziomu głodu jest niemniejsza od 5 i stan zwierzaka jest różny od "eating", obniża wartość poziomu głodu o 5 i aktualizuje statystyki na podanym płótnie.

    Args:
        window (tk.Tk): Główne okno aplikacji, na którym wywoływana jest metoda after().
        canvas (tk.Canvas): Płótno, na którym aktualizowane są statystyki.
    """
    global hunger_timer
    def decrease():
        global hunger, hunger_timer
        if hunger >= 5 and not state == "eating":
            hunger -= 5
            update_stats(canvas)
        hunger_timer = window.after(45000, decrease)
    hunger_timer = window.after(45000, decrease)

def decrease_fun(window, canvas):
    """Funkcja do cykliczngo odniżania poziomu nudy zwierzaka.

    Funkcja wewnętrzna "decrease()" rekurencyjnie, co 64 sekundy, jeśli wartość poziomu nudy jest niemniejsza od 5 i stan zwierzaka jest różny od "playing", obniża wartość poziomu nudy o 5 i aktualizuje statystyki na podanym płótnie.

    Args:
        window (tk.Tk): Główne okno aplikacji, na którym wywoływana jest metoda after().
        canvas (tk.Canvas): Płótno, na którym aktualizowane są statystyki.
    """
    global fun_timer
    def decrease():
        global fun, fun_timer
        if fun >= 5 and not state == "playing":
            fun -= 5
            update_stats(canvas)
        fun_timer = window.after(64000, decrease)
    fun_timer = window.after(64000, decrease)

def decrease_sleep(window, canvas):
    """Funkcja do cykliczngo odniżania poziomu zmęczenia zwierzaka.

    Funkcja wewnętrzna "decrease()" rekurencyjnie, co 90 sekund, jeśli wartość poziomu zmęczenia jest niemniejsza od 5 i stan zwierzaka jest różny od "sleeping", obniża wartość poziomu zmęczenia o 5 i aktualizuje statystyki na podanym płótnie.

    Args:
        window (tk.Tk): Główne okno aplikacji, na którym wywoływana jest metoda after().
        canvas (tk.Canvas): Płótno, na którym aktualizowane są statystyki.
    """
    global sleep_timer
    def decrease():
        global sleep, sleep_timer
        if sleep >= 5 and not state == "sleeping":
            sleep -= 5
            update_stats(canvas)
        sleep_timer = window.after(90000, decrease)
    sleep_timer = window.after(90000, decrease)

def start_decrease(window, canvas):
    """
    Uruchamia funkcje, które zaczynają obniżać poziom głodu, nudy i zmęczenia zwierzaka.

    Args:
        window (tk.Tk): Główne okno aplikacji, przekazane jako argument w funkcjach obniżających statystyki.
        canvas (tk.Canvas): Płótno przekazane jako argument w funkcjach obniżających statystyki.
    """
    global started
    if not started:
        started = True
        decrease_hunger(window, canvas)
        decrease_fun(window, canvas)
        decrease_sleep(window, canvas)

def increase_hunger(canvas):
    """Funkcja zwiększająca poziom głodu zwierzaka.

    Jeśli stan zwierzaka ma wartość "eating", funkcja podnosi poziom głodu zwierzaka w zależności od jego aktualnej wartości, po czym aktualizuje statystyki na podanym płótnie.

    Args:
        canvas (tk.Canvas): Płótno, na którym aktualizowane są statystyki.
    """
    if state == "eating":
        global hunger
        if hunger <= 75:
            hunger += 25
        else:
            hunger = 100
        update_stats(canvas)

def increase_fun(canvas):
    """Funkcja zwiększająca poziom nudy zwierzaka.

    Jeśli stan zwierzaka ma wartość "playing", funkcja podnosi poziom nudy zwierzaka w zależności od jego aktualnej wartości, po czym aktualizuje statystyki na podanym płótnie.

    Args:
        canvas (tk.Canvas): Płótno, na którym aktualizowane są statystyki.
    """
    if state == "playing":
        global fun
        if fun <= 80:
            fun += 20
        else:
            fun = 100
        update_stats(canvas)

def increase_sleep(window, canvas):
    """Funkcja do cykliczngo zwiększania poziomu zmęczenia zwierzaka.

    Funkcja wewnętrzna "increase()", rekurencyjnie, co 16 sekund, jeśli stan zwierzaka ma wartość "sleeping" i wartość poziomu zmęczenia jest niewiększa od 95, zwiększa wartość poziomu zmęczenia o 5 i aktualizuje statystyki na podanym płótnie.

    Args:
        window (tk.Tk): Główne okno aplikacji, na którym wywoływana jest metoda after().
        canvas (tk.Canvas): Płótno, na którym aktualizowane są statystyki.
    """
    global sleep_timer
    if state == "sleeping":
        def increase():
            global sleep, sleep_timer
            if sleep <= 95 and state == "sleeping":
                sleep += 5
                update_stats(canvas)
            sleep_timer = window.after(16000, increase)
        sleep_timer = window.after(16000, increase)

def cancel_timers(window):
    """Funkcja do anulowania timerów.

    Funkcja anuluje wszystkie timery, przechowywane w zmiennych globalnych "hunger_timer", "fun_timer" i "sleep_timer", podanego okna, po czym każdemu z nich przypisuje wartość "None".

    Args:
        window (tk.Tk): Główne okno aplikacji, na którym wywoływana jest metoda after_cancel().
    """
    global hunger_timer, fun_timer, sleep_timer
    for timer in (hunger_timer, fun_timer, sleep_timer):
        if timer:
            window.after_cancel(timer)
    hunger_timer = None
    fun_timer = None
    sleep_timer = None

def set_state(s):
    """
    Zmienia stan zwierzaka.

    Args:
        s (str): Stan, jaki przyjmuje zwierzak.
    """
    global state
    state = s