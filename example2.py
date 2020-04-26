import sys
import elemento.elemento as el
from colorama import Fore, Style

notion = el.Notion()

f = open("books/The_pirate_Modi.txt","r+")
text = f.readlines()
notion.process_text(text)
print(notion.idees)

questions = []
for idee in notion.idees:
    questions.extend( el.generate_questions( idee ))

print( Fore.RED)
print("QUESTIONS:")
for question in questions:
    print("Question:", question["question"])
    print("Answer:", question["answer"])
    print("\n")
print( Style.RESET_ALL )