# Author: Calvin Todd
# Date: 11.19.20
# Description: Assignment 9/Portfolio Project where we create a representation of the board game Domination!

class FocusGame:
    """
    The main class to represent the board, player moves, and win conditions for the Focus Game.  The __init__ function
    for the class creates two instances of the Players class based on the tuple of data used to initialize the
    FocusGame class.  FocusGame will call to the Player class objects when it needs information specifically related
    the players.  Otherwise, FocusGame will contain all information related to the game.
    """

    def __init__(self, player_one, player_two):
        """
        Initializes the FocusGame class with an empty board, the player objects,
        turn order, and a winner status.  Once everything is initialized, __init__ will run the
        initialize_game() function to set up the board.
        """
        self._player_one = Player(player_one[0], player_one[1])
        self._player_two = Player(player_two[0], player_two[1])
        self._turn = None
        self._winner = None
        self._board =[[[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []],
                      [[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []]]
        self.initialize_game()

    def get_board(self):
        """
        Returns the FocusGame ._board data member.
        """
        return self._board

    def set_board(self, board):
        """
        Takes an instance of the game board as a parameter and updates the FocusGame ._board data member.
        """
        self._board = board

    def get_player_one(self):
        """
        Returns FocusGame Player One object
        """
        return self._player_one

    def get_player_two(self):
        """
        Returns FocusGame Player Two object
        """
        return self._player_two

    def get_turn(self):
        """
        Returns the current turn for the FocusGame
        """
        return self._turn

    def set_turn(self, player_name):
        """
        Takes a parameter of a player name, sets the FocusGame turn to that player
        """
        self._turn = player_name

    def get_winner(self):
        """
        Returns the current value for the FocusGame winner
        """
        return self._winner

    def set_winner(self, player_name):
        """
        Take a parameter of a player_name and sets the winner data field of FocusGame to the inputted player
        """
        self._winner = player_name

    def print_board(self):
        """
        Print FocusGame board for testing purposes
        """
        board = self.get_board()
        row_num = 0
        for row in board:
            space_num = 0
            for space in row:
                print('(', row_num, ',', space_num, ')', '=', space, end=' | ')
                space_num += 1
            row_num += 1
            print('')

    def initialize_game(self):
        """
        Initializes the board with player pieces, runs at the end of the __init__ function.
        """
        board = self.get_board()
        player_one = self.get_player_one()
        player_two = self.get_player_two()

        counter = 0
        color = player_one.get_player_color()
        row_counter = 0

        for row in board:
                space_counter = 0
                for space in row:
                    if counter == 2 and color == player_one.get_player_color():
                        color = player_two.get_player_color()
                        counter = 0
                    if counter == 2 and color == player_two.get_player_color():
                        color = player_one.get_player_color()
                        counter = 0
                    space.append(color)
                    counter += 1
                    space_counter += 1
                row_counter += 1
        self.set_board(board)

    def move_piece(self, player_name, start, destination, num_of_pieces):
        """
        Method for the movement of pieces.  Takes a player_name, start location, destination location, and the number
        of pieces desired to move as parameters.  move_piece will check the validity of the move and then make the
        appropriate move depending on whether it is a single move or multiple move.  Will update the board, and captured
        and reserved pieces and finally check win conditions.  This will all lead in to updating the next turn for
        the FocusGame and returning the appropriate message
        """
        turn = self.get_turn()
        player = self.get_active_player(player_name)
        movement_range = self.get_range(start)
        move_size = self.move_size(start, destination)
        valid_move = self.check_valid_move(player, start, destination)
        pieces_to_move = self.get_pieces_to_move(start, num_of_pieces)

        if turn != player and turn != None:
            return 'not your turn'

        if move_size > movement_range:
            return 'invalid location'

        if num_of_pieces > movement_range:
            return 'invalid number of pieces'

        if valid_move is False:
            return 'invalid location'

        board = self.update_board_location(start, destination, pieces_to_move)
        board = self.process_stack(board, destination, player)

        if self.get_winner() is not None:
            return 'Wins'

        else:
            self.set_board(board)
            self.get_next_player(player)
            return 'successfully moved'

    def get_next_player(self, player):
        """
        Takes a player's name as a parameter and updates the FocusGame ._turn data field to whose turn it will be next.
        """
        player_one = self.get_player_one()
        player_two = self.get_player_two()
        if player_one.get_player_name() == player.get_player_name():
            self.set_turn(player_two.get_player_name())
        else:
            self.set_turn(player_one.get_player_name())

    def process_stack(self, board, destination, player):
        """
        Takes the stack post player move and processes it.  Captures enemy pieces and gets reserve pieces if the size of
        the stack is more than five pieces.  Updates the current board and returns it to the calling function.
        """
        stack = board[destination[0]][destination[1]]
        while len(stack) > 5:
            piece = stack[0]
            if piece == player.get_player_color():
                player.add_reserve_piece()
            else:
                player.capture_piece()
            stack = stack[1:]

        board[destination[0]][destination[1]] = stack

        self.check_win_conditions(player)

        return board

    def check_win_conditions(self, player):
        """
        Takes a player object as the parameter and checks to see if the player has met the win conditions, updates the
        ._winner data member if so.
        """
        if player.get_captured_pieces() > 5:
            self.set_winner(player)

    def update_board_location(self, start, destination, pieces_to_move):
        """
        Takes the starting location tuple, destination tuple, and pieces to move tuple.  Updates the initial location
        with the first item in the pieces to move tuple (the part of the stack not desired to move) appends the second
        part of the pieces to move tuple to the destination list.  Returns the updated instance of the board.
        """
        board = self.get_board()
        board[start[0]][start[1]] = pieces_to_move[0]
        list_of_pieces_to_add = pieces_to_move[1]
        for piece in list_of_pieces_to_add:
            board[destination[0]][destination[1]].append(piece)
        return board

    def get_pieces_to_move(self, coord, num_of_pieces):
        """
        Takes the coordinates of teh stack, and the nubmer of pieces desired to move form that stack, as parameters.
        Splits the stack and returns it in a tuple.
        """
        stack = self.get_stack(coord)
        pieces_to_move = []
        counter = 0
        while counter != num_of_pieces:
            pieces_to_move.insert(0,stack.pop())
            counter += 1
        return stack, pieces_to_move

    def check_valid_move(self, player, start, destination):
        """
        Checks to see if the conditions necessary for the player to move said stack are present.  Returns True or
        False based on the conditions.
        """
        stack = self.get_stack(start)
        if len(stack) > 0 and player.get_player_color() != stack[-1]:
            return False
        if start[0] < 0 or start[0] > 5 or start[1] < 0 or start[1] > 5:
            return False
        if destination[0] < 0 or destination[0] > 5 or destination[1] < 0 or destination[1] > 5:
            return False
        else:
            return True

    def get_stack(self, coord):
        """
        Takes coordinates for the board and returns the list of the stacked pieces at the given location
        """
        board = self.get_board()
        stack = board[coord[0]][coord[1]]
        return stack

    def move_size(self, start, destination):
        """
        Takes a starting and ending location as parameters and then determines and returns how far the player intends to
        move
        """
        vertical_move = abs(start[0] - destination[0])
        horizontal_move = abs(start[1] - destination[1])
        total_move_size = vertical_move + horizontal_move
        return total_move_size

    def get_range(self, coordinates):
        """
        Takes board coordinates as a parameter and counts and returns the number of pieces at the location on the board
        """
        movement_range = 0
        board = self.get_board()
        space = board[coordinates[0]][coordinates[1]]
        for piece in space:
            movement_range += 1
        return movement_range

    def get_active_player(self, player_name):
        """
        Takes a player_name as a parameter and returns the active player based on the player name
        """
        player_one = self.get_player_one()
        player_two = self.get_player_two()

        if player_one.get_player_name() == player_name:
            return player_one
        if player_two.get_player_name() == player_name:
            return player_two
        else:
            return 'player not found'

    def show_pieces(self, coord):
        """
        Takes a board coordinate as a parameter and returns the pieces at the requested location on the board
        """
        return self.get_stack(coord)

    def show_reserve(self, player_name):
        """
        Takes a player name as a parameter and returns how many pieces they have in reserve
        """
        player = self.get_active_player(player_name)
        return player.get_reserve_pieces()

    def show_captured(self, player_name):
        """
        Takes the players name asa parameter and returns the amount of captured pieces
        """
        player = self.get_active_player(player_name)
        return player.get_captured_pieces()

    def reserved_move(self, player_name, coord):
        """
        Takes a players name, and the destination coordinates and determines if they can make a reserve piece move,
        and executes if so.  Updates the turn order.  Returns a message if failed.
        """
        player = self.get_active_player(player_name)
        board = self.get_board()
        if player.get_reserve_pieces() < 1:
            return 'no pieces in reserve'
        board[coord[0]][coord[1]].append(player.get_player_color())
        player.remove_reserve_piece()
        self.set_board(board)
        self.get_next_player(player_name)


class Player:
    """
    A class to represent the individual players for the Focus Game
    """

    def __init__(self, player_name, player_color):
        """
        Initializes with empty captured pieces, reserved pieces, their assigned color, and name.
        """
        self._player_name = player_name
        self._player_color = player_color
        self._reserve_pieces = 0
        self._captured_pieces = 0

    def get_player_name(self):
        """
        Returns players name
        """
        return self._player_name

    def get_player_color(self):
        """
        Returns player color
        """
        return self._player_color

    def get_reserve_pieces(self):
        """
        Returns the number of pieces in player's reserve
        """
        return self._reserve_pieces

    def get_captured_pieces(self):
        """
        Returns the number of the player's captured pieces
        """
        return self._captured_pieces

    def add_reserve_piece(self):
        """
        Adds a piece to the player's reserve pile
        """
        self._reserve_pieces += 1

    def remove_reserve_piece(self):
        """
        Checks to see if there are enough reserve pieces for a move, then removes one if so, if not returns an error
        message
        """
        reserve_pieces = self.get_reserve_pieces()
        if reserve_pieces > 0:
            self._reserve_pieces -= 1
        else:
            return "no pieces in reserve"

    def capture_piece(self):
        """
        Captures a piece for the player
        """
        self._captured_pieces += 1

game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))
game.print_board()
print(game.move_piece('PlayerA',(0,0), (0,1), 1))  #Returns message "successfully moved"
print(game.show_pieces((0,1))) #Returns ['R','R']
print(game.show_captured('PlayerA')) # Returns 0
print(game.reserved_move('PlayerA', (0,0))) # Returns message "No pieces in reserve"
print(game.show_reserve('PlayerA')) # Returns 0