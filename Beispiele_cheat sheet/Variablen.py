""""""""""
Integers
"""
x = 6  # this is a Integer

x = x + 1  # add 1
x += 1  # add 1

""""""""""
Float
"""
x = 3.14159265359  # this is a Float

x = x + 1  # add 1
x += 1  # add 1
# round(number,points after fullstop)
round(1923334567124, 4)  # 1923334567124
round(2345.1252342, 4)  # 2345.1252
round(192.67, 4)  # 192.67

"""""""""
Strings
"""
vorname = 'Max'  # Simple String
nachname = "Müller"  # Simple String
vollname = f'Mein Name ist {vorname} {nachname}'  # f-String

"""""""""
Lists
"""

namen = ["Axel", "Max", "Paul", "Tim"]  # this is a List
#          0       1       2      3
namen.pop()  # get the last item from the list and remove it
print(namen[1])  # print Max

"""""""""
Tuple
"""

"""""""""
Conversions
"""

to_int = "4"
to_float = "3.14"  # important you need a fullstop
to_bool = "True"
to_str = False
to_list = "Max"
to_tuple = ["Max", "Müller"]

int(to_int)  # convert to Int
float(to_float)  # convert to Float
bool(to_bool)  # convert to Bool
str(to_str)  # convert to String
list(to_list)  # convert to List
tuple(to_tuple)  # convert to Tuple
print(type())  # Print Type Variables
