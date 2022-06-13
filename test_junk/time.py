import time

trigger = time.gmtime()
x = trigger.tm_mday
#print(x)
#day = 33
#print(type(trigger.tm_min))
day = int(trigger.tm_min)
while True:
    if trigger.tm_min != day:
        day = trigger.tm_min
        print("Tag ist ungleich")
    else:
        print("Tag ist gleich")
    time.sleep(5)
    print(trigger.tm_min)
    print(day)
