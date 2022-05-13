import time


def feching():
    print("fetching")


schutzsleep = 10
zeit_idle = 10

x = 1

while x == 1:
    zeit = time.strftime("%Y-%m-%d %H:%M:%S")
    trigger = time.gmtime()
    print(f'{trigger.tm_hour}:{trigger.tm_min} Uhr')
    if trigger.tm_min % 15 == 0:
        feching()
        print(f'Jetzt in der Schutzsleepphase von {schutzsleep}s')
        time.sleep(schutzsleep)
    else:
        print(f'Warten auf nächtes Viertel')
    if trigger.tm_min <= 15:
        print("Erstes Virtel")
        zeit_idle = trigger.tm_min %2
    elif trigger.tm_min <= 30 and trigger.tm_min >= 15:
        print("2 Virtel")
        zeit_idle = trigger.tm_min %2
    elif trigger.tm_min <= 45 and trigger.tm_min >= 30:
        print("3 Virtel")
    elif trigger.tm_min <= 59 and trigger.tm_min >= 45:
        print("Letztes Virtel")
    else:
        print("Fehler")
        break
    print(f'{zeit_idle}sekunden ist zeit idle')
    time.sleep(zeit_idle)

"""""""""


"""""""""


