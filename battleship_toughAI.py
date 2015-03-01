from random import *

class Battleship:

    def __init__(self):
        self.computer_grid = self.freeze([['   ']*10]*10)
        self.player_grid = self.freeze([['   ']*10]*10)
        self.locations = self.location_setup()
        self.computer_locations = self.location_setup()
        self.computer_ships = []
        self.computer_hit_player = False
        self.up_track = []
        self.down_track = []
        self.left_track = []
        self.right_track = []
        self.difficulty = 'Hard'
        self.player_ships_lengths = [2,3,3,3,4,5]

    def freeze(self, given):
        result = []
        for element in given:
            if type(element) == list:
                result += [self.freeze(element)]
            else:
                result += [element]
        return result

    def surroundings(self, location):
        places = []
        places.append(chr(ord(location[0])-1) + location[1:])
        places.append(location[0] + str(int(location[1:])+1))
        places.append(location[0] + str(int(location[1:])-1))
        places.append(chr(ord(location[0])+1) + location[1:])
        places.append((chr(ord(location[0])+1))+str(int(location[1:])+1))
        places.append((chr(ord(location[0])+1))+str(int(location[1:])-1))
        places.append((chr(ord(location[0])-1))+str(int(location[1:])+1))
        places.append((chr(ord(location[0])-1))+str(int(location[1:])-1))
        return places

    def computer_track(self):
        origin = self.last_hit
        new_point = chr(ord(origin[0])-1) + origin[1:]
        while new_point in self.locations:
            self.up_track.append(new_point)
            new_point = chr(ord(new_point[0])-1) + new_point[1:]
        new_point = chr(ord(origin[0])+1) + origin[1:]
        while new_point in self.locations:
            self.down_track.append(new_point)
            new_point = chr(ord(new_point[0])+1) + new_point[1:]
        new_point = origin[0] + str(int(origin[1:])-1)
        while new_point in self.locations:
            self.left_track.append(new_point)
            new_point = new_point[0] + str(int(new_point[1:])-1)
        new_point = origin[0] + str(int(origin[1:])+1)
        while new_point in self.locations:
            self.right_track.append(new_point)
            new_point = new_point[0] + str(int(new_point[1:])+1)
        
    def location_setup(self):
        result = []
        for letter in 'ABCDEFGHIJ':
            for i in range(1,11):
                result.append(letter + str(i))
        return result

    def draw_full_grid(self):
        copy_cat = []
        for element in self.computer_grid:
            storage = []
            for sub_element in element:
                if sub_element == ' # ' or sub_element == ' X ':
                    storage.append(sub_element)
                else:
                    storage.append('   ')
            copy_cat.append(storage)
        print('  COMPUTER GRID' + ' '*38 + 'PLAYER GRID')
        print('    1   2   3   4   5   6   7   8   9   10             1   2   3   4   5   6   7   8   9   10')
        print('  ' + '-'*41 + '          ' + '-'*41)
        letters = 'ABCDEFGHIJ'
        for i in range(10):
            to_print = letters[i] + ' |'
            combined = copy_cat[i] + self.player_grid[i]
            for j in range(len(combined)):
                to_print += combined[j] + '|'
                if j == 9:
                    to_print += '        ' + letters[i] + ' |'
            print(to_print)
            print('  ' + '-'*41 + '          ' + '-'*41)
                
        
    def draw_grid(self, side):
        j = 0
        print('    1   2   3   4   5   6   7   8   9   10')
        letters = ['J ','I ','H ','G ','F ','E ','D ','C ','B ','A ']
        if side == 'player':
            for element in self.player_grid:
                to_print = letters.pop() + '|'
                j += 1
                for i in range(len(element)):
                    to_print += element[i] + '|'
                print(to_print)
                if j < 10: 
                    print('  ' +'-'*41)
        else:
            for element in self.computer_grid:
                to_print = letters.pop() + '|'
                j += 1
                for i in range(len(element)):
                    if element[i] == ' X ' or element[i] == ' # ':
                        to_print += element[i] + '|'
                    else:
                        to_print += '   |'
                print(to_print) 
                if j < 10: 
                    print('  '+'-'*41)

    def reveal_computer_grid(self):
        '''Reveals the full computer grid. For testing purposes'''
        j = 0
        print('    1   2   3   4   5   6   7   8   9   10')
        letters = ['J ','I ','H ','G ','F ','E ','D ','C ','B ','A ']
        for element in self.computer_grid:
                to_print = letters.pop() + '|'
                j += 1
                for i in range(len(element)):
                    to_print += element[i] + '|'
                print(to_print) 
                if j < 10: 
                    print('  '+'-'*41)

    def fire_missle_player(self, location):
        needed = ['   ', ' O ']
        location = location.upper()
        if location in self.locations:
            if self.computer_grid[ord(location[0]) - 65][int(location[1:])-1] in needed:
                if self.computer_grid[ord(location[0]) - 65][int(location[1:])-1] == ' O ':
                    self.computer_grid[ord(location[0]) - 65][int(location[1:])-1] = ' X '
                    which_ship = []
                    sunk = True
                    for element in self.computer_ships:
                        if location in element:
                            which_ship = element
                    for element in which_ship:
                        if self.computer_grid[ord(element[0]) - 65][int(element[1:])-1] != ' X ':
                            sunk = False
                    if sunk:
                        print('You sunk a ship!')
                        for place in which_ship:
                            surroundings = self.surroundings(place)
                            for sub_element in surroundings:
                                if sub_element in self.locations and self.computer_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] == '   ':
                                    self.computer_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] = ' # '
                    else:
                        print('You hit!')
                else:
                    print('You missed!')
                    self.computer_grid[ord(location[0]) - 65][int(location[1:])-1] = ' # '
                return 'Valid'
        return 'Invalid'

    def add_block_player(self, location):
        location = location.upper()
        if location in self.locations:
            self.player_grid[ord(location[0]) - 65][int(location[1:])-1] = ' O '
        else:
            return 'Invalid'

    def computer_grid_generate(self, length):
        random = self.computer_locations[:]
        directions = ['up', 'right', 'down', 'left']
        ship_placed = False
        while not ship_placed:
            can_go_on = True
            shuffle(random)
            shuffle(random)
            chosen = random[5]
            storage = []
            shuffle(directions)
            order = directions[1]
            if order == 'up':
                for i in range(length):
                    storage.append(chr(ord(chosen[0])-i) + chosen[1:])
            elif order == 'right':
                for i in range(length):
                    storage.append(chosen[0] + str(int(chosen[1:])+i))
            elif order == 'left':
                for i in range(length):
                    storage.append(chosen[0] + str(int(chosen[1:])-i))
            else:
                for i in range(length):
                    storage.append(chr(ord(chosen[0])+i) + chosen[1:])
            for location in storage:
                if location not in self.computer_locations:
                    can_go_on = False
            if can_go_on:
                temp = []
                for location in storage:
                    self.computer_grid[ord(location[0]) - 65][int(location[1:])-1] = ' O '
                    removal = self.surroundings(location)
                    for element in removal:
                        if element in self.computer_locations:
                            self.computer_locations.remove(element)
                    temp.append(location)
                self.computer_ships.append(temp)
                ship_placed = True

    def fire_missle_computer(self):
        if not self.computer_hit_player:
            resolved = False
            random = self.locations[:]
            while not resolved:
                if self.difficulty == 'Hard':
                    chosen = self.computer_fire_missle_hard()
                else:
                    shuffle(random)
                    chosen = random[5]
                if self.player_grid[ord(chosen[0]) - 65][int(chosen[1:])-1] == '   ':
                    print('The computer shot at ' + chosen + ' and missed!')
                    self.player_grid[ord(chosen[0]) - 65][int(chosen[1:])-1] = ' # '
                    resolved = True
                elif self.player_grid[ord(chosen[0]) - 65][int(chosen[1:])-1] == ' O ':
                    self.player_grid[ord(chosen[0]) - 65][int(chosen[1:])-1] = ' X '
                    surroundings = self.surroundings(chosen)
                    sunk = True
                    for element in surroundings:
                        if element in self.locations and self.player_grid[ord(element[0]) - 65][int(element[1:])-1] == ' O ':
                            sunk = False
                    if sunk:
                        print('The computer shot at ' + chosen  + ', hit, and downed one of your ships!')
                        self.player_ships_lengths.remove(1)
                        for element in surroundings:
                            if element in self.locations and self.player_grid[ord(element[0]) - 65][int(element[1:])-1] == '   ':
                                self.player_grid[ord(element[0]) - 65][int(element[1:])-1] = ' # '
                    else:
                        print('The computer shot at ' + chosen + ' and hit a ship!')
                        self.computer_hit_player = True
                        self.last_hit = chosen
                        self.current_tracked_ship = [chosen]
                        self.computer_tracking = ['left', 'right', 'up', 'down']
                        self.computer_track()
                        if self.difficulty == 'Hard':
                            spaces = self.avaible_tiles(self.last_hit)
                            if spaces[0] < min(self.player_ships_lengths):
                                self.computer_tracking.remove('left')
                                self.computer_tracking.remove('right')
                            if spaces[1] < min(self.player_ships_lengths):
                                self.computer_tracking.remove('up')
                                self.computer_tracking.remove('down')
                    resolved = True
        else:
            resolved = False
            hit = False
            while not resolved:
                shuffle(self.computer_tracking)
                result = self.computer_tracking[0]
                if result == 'up' and len(self.up_track) != 0:
                    if self.player_grid[ord((self.up_track[0])[0]) - 65][int((self.up_track[0])[1:])-1] == '   ':
                        self.player_grid[ord((self.up_track[0])[0]) - 65][int((self.up_track[0])[1:])-1] = ' # '
                        self.computer_tracking.remove('up')
                        print('The computer shot at ' + self.up_track[0] + ' and missed!')
                        resolved = True
                    elif self.player_grid[ord((self.up_track[0])[0]) - 65][int((self.up_track[0])[1:])-1] == ' O ':
                        self.player_grid[ord((self.up_track[0])[0]) - 65][int((self.up_track[0])[1:])-1] = ' X '
                        hit = True
                        resolved = True
                        last_hit = self.up_track[0]
                        self.current_tracked_ship.append(self.up_track.pop(0))
                        if 'right' in self.computer_tracking:
                            self.computer_tracking.remove('right')
                        if 'left' in self.computer_tracking:
                            self.computer_tracking.remove('left')
                    else:
                        self.computer_tracking.remove('up')
                elif result == 'down' and len(self.down_track) != 0:
                    if self.player_grid[ord((self.down_track[0])[0]) - 65][int((self.down_track[0])[1:])-1] == '   ':
                        self.player_grid[ord((self.down_track[0])[0]) - 65][int((self.down_track[0])[1:])-1] = ' # '
                        self.computer_tracking.remove('down')
                        print('The computer shot at ' + self.down_track[0] + ' and missed!')
                        resolved = True
                    elif self.player_grid[ord((self.down_track[0])[0]) - 65][int((self.down_track[0])[1:])-1] == ' O ':
                        self.player_grid[ord((self.down_track[0])[0]) - 65][int((self.down_track[0])[1:])-1] = ' X '
                        hit = True
                        resolved = True
                        last_hit = self.down_track[0]
                        self.current_tracked_ship.append(self.down_track.pop(0))
                        if 'right' in self.computer_tracking:
                            self.computer_tracking.remove('right')
                        if 'left' in self.computer_tracking:
                            self.computer_tracking.remove('left')
                    else:
                        self.computer_tracking.remove('down')
                elif result == 'left' and len(self.left_track) != 0:
                    if self.player_grid[ord((self.left_track[0])[0]) - 65][int((self.left_track[0])[1:])-1] == '   ':
                        self.player_grid[ord((self.left_track[0])[0]) - 65][int((self.left_track[0])[1:])-1] = ' # '
                        self.computer_tracking.remove('left')
                        print('The computer shot at ' + self.left_track[0] + ' and missed!')
                        resolved = True
                    elif self.player_grid[ord((self.left_track[0])[0]) - 65][int((self.left_track[0])[1:])-1] == ' O ':
                        self.player_grid[ord((self.left_track[0])[0]) - 65][int((self.left_track[0])[1:])-1] = ' X '
                        hit = True
                        resolved = True
                        last_hit = self.left_track[0]
                        self.current_tracked_ship.append(self.left_track.pop(0))
                        if 'down' in self.computer_tracking:
                            self.computer_tracking.remove('down')
                        if 'up' in self.computer_tracking:
                            self.computer_tracking.remove('up')
                    else:
                        self.computer_tracking.remove('left')
                elif result == 'right' and len(self.right_track) != 0:
                    if self.player_grid[ord((self.right_track[0])[0]) - 65][int((self.right_track[0])[1:])-1] == '   ':
                        self.player_grid[ord((self.right_track[0])[0]) - 65][int((self.right_track[0])[1:])-1] = ' # '
                        self.computer_tracking.remove('right')
                        print('The computer shot at ' + self.right_track[0] + ' and missed!')
                        resolved = True
                    elif self.player_grid[ord((self.right_track[0])[0]) - 65][int((self.right_track[0])[1:])-1] == ' O ':
                        self.player_grid[ord((self.right_track[0])[0]) - 65][int((self.right_track[0])[1:])-1] = ' X '
                        hit = True
                        resolved = True
                        last_hit = self.right_track[0]
                        self.current_tracked_ship.append(self.right_track.pop(0))
                        if 'down' in self.computer_tracking:
                            self.computer_tracking.remove('down')
                        if 'up' in self.computer_tracking:
                            self.computer_tracking.remove('up')
                    else:
                        self.computer_tracking.remove('right')
                if hit:
                    sunk = True
                    for element in self.current_tracked_ship:
                        tiles = self.surroundings(element)
                        for location in tiles:
                            if location in self.locations and self.player_grid[ord(location[0]) - 65][int(location[1:])-1] == ' O ':
                                sunk = False
                    if not sunk:
                        print('The computer shot at ' + last_hit + ' and hit a ship!')
                            
                    else:
                        print('The computer shot at ' + self.current_tracked_ship[-1] +', hit, and downed one of your ships!')
                        self.player_ships_lengths.remove(len(self.current_tracked_ship))
                        for element in self.current_tracked_ship:
                            tiles = self.surroundings(element)
                            for location in tiles:
                                if location in self.locations and self.player_grid[ord(location[0]) - 65][int(location[1:])-1] == '   ':
                                    self.player_grid[ord(location[0]) - 65][int(location[1:])-1] = ' # '
                        self.computer_hit_player = False
                        self.up_track = []
                        self.down_track = []
                        self.left_track = []
                        self.right_track = []
                        

    def computer_fire_missle_hard(self):
        min_length = min(self.player_ships_lengths)
        random = self.locations[:]
        done = False
        while not done:
            shuffle(random)
            chosen = self.avaible_tiles(random[5])
            if chosen[0] >= min_length or chosen[1] >= min_length:
                done = True
        return random[5]

    def avaible_tiles(self, chosen):
        horizontal_result = 1
        vertical_result = 1
        not_allowed = ' X  # '
        new_point = chr(ord(chosen[0])-1) + chosen[1:]
        while new_point in self.locations and self.player_grid[ord(new_point[0]) - 65][int(new_point[1:])-1] not in not_allowed:
            vertical_result += 1
            new_point = chr(ord(new_point[0])-1) + new_point[1:]
        new_point = chr(ord(chosen[0])+1) + chosen[1:]
        while new_point in self.locations and self.player_grid[ord(new_point[0]) - 65][int(new_point[1:])-1] not in not_allowed:
            vertical_result += 1
            new_point = chr(ord(new_point[0])+1) + new_point[1:]
        new_point = chosen[0] + str(int(chosen[1:])-1)
        while new_point in self.locations and self.player_grid[ord(new_point[0]) - 65][int(new_point[1:])-1] not in not_allowed:
            horizontal_result += 1
            new_point = new_point[0] + str(int(new_point[1:])-1)
        new_point = chosen[0] + str(int(chosen[1:])+1)
        while new_point in self.locations and self.player_grid[ord(new_point[0]) - 65][int(new_point[1:])-1] not in not_allowed:
            horizontal_result += 1
            new_point = new_point[0] + str(int(new_point[1:])+1)
        return [horizontal_result, vertical_result]

    def winner(self):
        player = True
        computer = True
        for element in self.player_grid:
            for sub_element in element:
                if sub_element == ' O ':
                    computer = False
        for element in self.computer_grid:
            for sub_element in element:
                if sub_element == ' O ':
                    player = False
        if player:
            return 'Player wins'
        elif computer:
            return 'Computer wins'
        else:
            return 'No one'
                    

if __name__ == '__main__':
    def begin_game():
        print('Welcome to battleship.')
        print('Select a difficulty, either normal or hard.')
        print('Normal has a standard AI. It will shoot randomly until it hits, at which point it will proceed to down the ship.')
        print('Hard AI is the same but takes into account the length of the smallest ship left alive on your side, which results in more accurate hits late game due to the heightened logic.')
        diff = input('So select, Hard or Normal? ')
        diff = diff.lower()
        valid = 'hardnormal'
        while diff not in valid:
            print('Invalid input')
            diff = input('Hard or Normal? ')
            diff = diff.lower()
        game = Battleship()
        game.difficulty = diff
        game.draw_grid('player')
        done = False
        while not done:
            user_input = input('Enter the points of your two-tile ship. Seperate each spot with a space. ')
            user_input = user_input.upper()
            valid = True
            if len(user_input) == 5:
                coordinates = [user_input[0:2], user_input[3:]]
                coordinates.sort()
                for element in coordinates:
                    testing = game.surroundings(element)
                    for sub_element in testing:
                        if sub_element in game.locations and game.player_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] != '   ':
                            valid = False
            else:
                valid = False
            if valid:
                for element in coordinates:
                    game.add_block_player(element)
                done = True
            else:
                print('Input invalid')
        game.draw_grid('player')
        done = False
        while not done:
            user_input = input('Enter the points of your first three-tile ship. Seperate each spot with a space. ')
            user_input = user_input.upper()
            valid = True
            if len(user_input) == 8:
                coordinates = [user_input[0:2], user_input[3:5], user_input[6:]]
                coordinates.sort()
                for element in coordinates:
                    testing = game.surroundings(element)
                    for sub_element in testing:
                        if sub_element in game.locations and game.player_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] != '   ':
                            valid = False
            else:
                valid = False
            if valid:
                for element in coordinates:
                    game.add_block_player(element)
                done = True
            else:
                print('Input invalid')
        game.draw_grid('player')
        done = False
        while not done:
            user_input = input('Enter the points of your second three-tile ship. Seperate each spot with a space. ')
            user_input = user_input.upper()
            valid = True
            if len(user_input) == 8:
                coordinates = [user_input[0:2], user_input[3:5], user_input[6:]]
                coordinates.sort()
                for element in coordinates:
                    testing = game.surroundings(element)
                    for sub_element in testing:
                        if sub_element in game.locations and game.player_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] != '   ':
                            valid = False
            else:
                valid = False
            if valid:
                for element in coordinates:
                    game.add_block_player(element)
                done = True
            else:
                print('Input invalid')
        game.draw_grid('player')
        done = False
        while not done:
            user_input = input('Enter the points of your third three-tile ship. Seperate each spot with a space. ')
            user_input = user_input.upper()
            valid = True
            if len(user_input) == 8:
                coordinates = [user_input[0:2], user_input[3:5], user_input[6:]]
                coordinates.sort()
                for element in coordinates:
                    testing = game.surroundings(element)
                    for sub_element in testing:
                        if sub_element in game.locations and game.player_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] != '   ':
                            valid = False
            else:
                valid = False
            if valid:
                for element in coordinates:
                    game.add_block_player(element)
                done = True
            else:
                print('Input invalid')
        game.draw_grid('player')
        done = False
        while not done:
            user_input = input('Enter the points of your four-tile ship. Seperate each spot with a space. ')
            user_input = user_input.upper()
            valid = True
            if len(user_input) == 11:
                coordinates = [user_input[0:2], user_input[3:5], user_input[6:8], user_input[9:]]
                coordinates.sort()
                for element in coordinates:
                    testing = game.surroundings(element)
                    for sub_element in testing:
                        if sub_element in game.locations and game.player_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] != '   ':
                            valid = False
            else:
                valid = False
            if valid:
                for element in coordinates:
                    game.add_block_player(element)
                done = True
            else:
                print('Input invalid')
        game.draw_grid('player')
        done = False
        while not done:
            user_input = input('Enter the points of your five-tile ship. Seperate each spot with a space. ')
            user_input = user_input.upper()
            valid = True
            if len(user_input) == 14:
                coordinates = [user_input[0:2], user_input[3:5], user_input[6:8], user_input[9:11], user_input[12:]]
                coordinates.sort()
                for element in coordinates:
                    testing = game.surroundings(element)
                    for sub_element in testing:
                        if sub_element in game.locations and game.player_grid[ord(sub_element[0]) - 65][int(sub_element[1:])-1] != '   ':
                            valid = False
            else:
                valid = False
            if valid:
                for element in coordinates:
                    game.add_block_player(element)
                done = True
            else:
                print('Input invalid')
        game.draw_grid('player')
        crap = True
        computer_ships = [2,3,3,3,4,5]
        shuffle(computer_ships)
        for element in computer_ships:
            game.computer_grid_generate(element)
        while crap:
            game.draw_full_grid()
            user_input = game.fire_missle_player(input('Enter a location: '))
            while user_input == 'Invalid':
                print('Invalid location selected')
                user_input = game.fire_missle_player(input('Enter a location: '))
            if game.winner() == 'Player wins':
                print('You won!')
                break
            game.fire_missle_computer()
            if game.winner() == 'Computer wins':
                print('You lost!')
                break
        

    def test_run():
        ''' Here! '''
        crap = True
        computer_ships = [2,3,3,3,4,5]
        shuffle(computer_ships)
        for element in computer_ships:
            test.computer_grid_generate(element)
        while crap:
            test.draw_full_grid()
            user_input = test.fire_missle_player(input('Enter a location: '))
            while user_input == 'Invalid':
                print('Invalid location selected')
                user_input = test.fire_missle_player(input('Enter a location: '))
            if test.winner() == 'Player wins':
                print('You won!')
                break
            test.fire_missle_computer()
            if test.winner() == 'Computer wins':
                print('You lost!')
                break
            
                        
                    
# Somethings wrong with input in begin_game. Coordinates come up fine but logic error strikes and fails the call. Find and fix.
                        
                        
                        
                                                        
                
                    
                
                    
                    

                
                
                        
                        
            
        
