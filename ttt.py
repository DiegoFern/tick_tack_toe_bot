'''
Tic tac Toc bot to telegram player
TODO put AI (for now play by movement)
'''
import numpy as np

class Game:
    '''
    Game class (tic tac toe)
    '''
    SYMBOLS={0:'  ',1:'X',2:'O'}.__getitem__
    def __init__(self):
        self.board=np.zeros([3,3],dtype=np.int8)
        self.player=1
    def isWin(self,player):
        b = (self.board==player)
        return (np.any(b.sum(axis=0)>2) or
                np.any(b.sum(axis=1)>2) or
                (b[[0,1,2],[0,1,2]].sum()>2) or
                (b[[2,1,0],[0,1,2]].sum()>2) )

    def move(self,x,y):
        if self.board[x,y]==0:
            self.board[x,y] = self.player
            if self.isWin(self.player):
                return (1,self.player,)

            else:

                self.player = 3 -self.player#2->1 1->2 change player
                return (0,self.player)
        return (0,-1)
    def draw(self):
        A=''
        for i in self.board:
            #A+=('|--|--|--|\n')
            A+=('|{}|{}|{}|\n'.format(*map(Game.SYMBOLS,i)))
        return A

    def clean(self):
        self.board=0
        self.player=1

import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.
#Init Bot
try:
    token=next(open('token_secret.txt')).strip()
except:
    raise Exception('''Append token_secret.txt file with the token of the application''')

bot = telebot.TeleBot(token)

#Memory system

Memory={}

@bot.message_handler(commands=['newgame']) # Indicamos que lo siguiente va a controlar el comando '/ayuda'
def command_newgame(m): # Definimos una función que resuleva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    Memory[cid]=Game()
    time.sleep(1) #La respuesta del bot tarda 1 segundo en ejecutarse
    bot.send_message(cid, Memory[cid].draw()) # Enviando ...
    bot.send_message(cid,'put /move i j to move')

@bot.message_handler(commands=['move']) #
def command_move(m): #
    A = m.text.split()
    cid = m.chat.id
    print(A)
    try:
        assert A[1].isdigit() and int(A[1]) in (0,1,2)
        assert A[2].isdigit() and int(A[2]) in (0,1,2)
    except:
        pass
        return
    ans=Memory[cid].move(int(A[1]),int(A[2]))
    print(ans)
    if ans[0]==1:
        bot.send_message(cid,Memory[cid].draw()+'\nplayer {} Won'.format(Game.SYMBOLS(Memory[cid].player) ))
        Memory[cid].clean()
    else:
        bot.send_message(cid,Memory[cid].draw())



if __name__ == '__main__':

    bot.polling()
