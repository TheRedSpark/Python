import time

print()
#day = 33
#print(type(trigger.tm_min))
day = 33
while True:
    trigger = time.gmtime()
    print(trigger.tm_mday)
    if trigger.tm_min != day:
        day = trigger.tm_min
        print("Tag ist ungleich")
    else:
        print("Tag ist gleich")
        time.sleep(1)
    #print(trigger.tm_min)
    #print(day)
