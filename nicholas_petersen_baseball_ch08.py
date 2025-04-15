#! usr/bin/env python3

#import read and write functions from module
import fileio

FILENAME = "baseball.csv"

POSITIONS = ("1B", "2B", "3B", "P", "C", "SS", "LF", "CF", "RF")

def display_separator():
    print("========================================================================")

def display_title():
    print("Baseball Team Manager\n" )

def display_menu(positions):
    print("MENU OPTIONS\n",
          "1 - Display Lineup\n",
          "2 - Add Player\n",
          "3 - Remove Player\n",
          "4 - Move Player\n",
          "5 - Edit Player Position\n",
          "6 - Edit Player Stats\n",
          "7 - Exit Program\n")
    print()
    print("POSITIONS")
    print(*POSITIONS, sep=" | ")

def validate_avg(at_bat, hits): 
    if at_bat >= hits and at_bat >0 and hits >=0:
        return at_bat, hits                                                             #returns at _bat and hits to the main function variables if passes validation
        
    else:                                                                                      #else if validation fails....
        while True:
            while at_bat < 0:                                                            # check eto ensure times at bat is not negative
                print("You cannot have less than zero times at bat. Please try again...\n")
                at_bat =int(input("Official number of at bats: "))      #get times at bat from the user if it is
                
            while hits < 0:                                                                 #check to ensure hits is not less than 1
                print("You cannot have less than zero hits. Please try again...\n")
                hits =int(input("Number of hits: "))                            #get number of hits from the user if it is
                
            if at_bat < hits:                                                              # check to ensure there are not more hits than times a bat
                print("Your entry was invalid. Times at bat must be greater than or equal to hits. Please try again...\n")
                at_bat =int(input("Official number of at bats: "))         #get times at bat from the user
                hits = int(input("Number of hits: "))                              #get number of hits from the user
            else:
                break
                
        return at_bat, hits

def validate_pos(position):
    while True:
       validatePos = POSITIONS.count(position)
       if validatePos == 0:
           position = input("Position not valid. Please choose from the list above: ")
       else:
            break
    return position

def showLineup():
    list_data = fileio.read_file(FILENAME)                              #read list from file and asign to list_data
    print("LINEUP")
    print("   Player\t\t\tPosition\tAt bats\tHits\tAverage")
    print("-------------------------------------------------------------------------------------------------------------------")
    for i, list_data in enumerate(list_data, start=1):
        if len(list_data[0]) > 25:                                                  #check name length and truncate if too long to fit in column
            print(f"{i}. {list_data[0][0:22]}...\t{list_data[1]}\t{list_data[2]}\t{list_data[3]}\t{list_data[4]}")
        else:                                                                                 #otherwise print full name up to 25 characters
            print(f"{i}. {list_data[0].ljust(25, " ")}\t{list_data[1]}\t{list_data[2]}\t{list_data[3]}\t{list_data[4]}")
    print()


def addPlayer(list_data):
        try:                                                                                        #add error handling for invalid user inputs
            name = input("Enter player name: ")
            if any(char.isdigit() for char in name) == True:
                raise UserWarning("Player Name cannot contain numbers. Add operation cancelled.\n")
            position = input("Enter their position: ").upper()
            position = validate_pos(position)    
            at_bat =int(input("Official number of at bats: "))                 
            hits = int(input("Number of hits: "))                                      

            at_bat, hits = validate_avg(at_bat, hits)
            average = round(float(hits/at_bat), 3)
            if average == 0:
                average = "<0.001"
            list_data.append([name, position, at_bat, hits, average])
            fileio.write_file(FILENAME, list_data)                                  #write new player to file
            print(f"{name} was added to the team.")
            print()
            
        except UserWarning as w:
            print(w)
        except ValueError:
            print("Hits and at bats must be whole numbers. Cannot contain letters or specials. Add operation cancelled.\n")
        except ZeroDivisionError:
            print("cannot have zero times at bat. Add operation cancelled.\n")
            

def removePlayer(list_data):
    try:                                                                                            #add error handling for invalid user inputs
        delete = int(input("which player number would you like to remove?: "))
        print(f"{list_data[delete -  1][0]} has been removed from the team")
        print()
        list_data.pop(int(delete) -1)
        fileio.write_file(FILENAME, list_data)                                  #remove player from file
    except ValueError:
        print("You must enter the lineup number. Remove operation cancelled.\n")
    except IndexError:
        print("Lineup number does not exist. Remove operation cancelled.\n")

def movePlayer(list_data):
    try:                                                                                             #add error handling for invalid user inputs
        currentNum = input("Current lineup number: ")
        newNum = input("New lineup number: ")
        placeholder = list_data.pop(int(currentNum) - 1)
        list_data.insert((int(newNum)-1), placeholder)
        fileio.write_file(FILENAME, list_data)                                  #write new list order to file
        print(f"{list_data[int(newNum)-1][0]} was moved to position {newNum} in the lineup.")
        print()
    except ValueError:
        print("You must enter the desired linup numbers. Move operation cancelled.\n")
    except IndexError:
        print("Lineup number does not exist. Remove operation cancelled.\n")

def changePosition(list_data):
    try:                                                                                            #add error handling for invalid user inputs
        print("POSITIONS")
        print(*POSITIONS, sep=" | ")
        player = input("Current lineup number: ")
        newPos = input("Enter the new position: ").upper()
        newPos = validate_pos(newPos)
        currentPos=  list_data[int(player)-1][1]
        list_data[int(player)-1][1] = newPos
        fileio.write_file(FILENAME, list_data)                                  #write new position to file
        print(f"{list_data[int(player)-1][0]}'s position was changed from {currentPos} to {newPos}.")
        print()
    except IndexError:
        print("Number does not exist in the current lineup. Change operation cancelled.\n")
    except ValueError:
        print("Lineup number cannot be a letter or symbol. Change operation cancelled.\n")

def changeStats(list_data):
    try:                                                                                            #add error handling for invalid user inputs
        player = input("Current lineup number: ")
        if any(char.isdigit() for char in player) == False:
            raise UserWarning("Lineup number cannot be a letter or symbol. Edit operation cancelled.\n")
        at_bat =int(input("Official number of at bats: "))                  #get times at bat from the user
        hits = int(input("Number of hits: "))                                       #get number of hits from the user
        at_bat, hits = validate_avg(at_bat, hits)
        average = round(float(hits/at_bat), 3)
        if average == 0:
            average = "<0.001"
        list_data[int(player)-1][2] = at_bat
        list_data[int(player)-1][3] = hits
        list_data[int(player)-1][4] = average
        fileio.write_file(FILENAME, list_data)                                  #write new stats to file
        print(f"Stats for {list_data[int(player)-1][0]} have been updated.")
        print()

    except UserWarning as w:
        print(w)
    except ValueError:
        print("Hits and at bats must be whole numbers. Cannot contain letters or specials. Edit operation cancelled.\n")
    except ZeroDivisionError:
        print("cannot have zero times at bat. Add operation cancelled.\n")

def main ():
    players = fileio.read_file(FILENAME)

    
    display_separator()
    display_title()
    display_menu(POSITIONS)
    display_separator()

    while True:
        menu = (input("Menu option: "))
        if menu == "1":
            showLineup()
        elif menu == "2":
             addPlayer(players)
        elif menu == "3":
            removePlayer(players)
        elif menu == "4":
            movePlayer(players)
        elif menu == "5":
            changePosition(players)
        elif menu == "6":
            changeStats(players)
        elif menu == "7":
            print("Bye!")
            break                
        else:
            print("Not a valid option. Please try agian.\n")
            display_menu(POSITIONS)
            display_separator()
        

if __name__ == "__main__":
    main()
