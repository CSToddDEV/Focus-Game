# Author: Calvin Todd
# Date: 11.19.20
# Description: Assignment 9/Portfolio Project where we create a representation of the game Domination!

class FocusGame:
    """
    The main class to represent the board, player moves, and win conditions for the Focus Game.
    """

    def __init__(self, player_one, player_two):
        """
        Initializes the FocusGame class with a new board, player names, other data members
        """
        self._player_one = Player(player_one[0], player_one[1])
        self._player_one_name = player_one[0]
        self._player_one_color = player_one[1]
        self._player_two = Player(player_two[0], player_two[1])
        self._player_two_name = player_two[0]
        self._player_two_color = player_two[1]
        self._turn = None
        self._winner = None
        self._board =[[[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []],
                      [[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []]]
        self.initialize_game()

    def get_board(self):
        """
        Returns Focus Game Board
        """
        return self._board

    def set_board(self, board):
        """
        Updates the board
        """
        self._board = board

    def get_player_one(self):
        """
        Returns Player One
        """
        return self._player_one

    def get_player_two(self):
        """
        Returns Player Two
        """
        return self._player_two

    def get_turn(self):
        """
        Returns the current turn
        """
        return self._turn

    def set_turn(self, player):
        """
        Sets the current turn to the inputted player
        """
        self._turn = player

    def get_winner(self):
        """
        Returns the current winner
        """
        return self._winner

    def set_winner(self, player):
        """
        Sets the winner to the inputted player
        """
        self._winner = player

    def print_board(self):
        """
        Print board for testing purposes
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
        Initializes the board with player pieces
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
        Method for the movement of pieces, returns various messages depending on the outcome
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
        Get the player whose turn it is next and sets the next turn to them
        """
        player_one = self.get_player_one()
        player_two = self.get_player_two()
        if player_one.get_player_name() == player.get_player_name():
            self.set_turn(player_two.get_player_name())
        else:
            self.set_turn(player_one.get_player_name())

    def process_stack(self, board, destination, player):
        """
        Processes the stack for the player if it is more than 5 pieces on the stack, returns the board
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
        Checks to see if the player has met the win conditions
        """
        if player.get_captured_pieces() > 5:
            self.set_winner(player)

    def update_board_location(self, start, destination, pieces_to_move):
        """
        Updates the board with players move
        """
        board = self.get_board()
        board[start[0]][start[1]] = pieces_to_move[0]
        list_of_pieces_to_add = pieces_to_move[1]
        for piece in list_of_pieces_to_add:
            board[destination[0]][destination[1]].append(piece)
        return board

    def get_pieces_to_move(self, coord, num_of_pieces):
        """
        Gets the amount of pieces to remove and returns a tuple of lists of the pieces staying, and the pieces
        moving
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
        Checks to see if the player may move the stack
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
        Returns the list of the stacked pieces at the given location
        """
        board = self.get_board()
        stack = board[coord[0]][coord[1]]
        return stack

    def move_size(self, start, destination):
        """
        Determines and returns how far the player intends to move
        """
        vertical_move = abs(start[0] - destination[0])
        horizontal_move = abs(start[1] - destination[1])
        total_move_size = vertical_move + horizontal_move
        return total_move_size

    def get_range(self, coordinates):
        """
        Counts and returns the number of pieces at the location on the board
        """
        movement_range = 0
        board = self.get_board()
        space = board[coordinates[0]][coordinates[1]]
        for piece in space:
            movement_range += 1
        return movement_range

    def get_active_player(self, player_name):
        """
        Returns the active player based on the player name
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
        Shows the pieces at the requested location on the board
        """
        return self.get_stack(coord)

    def show_reserve(self, player_name):
        """
        Takes a player name and shows how many pieces they have in reserve
        """
        player = self.get_active_player(player_name)
        return player.get_reserve_pieces()

    def show_captured(self, player_name):
        """
        Takes the players name and returns the amount of captured pieces
        """
        player = self.get_active_player(player_name)
        return player.get_captured_pieces()

    def reserved_move(self, player_name, coord):
        """
        Makes a reserve move if possible for the player
        """
        player = self.get_active_player(player_name)
        board = self.get_board()
        if player.get_reserve_pieces() < 1:
            return 'no pieces in reserve'
        board[coord[0]][coord[1]].append(player.get_player_color())
        player.remove_reserve_piece()
        self.set_board(board)


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
        Returns the number of pieces in rserve
        """
        return self._reserve_pieces

    def get_captured_pieces(self):
        """
        Returns the number of captured pieces
        """
        return self._captured_pieces

    def add_reserve_piece(self):
        """
        Adds a piece to the reserve pile
        """
        self._reserve_pieces += 1

    def remove_reserve_piece(self):
        """
        Checks to see if there are enough reserve pieces, then removes one if if so
        """
        reserve_pieces = self.get_reserve_pieces()
        if reserve_pieces > 0:
            self._reserve_pieces -= 1
        else:
            return "no pieces in reserve"

    def capture_piece(self):
        """
        Captures a piece
        """
        self._captured_pieces += 1

game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))
game.print_board()
print(game.move_piece('PlayerA',(0,0), (0,1), 1))  #Returns message "successfully moved"
print(game.show_pieces((0,1))) #Returns ['R','R']
print(game.show_captured('PlayerA')) # Returns 0
print(game.reserved_move('PlayerA', (0,0))) # Returns message "No pieces in reserve"
print(game.show_reserve('PlayerA')) # Returns 0