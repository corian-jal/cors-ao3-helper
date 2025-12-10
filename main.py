# import libraries
import os

# import modules
import ao3interactions as ao3int
import htmlparsing as htp
import datamanipulation as dm

#main program text
os.system('cls') #clear terminal

options = ["[1] Sample Testing", "[2] Exit"]
print("Hi! Cor's AO3 Helper is now running. For now, you can only run sample testing. What would you like to do?")

while True:
    for option in options:
        print('   ', option)
    prompt = input("> ")
    match prompt:
        case '1':
            sample = ao3int.getMFLSample()
            library = htp.mflPageToFicList(sample)
            name = input('What should I name this file?\n> ')
            filename = './files/' + name + '.csv'
            dm.createArchive(library, filename)
            print("Alright, I've exported '", filename, "'. What else would you like to do?")
        case '2':
            print("Understood! I'm closing now, so goodbye.")
            break
        case _:
            print("Sorry, I didn't understand. Please try again?")