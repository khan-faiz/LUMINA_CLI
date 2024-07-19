import code
import readline
import json
from openai import OpenAI
from pathlib import Path
APIKEY=""

with open("./apikey", encoding="utf-8") as apikey:
    APIKEY=apikey.read().strip()

client = OpenAI(
    api_key=APIKEY,
)

context = []
context_tokens = []

if Path("context.json").is_file():
  with open("context.json", "r") as jsonfile:
    context = json.loads(jsonfile.read())
    jsonfile.close()
  with open("context_tokens.json", "r") as jsonfile:
    context_tokens = json.loads(jsonfile.read())
    jsonfile.close()

def promptAI(input_text):
  #print("text was: " + input_text)
  msg = {
              "role": "user",
              "content": input_text,
          }

  context.append(msg)
  chat_completion = client.chat.completions.create(
      messages=[

          {
              "role": "user",
              "content": input_text,
          }
      ],
      model="gpt-4o",
  )

  reply_text =  chat_completion.choices[0].message.content

  reply_tokens = chat_completion.usage.completion_tokens
  prompt_tokens = chat_completion.usage.prompt_tokens

  replymsg = {
              "role": "assistant",
              "content": reply_text,
          }
  context.append(replymsg)
  context_tokens.append([prompt_tokens,reply_tokens])
  print(reply_text)

def runlumina(prompt=''):
  while True:
    print(" -> ", end='')
    input_text=input()
    if input_text == 'buffer':
      buffer = []
      print("Buffer opened")
      while True:
        try:
          line = input()
        except EOFError:
            print("Buffer closed")
            break
        buffer.append(line)
      promptAI('\n'.join(buffer))
      continue
    if input_text == 'exit':

      with open("context.json", "w") as jsonfile:
        contextdump = json.dumps(context)
        jsonfile.write(contextdump)
        jsonfile.close()

      with open("context_tokens.json", "w") as jsonfile:
        contextdump = json.dumps(context_tokens)
        jsonfile.write(contextdump)
        jsonfile.close()
      
      raise EOFError()
    if input_text == 'context':
      print(context)
      print(context_tokens)
      continue
    promptAI(input_text)

code.interact(banner="LUMINA ONLINE...",exitmsg="LUMINA OFFLINE...", readfunc=runlumina)
