import code
import openai

def promptAI():

def runlumina(prompt=''):
  while True:
    print(" -> ", end='')
    aa=input()
    if aa == 'exit':
      raise EOFError()
  
code.interact(banner="LUMINA ONLINE...",exitmsg="LUMINA OFFLINE...", readfunc=runlumina)
