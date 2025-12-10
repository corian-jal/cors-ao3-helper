# import libraries
import os

# import modules
import ao3interactions as ao3int
import htmlparsing as htp
import datamanipulation as dm

#main program text
os.system('cls') #clear terminal
prompt = input("Hi! Cor's AO3 Helper is now running. For now, you can only run sample testing. Enter y if that's what you would like to do.\n> ") 
#abstract printable options later, instead of adding them all literally
match prompt:
    case 'y':
        sample = ao3int.getMFLSample()
        library = htp.mflPageToFicList(sample)
        name = input('What should I name this file?\n> ')
        filename = './files/' + name + '.csv'
        dm.createArchive(library, filename)
        print("Okay! I'm done, so I'm going to close now.")
    case _:
        print("Sorry, I didn't understand. I'm going to close now.")