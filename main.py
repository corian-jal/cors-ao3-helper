# import libraries
import os

# import modules
import ao3interactions as ao3int
import htmlparsing as htp
import datamanipulation as dm

source : str = None
archive : dm.pd.DataFrame = None
dm_options = ["1 - [L]oad from CSV", "2 - [S]ave to CSV", "3 - [R]eset to Last Load", "4 - [F]ilter", 
              "5 - S[o]rt", "6 - [C]ount", "7 - L[i]st Columns", "8 - [P]rint", "9 - View [H]all of Fame", 
              "10 - Go [B]ack"]

# callable methods for the main program loop
def dmLoop() -> None:
    global source
    global archive

    if archive is None:
        filename = input("No archive is currently active. Please give me the name of the csv to load.\n> ")
        source = './files/' + filename + '.csv'
        archive = dm.loadArchive(source)
        print("Successfully loaded archive.")
    print("You are now in the data manipulation loop. What would you like to do?")

    while True:
        for option in dm_options:
            print('  ', option)
        prompt = input("> ")

        match prompt:
            case 'l': #load       
                filename = input("Please give me the name of the csv to load.\n> ")
                source = './files/' + filename + '.csv'
                archive = dm.loadArchive(source)
                print("Successfully loaded archive.")

            case 's': #save
                filename = input("What would you like to name this file?\n> ")
                dm.storeArchive(archive, './files/' + filename + '.csv')
                print("Successfully saved archive.")

            case 'r': #reset
                archive = dm.loadArchive(source)
                print("Successfully reloaded archive.")

            case 'f': #filter
                col_name = input("What column would you like to filter on?\n> ")
                mode = input("Would you like to filter for an [i]tem or [r]ange?\n> ")
                # should i check for valid? or another ymmv if you do something weird
                match mode:
                    case 'i':
                        val = input("What item would you like to search?\n> ")
                        inc = input("Would you like to include or exclude the item? Enter y for include, n for exclude.\n> ").lower().startswith('y')
                        archive = dm.filterItem(archive, col_name, val, inc)
                    case 'r':
                        start = int(input("Enter the lower range number, inclusive.\n> "))
                        end = int(input("Enter the higher range number, inclusive.\n> "))
                        archive = dm.filterRange(archive, col_name, start, end)
                    case _:
                        print("[Wrong buzzer noise.] Try again.")
                print("Okay, found", dm.countRows(archive), "results.")
                dm.printArchive(archive, ['work_id', 'title', 'author', col_name], dm.countRows(archive))

            case 'o': #sort
                #check if it's a sortable col here or in dm? > honestly, you should be able to sort any col you want; ymmv if you choose a weird option.
                col_name = input("Would column would you like to sort on?\n> ")
                asc = input("Would you like it in ascending order? y/n\n> ").lower().startswith('y')
                archive = dm.sortBy(archive, col_name, asc)
                dm.printArchive(archive, ['work_id', 'title', 'author', col_name], dm.countRows(archive))

            case 'c': #count
                print("Number of entries: ", dm.countRows(archive))

            case 'i': #list cols
                dm.printColumns(archive)

            case 'p': #print archive
                height = int(input("How many rows would you like?\n> "))
                cols = []
                if (input("Would you like columns other than id, title, and author? y/n\n> ").lower().startswith('y')):
                    cols = (input("List each column name separated by a space, with no leading or trailing spaces.\n> ")).split(' ')
                dm.printArchive(archive,['work_id', 'title', 'author'] + cols, height)

            case 'h': #view hall of fame
                # should i be worried about overwriting and/or errors?
                cat = input("What tag category would you like the results for?\n> ")
                hallofframe = dm.topTags(archive, cat)
                num = int(input("How many rows would you like?\n> "))
                dm.printArchive(hallofframe, ['tag', 'count'], num)
                if (input("Would you like to save to save these results to a file? y/n\n> ").lower().startswith('y')):
                    dm.storeArchive(hallofframe, './files/hallofframe-' + cat + '.csv')

            case 'b': #back
                print("Alright, sending you back.")
                break

            case _: #what?
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
            mfl_pg1 = ao3int.getMFL()
            library = htp.mflPageToFicList(mfl_pg1)
            archive = dm.createArchive(library)

            filename = input('What should I name this file?\n> ')
            source = './files/' + filename + '.csv'
            dm.storeArchive(archive, source)

            print("Alright, I've exported '" + source + "'. What else would you like to do?")

        case 'd': # test data manipulation
            dmLoop()

        case 'e': # exit
            print("Understood! I'm closing now, so goodbye.")
            break

        case _: # what?
            print("Sorry, I didn't understand. Please try again?")