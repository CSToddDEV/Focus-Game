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
        # Get the game board
        board = self.get_board()
        # Get player one
        player_one = self.get_player_one()
        # Get player two
        player_two = self.get_player_two()

        # Initialize the counter for alternating the board colors to 0
        counter = 0
        # Get the color for the first player
        color = player_one.get_player_color()

        # Iterate through each row in the board
        for row in board:
                # Iterate through each space in each row on the board
                for space in row:
                    # If the counter for alternating board counters is 2 and the color is that of player one's color
                    # Then change the color to player 2's color and set the alternating color counter to 0
                    if counter == 2 and color == player_one.get_player_color():
                        color = player_two.get_player_color()
                        counter = 0
                    # If the counter for alternating board counters is 2 and the color is that of player two's color
                    # Then change the color to player 1's color and set the alternating color counter to 0
                    if counter == 2 and color == player_two.get_player_color():
                        color = player_one.get_player_color()
                        counter = 0
                    # Add the color of the player to position 0 of the corresponding list on the corresponding
                    # space on the game board
                    space.append(color)
                    # Increase the alternating color counter.
                    counter += 1
        # Call the set_board function to update the FocusGame._board data member.
        self.set_board(board)

    def move_piece(self, player_name, start, destination, num_of_pieces):
        """
        Method for the movement of pieces.  Takes a player_name, start location, destination location, and the number
        of pieces desired to move as parameters.  move_piece will check the validity of the move and then make the
        appropriate move depending on whether it is a single move or multiple move.  Will update the board, and captured
        and reserved pieces and finally check win conditions.  This will all lead in to updating the next turn for
        the FocusGame and returning the appropriate message
        """
        # Get and store what player's turn it is supposed to be
        turn = self.get_turn()
        # Retrieve and store player object based on player's name
        player = self.get_active_player(player_name)
        # Get and store the proposed Move size (in spaces) based on the given starting and ending location
        move_size = self.move_size(start, destination)
        # Check to see if the move meets the following criteria: The player can move the stack because their piece is on
        # the top of the stack (the last piece on the list at the location), and that the move does not originate or
        # have a destination off the board.  Call the valid_move function for this.
        valid_move = self.check_valid_move(player, start, destination)
        # Split the stack in to pieces that are going to stay in the spot, and pieces that are going to move to the
        # new location.  Call the get_pieces_to_move function for this.
        pieces_to_move = self.get_pieces_to_move(start, num_of_pieces)

        # If it is not the first turn (ie. turn does not equal None) and not the player's turn then return
        # 'not your turn'
        if turn != player and turn != None:
            return 'not your turn'

        # If the amount of pieces in the stack that the player wants to move is less than the range the want to move
        # the pieces, return the error 'invalid number of pieces'
        if num_of_pieces != move_size:
            return 'invalid number of pieces'

        # If the the valid_move function returns false, return 'invalid location'
        if valid_move is False:
            return 'invalid location'

        # Update the starting and destination locations for the game board
        board = self.update_board_location(start, destination, pieces_to_move)
        # Process the stack on the destination board square if the stack if over 5 pieces.
        # Check win conditions.
        board = self.process_stack(board, destination, player)

        # Check to see if the win condition has been met.  If it has, return 'Wins'
        if self.get_winner() is not None:
            return 'Wins'

        else:
            # Update the game board
            self.set_board(board)
            # Set the next player to move
            self.get_next_player(player)
            # Return the 'Successfully moved' message
            return 'successfully moved'

    def get_next_player(self, player):
        """
        Takes a player object as a parameter and updates the FocusGame ._turn data field to whose turn it will be next.
        """
        # Get the player objects
        player_one = self.get_player_one()
        player_two = self.get_player_two()
        # If the passed player object matches player one, then set the turn to player two
        if player_one.get_player_name() == player.get_player_name():
            self.set_turn(player_two.get_player_name())
        else:
            # Else set the turn to player one
            self.set_turn(player_one.get_player_name())

    def process_stack(self, board, destination, player):
        """
        Takes the stack post player move and processes it.  Captures enemy pieces and gets reserve pieces if the size of
        the stack is more than five pieces.  Updates the current board and returns it to the calling function.
        """
        # Get the nested list at the location on the game board and store it in stack
        stack = board[destination[0]][destination[1]]
        # If the list that is stack has more than 5 items (or pieces) in it:
        while len(stack) > 5:
            # The bottom piece of the stack is represented by the piece at index 0.
            piece = stack[0]
            # If the piece matches the player whose turn it is color, then increase the players reserved pieces by 1.
            if piece == player.get_player_color():
                player.add_reserve_piece()
            # If the piece does not match the player whose turn it is, then capture the piece.
            else:
                player.capture_piece()
            # Remove the piece from the bottom of the stack (index 0) and return to the top of the of the loop if the
            # "stack" still has more than 5 items in it.
            stack = stack[1:]

        # Return the updated stack of 5 to the board
        board[destination[0]][destination[1]] = stack

        # Check the player whose turn it is win conditions
        self.check_win_conditions(player)

        # Return the updated board.
        return board

    def check_win_conditions(self, player):
        """
        Takes a player object as the parameter and checks to see if the player has met the win conditions, updates the
        ._winner data member if so.
        """
        # Check the win condition.  If the player has 6 or more captured pieces, set the FocusGame._winner to them.
        if player.get_captured_pieces() > 5:
            self.set_winner(player)

    def update_board_location(self, start, destination, pieces_to_move):
        """
        Takes the starting location tuple, destination tuple, and pieces to move tuple.  Updates the initial location
        with the first item in the pieces to move tuple (the part of the stack not desired to move) appends the second
        part of the pieces to move tuple to the destination list.  Returns the updated instance of the board.
        """
        # Get the game board
        board = self.get_board()
        # Update the location of the starting move with the first half of the tuple of pieces_to_move which represent
        # the pieces that are staying at the location on the board.
        board[start[0]][start[1]] = pieces_to_move[0]
        # Append the second half of the pieces_to_move tuple to the destination list representing the pieces that were
        # were intended to move being stacked on the destination location.
        list_of_pieces_to_add = pieces_to_move[1]
        for piece in list_of_pieces_to_add:
            board[destination[0]][destination[1]].append(piece)
        # Return the updated board
        return board

    def get_pieces_to_move(self, coord, num_of_pieces):
        """
        Takes the coordinates of teh stack, and the nubmer of pieces desired to move form that stack, as parameters.
        Splits the stack and returns it in a tuple.
        """
        # Get and store the stack at the requested coordinates
        stack = self.get_stack(coord)
        # Initialize a list of the pieces that are intended to be moved
        pieces_to_move = []
        # Set counter to 0
        counter = 0
        # If the counter does not equal the number_of_pieces requested to be moved, continue
        while counter != num_of_pieces:
            # take the last item of the list, representing the player piece on top of the stack, and move it to the
            # bottom of the pieces_to_move stack
            pieces_to_move.insert(0, stack.pop())
            # increase the counter for the amount of pieces moved
            counter += 1
        # Return the a tuple of the now modified original stack and the a list of the pieces to move to the calling
        # functions.
        return stack, pieces_to_move

    def check_valid_move(self, player, start, destination):
        """
        Checks to see if the conditions necessary for the player to move said stack are present.  Returns True or
        False based on the conditions.
        """
        # Get stack at desired location
        stack = self.get_stack(start)
        # Make sure the player's piece is the one on the top of the stack by checking the last item in the list at the
        # requested location, which represents the piece on the top of the stack.  If not their piece, return False.
        if len(stack) > 0 and player.get_player_color() != stack[-1]:
            return False
        # If requested starting location is off the board return False
        if start[0] < 0 or start[0] > 5 or start[1] < 0 or start[1] > 5:
            return False
        # If the requested destination is off the board return False
        if destination[0] < 0 or destination[0] > 5 or destination[1] < 0 or destination[1] > 5:
            return False
        # Else it is a valid move and return True
        else:
            return True

    def get_stack(self, coord):
        """
        Takes coordinates for the board and returns the list of the stacked pieces at the given location
        """
        # Get the current game board
        board = self.get_board()
        # Get the list of pieces at the requested location
        stack = board[coord[0]][coord[1]]
        # return the list of the requested pieces
        return stack

    def move_size(self, start, destination):
        """
        Takes a starting and ending location as parameters and then determines and returns how far the player intends to
        move
        """
        # Get the amount of spaces moved vertically
        vertical_move = abs(start[0] - destination[0])
        # Get the amount of spaces moved horizontally
        horizontal_move = abs(start[1] - destination[1])
        # Add the two numbers together to get the total number of spaces moved
        total_move_size = vertical_move + horizontal_move
        # Return the total number of "spaces" moved
        return total_move_size

    def get_active_player(self, player_name):
        """
        Takes a player_name as a parameter and returns the active player based on the player name
        """
        # Get player objects
        player_one = self.get_player_one()
        player_two = self.get_player_two()

        # If passed player name equals player one
        if player_one.get_player_name() == player_name:
            # Return player one
            return player_one
        # If passed player name equals player two
        if player_two.get_player_name() == player_name:
            # Return player two
            return player_two
        else:
            # If it doesn't match either return 'player not found'
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
        # Get active player
        player = self.get_active_player(player_name)
        # Get current board
        board = self.get_board()
        # Check to see if player has reserve pieces, if not return 'no pieces in reserve'
        if player.get_reserve_pieces() < 1:
            return 'no pieces in reserve'
        # Add a piece of the players color to the end of the nested list specified, representing putting a piece on the
        # top of the stack
        board[coord[0]][coord[1]].append(player.get_player_color())
        # Decrement the players reserve piece count by one
        player.remove_reserve_piece()
        # Update current board
        self.set_board(board)
        # Set the next player's turn
        self.get_next_player(player_name)
        # Return "successfully moved' if everything works.
        return 'successfully moved'


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
        # Increases the Player._reserve_pieces count by one
        self._reserve_pieces += 1

    def remove_reserve_piece(self):
        """
        Checks to see if there are enough reserve pieces for a move, then removes one if so, if not returns an error
        message
        """
        # Decrement the Player._reserved_pieces count by one
        self._reserve_pieces -= 1

    def capture_piece(self):
        """
        Captures a piece for the player
        """
        # Increase the Player._captured_pieces count by one
        self._captured_pieces += 1

game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))
game.print_board()
print(game.move_piece('PlayerA',(0,0), (0,1), 1))  #Returns message "successfully moved"
print(game.show_pieces((0,1))) #Returns ['R','R']
print(game.show_captured('PlayerA')) # Returns 0
print(game.reserved_move('PlayerA', (0,0))) # Returns message "No pieces in reserve"
print(game.show_reserve('PlayerA')) # Returns 0