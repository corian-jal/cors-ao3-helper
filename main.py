# import libraries
import os

# import modules
import ao3interactions as ao3int
import htmlparsing as htp
import datamanipulation as dm

# callable methods for the main program loop
def dmLoop(archive : dm.pd.DataFrame) -> None:
    # give column options and check if given text is a valid column
    # might want to rethink loop method here (carry over frames v reset?)
    while True:
        prompt = input("Would you like to filter, sort, or go back?\n> ")
        match prompt:
            case 'filter':
                print("Not implemented for now. Sorry.")
            case 'sort':
                #check if it's a sortable col here or in dm? > honestly, you should be able to sort any col you want; ymmv if you choose a weird option.
                col_name = input("Would column would you like to sort on?\n> ")
                asc_val = input("Would you like it in ascending order? y or n\n> ")
                match asc_val:
                    case 'y':
                        asc = True
                    case 'n':
                        asc = False
                    case _:
                        print("[Wrong buzzer noise.] Try again.")
                new_archive = dm.sortBy(archive, col_name, asc)
                dm.printArchive(new_archive,['work_id', 'title', 'author', col_name])
            case 'back':
                print("Alright, sending you back.")
                break
            case _:
                print("Sorry, I don't understand. Try again?")

#main program text
os.system('cls') #clear terminal

options = ["1 - Test HTML [P]arse", "2 - Test [D]ata Manipulation", "3 - [E]xit"]
print("Hi! Cor's AO3 Helper is now running. For now, options are limited for testing. What would you like to do?")

while True:
    # need to add error handling
    for option in options:
        print('  ', option)
    prompt = input("> ")
    match prompt:
        case 'p': # get html, parse, save csv
            sample = ao3int.getMFLSample()
            library = htp.mflPageToFicList(sample)
            archive = dm.createArchive(library)

            name = input('What should I name this file?\n> ')
            filename = './files/' + name + '.csv'
            dm.storeArchive(archive, filename)

            print("Alright, I've exported '", filename, "'. What else would you like to do?")

        case 'd': # test data manipulation
            filename = input("Please give me the name of the csv to load.\n> ")
            archive = dm.loadArchive('./files/' + filename + '.csv')
            print("Successfully loaded archive.")
            dmLoop(archive)

        case 'e': # exit
            print("Understood! I'm closing now, so goodbye.")
            break

        case _: # what?
            print("Sorry, I didn't understand. Please try again?")