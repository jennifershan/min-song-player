import time
import curses
import threading
import random

def countdown():
    for time_left in range(600, 0, -1):
        timer_window.addstr(0, 0, str(time_left) + "\n")
        timer_window.refresh()
        time.sleep(1)
    timer_window.addstr(0, 0, "0" + "\n")
    timer_window.refresh()
    input_window.clear()
    input_window.addstr('Your score is ' + str(score) + '. \n(Press enter to exit.)')
    input_window.refresh()

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)

if curses.has_colors():
    curses.start_color()

curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
stdscr.addstr("Time left:", curses.A_REVERSE)
stdscr.chgat(-1, curses.A_REVERSE)
stdscr.noutrefresh()

timer_window = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)
timer_window.noutrefresh()

input_window = curses.newwin(curses.LINES, curses.COLS, 3, 0)
input_window.bkgd(curses.color_pair(1))
input_window.addstr("Press enter to start.")
input_window.noutrefresh()

curses.doupdate()

countdown_thread = threading.Thread(target = countdown)
countdown_thread.start()

score = 0

sequences = []
file = open("sequences.txt", "r")
lines = file.readlines()
total_lines = len(lines)

user_answer = ""
prev_answer = ""
while countdown_thread.is_alive():
    key = input_window.getch()
    if key == 10:
        sequence = -1
        while True:
            if sequence == -1 or sequence in sequences:
                sequence = random.randint(0, total_lines - 1)
            else:
                break
        sequences.append(sequence)
        
        question = lines[sequence].rsplit(',',1)[0].replace(" ", "")
        
        input_window.clear()
        input_window.addstr(question + ', __: ')
        
        if user_answer == "":
            pass
        elif user_answer == prev_answer:
            score += 1
        else:
            score -= 1

        user_answer = ""
        prev_answer = lines[sequence].split('=')[-1].replace("\n", "")
    elif key == 127:
        curs_pos = input_window.getyx()
        input_window.addstr(curs_pos[0], curs_pos[1] - 1, " ")
        input_window.move(curs_pos[0], curs_pos[1] - 1)
        user_answer = user_answer[:-1]
    else:
        input_window.addstr(chr(key))
        user_answer += chr(key)

curses.echo()
curses.nocbreak()
stdscr.keypad(False)
curses.endwin()