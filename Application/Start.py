from Game.Battle import Battle
from Game.MyException import MyException
try:
    game = Battle()
except MyException as e:
    print(e)