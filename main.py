# import libraries
import os

# import modules
import ao3interactions as ao3int
import htmlparsing as htp
import datamanipulation as dm

filepath = './files/'

source : str = None
archive : dm.pd.DataFrame = None
dm_options = ["", "1 - [L]oad from CSV", "2 - [S]ave to CSV", "3 - [R]eset to Last Load", "4 - [F]ilter", 
              "5 - S[o]rt", "6 - [C]ount", "7 - L[i]st Columns", "8 - [P]rint", "9 - View [H]all of Fame", 
              "10 - [E]xport to HTML", "11 - Go [B]ack"]

# callable methods for the main program loop
def dmLoop() -> None:
    global source
    global archive
     
    print("You are now in the data manipulation loop. What would you like to do?")

    while True:
        while archive is None:
            filename = input("\nNo archive is currently active. Please give me the name of the csv to load.\n> ")
            source = filepath + filename + '.csv'
            archive = dm.loadArchive(source)
            if archive is None:
                print("Failed to load. Please try again.")
            else:
                print("Successfully loaded archive.")

        for option in dm_options:
            print('  ', option)
        prompt = input("> ")

        match prompt:
            case 'l': #load       
                filename = input("Please give me the name of the csv to load.\n> ")
                source_tmp = filepath + filename + '.csv'
                archive = dm.loadArchive(source_tmp)
                if archive is None:
                    print("Failed to load. Keeping old archive active, unless you deleted the file between then and now.")
                    archive = dm.loadArchive(source)
                    if archive is None:
                        print("...You deleted it, didn't you? Welcome to the 'load a real file or else' loop, loser.")
                else:
                    print("Successfully loaded archive.")
                    source = source_tmp

            case 's': #save
                # ...how do i tell if it actually saved?
                filename = input("What would you like to name this file?\n> ")
                dm.storeArchive(archive, filepath + filename + '.csv')
                print("The archive should be saved now. Please double-check at your desired location.")

            case 'r': #reset
                archive = dm.loadArchive(source)
                print("Successfully reloaded archive. Unless you deleted the file between then and now.")
                if archive is None:
                    print("...You deleted it, didn't you? Welcome to the 'load a real file or else' loop, loser.")

            case 'f': #filter
                col_name = input("What column would you like to filter on?\n> ")
                mode = input("Would you like to filter for an [i]tem or [r]ange? Note that range is only for numerical fields.\n> ")
                match mode:
                    case 'i':
                        try: 
                            val = input("What item would you like to search?\n> ")
                            inc = input("Would you like to include or exclude the item? Enter y for include, n for exclude.\n> ").lower().startswith('y')
                            archive = dm.filterItem(archive, col_name, val, inc)
                        except:
                            print("...Are you sure that was right? Didn't work, though, did it?")
                            continue
                    case 'r':
                        try: 
                            start = int(input("Enter the lower range number, inclusive.\n> "))
                            end = int(input("Enter the higher range number, inclusive.\n> "))
                            archive = dm.filterRange(archive, col_name, start, end)
                        except:
                            print("...You entered a non-numerical value, didn't you? Get out of my class.")
                            continue
                    case _:
                        print("[Wrong buzzer noise.] Try again.")
                        continue
                print("Okay, I found", dm.countRows(archive), "results.")
                dm.printArchive(archive, ['work_id', 'title', 'author', col_name], dm.countRows(archive))

            case 'o': #sort
                #check if it's a sortable col here or in dm? > honestly, you should be able to sort any col you want; ymmv if you choose a weird option.
                col_name = input("Would column would you like to sort on?\n> ")
                asc = input("Would you like it in ascending order? y/n\n> ").lower().startswith('y')
                try: 
                    archive = dm.sortBy(archive, col_name, asc)
                    dm.printArchive(archive, ['work_id', 'title', 'author', col_name], dm.countRows(archive))
                except:
                    print("...Are you sure that was a real column? And that it was a sensible column to sort on?")

            case 'c': #count
                print("Number of entries: ", dm.countRows(archive))

            case 'i': #list cols
                dm.printColumns(archive)

            case 'p': #print archive
                height = int(input("How many rows would you like?\n> "))
                cols = []
                if (input("Would you like columns other than id, title, and author? y/n\n> ").lower().startswith('y')):
                    cols = (input("List each column name separated by a space, with no leading or trailing spaces.\n> ")).split(' ')
                try: 
                    dm.printArchive(archive,['work_id', 'title', 'author'] + cols, height)
                except:
                    print("I couldn't print for some reason? Was that not a real column or something?")

            case 'h': #view hall of fame
                # should i be worried about overwriting and/or errors?
                cat = input("What tag category would you like the results for?\n> ")
                try: 
                    hallofframe = dm.topTags(archive, cat)
                except:
                    print("Sorry, I couldn't grab your hall of fame for some reason. Check your conditions and try again.")
                    continue
                num = int(input("How many rows would you like?\n> "))
                dm.printArchive(hallofframe, ['tag', 'count'], num)
                if (input("Would you like to save to save these results to a file? y/n\n> ").lower().startswith('y')):
                    dm.storeArchive(hallofframe, './files/hallofframe-' + cat + '.csv')

            case 'e': #export html
                filename = input("What would you like to name the file?\n> ")
                with open(filepath + filename + '.html', 'w', encoding='utf-8') as f:
                    f.write(dm.getAllHTML(archive))
                print("Okay, should be exported.")
            
            case 'b': #back
                print("Alright, sending you back.")
                break

            case _: #what?
                print("Sorry, I don't understand. Try again?")

#main program text
os.system('cls') #clear terminal

print("Meowdy! Cor's AO3 Helper is now running. ")
options = ["","1 - Test HTML [P]arse", "2 - Test [D]ata Manipulation", "3 - [E]xit"]

while True:
    print("For the moment, options are limited for testing. What would you like to do?")
    # need to add error handling
    for option in options:
        print('  ', option)
    prompt = input("> ")
    
    match prompt:
        case 'p': # get html, parse, save csv
            if (input("Would you like to use the sample? y/n\n> ").lower().startswith('y')):
                mfl_pgs = [ao3int.getMFLSample()]
            else:
                mfl_pgs = ao3int.getMFL()

            library = []
            num = 1
            for mfl_pg in mfl_pgs:
                print("Parsing page " + str(num) + "...")
                library = library + htp.mflPageToFicList(mfl_pg, num)
                num += 1
            input("All done! Press enter to continue.")
            os.system('cls')
            print(str(len(library)) + " works found.")
            
            archive = dm.createArchive(library)

            filename = input('What should I name this file?\n> ')
            source = filepath + filename + '.csv'
            dm.storeArchive(archive, source)

            print("Alright, I've exported '" + source + "'.")

        case 'd': # test data manipulation
            dmLoop()

        case 'e': # exit
            print("Understood! I'm closing now, so goodbye.")
            break

        case _: # what?
            print("Sorry, I didn't understand. Please try again?")