from pyinstrument import Profiler
import time
profiler = Profiler()
profiler.start()

x = 5


print(f'Das ist x: {x}')
print(f'Das ist x: {x=}')


time.sleep(5)


# code you want to profile

profiler.stop()

profiler.print()