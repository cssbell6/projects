"""
File: metro_lines.py
Author: Chance Bell
Date: 5/4/2022
Section: 30-LEC (1648)
E-mail: cbell3@umbc.edu
Description: A program that accepts user inputs and puts them through a series of if statements based off of the
command and organizes them into various dictionaries. The dictionaries are then passed through as parameters to a
recursive function which tells a user howto get from one station to another. In general, it creates a trip planner
which will tell a user how to get from one station to another.
"""

def find_path(locations, current, destination, current_line, trains):
    start = list(current) # a deep copy of our starting point
    if current == destination: # if our desired location == our desired destination
        return [destination]

    if locations[current]['visited']:
        return False # if the point in the dictionary was already visited than visited returns False

    locations[current]['visited'] = True
    for new_place in locations[current]['connections']: # for each value in the key current
        the_path = find_path(locations, new_place[0], destination, current_line, trains)
        # the recursive call that returns the value new_place[0] and checks to see if it == to destination
        if the_path: #
            return [current] + the_path # we get back a list of the points we searched and that worked

    return f"There is no path to get from {''.join(start)} to {destination}." # if there is no path that works


def run_metro_system(name): #
    locations = dict() # two dictionaries for stations/locations and trains are created
    trains = dict()
    command = ''

    # a while loop is put into to place so that the program continues to run until the user inputs "exit"
    while 'exit' not in command:
        command = input(f'[{name}] >>> ').split()
        # this if statement checks for the creation of stations and trains
        if 'create' in command[0]:
            if 'station' in command[1] and len(command) == 3:
                locations[command[2]] = {'connections': [], 'visited': False}
            elif 'train' in command[1] and len(command) == 5:
                trains[command[2]] = command[3], command[4]
            else:
                print(f"Unknown command {' '.join(command)}")

        # this elif statement connects stations to one another
        elif 'connect' in command and 'stations' in command and len(command) == 5:
            if command[2] in locations:
                if command[3] in locations:
                    locations[command[2]]['connections'].append([command[3], command[4]])
                    locations[command[3]]['connections'].append([command[2], command[4]])
                else:
                    print(f'\t {command[3]} is not in the list of stations.')
            else: # makes sure the stations exists
                print(f'\t {command[2]} is not in the list of stations.')

        # this elif statement display either the current stations or trains
        elif 'display' in command and len(command) == 2:
            if 'stations' in command:
                for i in locations:
                    print(f'\t{i}')
            elif 'trains' in command:
                for k, v in trains.items():
                    print(f"*** Information for Train {k} ***\n\tLine: {v[0]}\n\tCurrent Position: {v[1]}")

        # this elif statement gets specific info on stations or trains based off of the users desired input
        elif 'get' in command and 'info' in command and len(command) == 4:
            if 'station' in command:
                print(f"*** Information for Station {command[3]} ***")
                for i in locations:
                    for j in locations[i]['connections']:
                        if i == command[3]:
                            print(f"\t{j[1]} Line - Next Station: {j[0]}")
            elif 'train' in command:
                for k, v in trains.items():
                    if command[3] in k:
                        print(f"*** Information for Train {k} ***\n\tLine: {v[0]}\n\tCurrent Position: {v[1]}")

        # the elif statement that obtains how to get from one stations to another by calling a function which is
        # recursive in itself. The function then returns a list of points that it searched to get to our destination.
        elif 'plan' in command and 'trip' in command and len(command) == 4:
            if command[2] in locations and command[3] in locations:
                path_list = find_path(locations, command[2], command[3], '', trains)
                direct = list() # a list which keeps our strings and which are ultimately joined at the end
                count = 1 # used for the start only
                for i in range(len(path_list)):
                    for k in locations[path_list[i]]['connections']:
                        if count == 1:
                            direct.append(f'Start on the {k[1]} --> {path_list[i]}')
                            previous = k[1]
                            count += 1
                        elif k[1] != previous and path_list[i] != path_list[-1] and count > 1:
                            direct.append(f'--> At {path_list[i]} transfer from the {previous} '
                                          f'line to the {k[1]} line.')
                            previous = k[1]
                            count += 1
                        elif count != 2 or i == (len(path_list) - 1):
                            direct.append(f'--> {path_list[-1]}')
                            previous = k[1]
                            count += 1
                count = 1
                print(' '.join(direct)) # joins the list of strings together

                for location in locations: # resets the visited boolean values in the locations dictionary
                    locations[location]['visited'] = False
            else: # is ran if either one of our stations we inputted into plan trip do not exist
                print(f'Stations {command[2]} or {command[3]} do not exist.')

        else:
            if 'exit' not in command:
                print(f"Unknown command {' '.join(command)}")
                # if our command is a greater index than we want or simply does not exist, than the program tells us
                # that our inputted command doesn't exist

if __name__ == "__main__":
    metro_system_name = input('>>> ')
    run_metro_system(metro_system_name) # runs the functions and uses the input as a parameter