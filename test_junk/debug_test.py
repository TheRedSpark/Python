from pyinstrument import Profiler


x = 5


print(f'Das ist x: {x}')
print(f'Das ist x: {x=}')



profiler = Profiler()
profiler.start()

# code you want to profile

profiler.stop()

profiler.print()