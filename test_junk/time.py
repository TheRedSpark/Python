import time

trigger = time.gmtime()
x = trigger.tm_mday
#print(x)
#day = 33
day = int(trigger.tm_min)
while True:
    if trigger.tm_mday != day:
        trigger.tm_mday = day
        print("Tag ist ungleich")
    else:
        print("Tag ist gleich")
    time.sleep(10)
