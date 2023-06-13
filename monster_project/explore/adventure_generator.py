
def make_location(row, col, location_type, width, height):
    terrain = ''
    match location_type:
        case '~':
            terrain = 'water'
        case '.':
            terrain = 'grass'
        case 'T':
            terrain = 'tree'
        case '^':
            terrain = 'mountain'

    location = {(row, col): {'terrain': terrain, 'connections': []}}
    connections = {'north': 'nothing', 'south': 'nothing', 'east': 'nothing', 'west': 'nothing'}
    if row > 0:
        connections.update({'north': (row-1, col)})
    if row < height-1:
        connections.update({'south':(row+1, col)})
    if col > 0:
        connections.update({'west':(row, col-1)})
    if col < width-1:
        connections.update({'east':(row, col+1)})
    location[(row, col)]['connections'] = connections
    return location
        

def make_map(filename='test_map.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()

    game_map = {}
    width = len(lines[0].strip())
    height = len(lines)
    row=0
    for line in lines:
        col=0
        for location in line.strip():
            game_map.update(make_location(row, col, location, width, height))
            col += 1
        row += 1
    return game_map

def walk_map(game_map, start=(2,6)):
    '''The main game loop. Each turn the player gives an input and can move to a new space. They can move N, S, E, W, or Q to quit.'''
    current_location = start
    while True:
        location_prompt(game_map[current_location], game_map)
        direction = input('Which direction do you want to go? (N, S, E, W): ')
        if direction == 'Q':
            print('Goodbye!')
            break
        elif direction in ['N', 'S', 'E', 'W']:
            
            if direction == 'N':
                new_location = (current_location[0]-1, current_location[1])
            elif direction == 'S':
                new_location = (current_location[0]+1, current_location[1])
            elif direction == 'E':
                new_location = (current_location[0], current_location[1]+1)
            elif direction == 'W':
                new_location = (current_location[0], current_location[1]-1)

            if new_location in game_map[current_location]['connections'].values():
                current_location = new_location
            else:
                print('You can\'t go that way!')
        else:
            print('Invalid input!')

def location_prompt(location: dict, game_map: dict):
    '''Prints the terrain of the location and the connections to other locations.'''
    east = location['connections'].get('east', 'nothing')
    west = location['connections'].get('west', 'nothing')
    north = location['connections'].get('north', 'nothing')
    south = location['connections'].get('south', 'nothing')

    if east != 'nothing':
        east = game_map[east]['terrain']
    if west != 'nothing':
        west = game_map[west]['terrain']
    if north != 'nothing':
        north = game_map[north]['terrain']
    if south != 'nothing':
        south = game_map[south]['terrain']

    prompt = f'''This location is covered in {location["terrain"]}. To the north there is {north}, to the west there is {west}, to the east there is {east}, to the south there is {south}. Describe this landscape using a small amount of descriptive imagery. Over all the description should be simple, the imagery embellishing occasionally.  Only describe plants and terrain, no animals. Only use 4 to 8 sentences. Do not include cardinal directions in your description, instead give an overall view of the location. Use pure description without any pronouns and minimal adverbs. Do not reference the horizon or say that something goes on forever, simply describe the current surroundings.'''
    return prompt


def get_location():
    game_map = make_map()
    return location_prompt(game_map[(2,6)], game_map)