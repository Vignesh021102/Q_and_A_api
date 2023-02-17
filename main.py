import os
import openai
import re


openai.api_key = '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'
start_sequence = "\nA:"
restart_sequence = "\n\nQ: "

# initialStatement = "Please answer rationally for this paragraph with just no,yes or unsure:\n"
initialStatement = "please answer rationally for this paragraph (note that the paragraph contains only partial information so return 0 if the provided information in not enough) and strictly follow the options and return the number of choosen options:\n"
notesFile =  open('note.txt','r') 
notes = notesFile.read()

totalScore = 0
questionsFile = open('questions.txt','r+')
questions = questionsFile.read()

questions = questions.split('Q:')
questionsFile.seek(0)
# print(questions)
newQuestions = [] 

print(f'length {len(questions)-1}')
for i in range(len(questions)):
  questions[i] = questions[i].split('.')[0]
  if questions[i] == '':
      questionsFile.writelines(f"")
      continue
  if(questions[i][0:2] == 'A:' or questions[i][0:3] == '\n\nt' ):continue
  # print(i,questions[i])

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"{initialStatement}{notes}\n\n{questions[i]}\nA:",
    temperature=0,
    max_tokens=1,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
  )
  answer = response['choices'][0]['text']
  print(i,answer)
  totalScore+=  int(answer)

  questionsFile.writelines(f"Q:{questions[i]}.\nA:{answer}\n\n")
questionsFile.writelines(f'\n\ntotal score is {totalScore}')
# print(questions)
# questionsFile.truncate()
notesFile.close()
questionsFile.close()