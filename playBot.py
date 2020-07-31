import sys
import random
import signal
import time
import copy
import traceback
# import bot

# We are the max player, the opponent is the min player.

class Team71:

	def __init__(self):
		self.depth = 4
		me = '-'
		opponent = '-'
		start_time = 0
		time_now = 0
		time_stop_it = 23
		inf = 999999999999

	def move(self, board, old_move, flag):
		self.start_time = time.time()
		self.board = copy.deepcopy(board)
		# move function signature specification
		# finding the list of valid cells allowed
		self.set_who_is_who(flag)
		to_send = self.minimax(board, 0, 0, old_move, 0, -999999999999, 999999999999, 0)[1]
		if(to_send[0] == -1):
			self.depth = 1
			to_send = self.minimax(board, 0, 0, old_move, 0, -999999999999, 999999999999, 0)[1]

		if(to_send[0] == -1):
			cells = board.find_valid_move_cells(old_move)
			return cells[random.randrange(len(cells))]

		print("The Chosen Move = ", to_send)
		return to_send	

	def get_beam_length(self, depth):
		# returns the beam width based on the depth
		return 15
		if(depth % 2 == 1):
			return 15
		else:
			return 15

	def win_possibility(self, board, init_x, init_y, turn):

		line = [ [], [], [], [], [], [], [], [], [] ]

		line[0] = [(init_x, init_y), (init_x + 1, init_y), (init_x + 2, init_y)] #top row
		line[1] = [(init_x, init_y + 1), (init_x + 1, init_y + 1), (init_x + 2, init_y + 1)] #middle row
		line[2] = [(init_x, init_y + 2), (init_x + 1, init_y + 2), (init_x + 2, init_y + 2)]	#bottom row
		
		line[3] = [(init_x, init_y), (init_x, init_y + 1), (init_x, init_y + 2)]	#col 1
		line[4] = [(init_x + 1, init_y), (init_x + 1, init_y + 1), (init_x + 1, init_y + 2)]	#col 2
		line[5] = [(init_x + 2, init_y), (init_x + 2, init_y + 1), (init_x + 2, init_y + 2)]	#col 3
		
		line[6] = [(init_x, init_y), (init_x + 1, init_y + 1), (init_x + 2, init_y + 2)] #diag 1
		line[7] = [(init_x, init_y + 2), (init_x + 1, init_y + 1), (init_x + 2, init_y)] #diag 2

		# print("The Opponent here is", turn)
		# print(init_x, init_y)

		count_twos =[0, 0]

		for big_board_number in range (0,2):

			for i in range(0,8):
				count_turn = 0
				flag = 0

				for j in range(0,3):
					# print(big_board_number, line[i][j][0], line[i][j][1], "has a ", board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]])

					if(board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == '-'):
						pass

					elif(board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == turn):
						count_turn += 1
						
					else:
						flag = 1
						break

				if(flag == 1):
					continue

				if(count_turn == 3):
					break

				elif(count_turn == 0):
					pass

				elif(count_turn == 1):
					pass

				elif(count_turn == 2):
					count_twos[big_board_number] += 1

		if(count_twos[0] > 0 and count_twos[1] > 0):
			return (True, True)
		elif(count_twos[0] > 0 and count_twos[1] == 0):
			return (True, False)
		elif(count_twos[0] == 0 and count_twos[1] > 0):
			return (False, True)
		else:
			return (False, False)

	def count_to_win_big(self, board, turn):

		line = [ [], [], [], [], [], [], [], [], [] ]
		init_x = 0
		init_y = 0

		line[0] = [(init_x, init_y), (init_x + 1, init_y), (init_x + 2, init_y)] #top row
		line[1] = [(init_x, init_y + 1), (init_x + 1, init_y + 1), (init_x + 2, init_y + 1)] #middle row
		line[2] = [(init_x, init_y + 2), (init_x + 1, init_y + 2), (init_x + 2, init_y + 2)]	#bottom row
		
		line[3] = [(init_x, init_y), (init_x, init_y + 1), (init_x, init_y + 2)]	#col 1
		line[4] = [(init_x + 1, init_y), (init_x + 1, init_y + 1), (init_x + 1, init_y + 2)]	#col 2
		line[5] = [(init_x + 2, init_y), (init_x + 2, init_y + 1), (init_x + 2, init_y + 2)]	#col 3
		
		line[6] = [(init_x, init_y), (init_x + 1, init_y + 1), (init_x + 2, init_y + 2)] #diag 1
		line[7] = [(init_x, init_y + 2), (init_x + 1, init_y + 1), (init_x + 2, init_y)] #diag 2

		count_to_win = [3, 3]

		for big_board_number in range (0,2):

			count_zeros = 0
			count_ones = 0
			count_twos = 0

			for i in range(0,8):
				count_turn = 0

				flag = 0

				for j in range(0,3):

					if(board.small_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == '-'):
						pass

					elif(board.small_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == turn):
						count_turn = count_turn + 1

					else:
						flag = 1
						break

			if(flag == 1):
				pass

			elif(count_turn == 3):
				count_to_win[big_board_number] = 0

			elif(count_turn == 0):
				pass

			elif(count_turn == 1):
				count_ones = count_ones + 1

			elif(count_turn == 2):
				count_twos = count_twos + 1


			if(count_twos > 0):
				count_to_win[big_board_number] = 1
			elif(count_ones > 0):
				count_to_win[big_board_number] = 2

		return count_to_win

	def count_to_win_it(self, board, init_x, init_y, opponent):

		line = [ [], [], [], [], [], [], [], [], [] ]

		line[0] = [(init_x, init_y), (init_x + 1, init_y), (init_x + 2, init_y)] #top row
		line[1] = [(init_x, init_y + 1), (init_x + 1, init_y + 1), (init_x + 2, init_y + 1)] #middle row
		line[2] = [(init_x, init_y + 2), (init_x + 1, init_y + 2), (init_x + 2, init_y + 2)]	#bottom row
		
		line[3] = [(init_x, init_y), (init_x, init_y + 1), (init_x, init_y + 2)]	#col 1
		line[4] = [(init_x + 1, init_y), (init_x + 1, init_y + 1), (init_x + 1, init_y + 2)]	#col 2
		line[5] = [(init_x + 2, init_y), (init_x + 2, init_y + 1), (init_x + 2, init_y + 2)]	#col 3
		
		line[6] = [(init_x, init_y), (init_x + 1, init_y + 1), (init_x + 2, init_y + 2)] #diag 1
		line[7] = [(init_x, init_y + 2), (init_x + 1, init_y + 1), (init_x + 2, init_y)] #diag 2

		count_to_win = [3, 3]

		for big_board_number in range (0,2):

			count_zeros = 0
			count_ones = 0
			count_twos = 0

			for i in range(0,8):
				count_opponent = 0

				flag = 0

				for j in range(0,3):

					if(board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == '-'):
						pass

					elif(board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == opponent):
						count_opponent = count_opponent + 1

					else:
						flag = 1
						break

			if(flag == 1):
				pass

			elif(count_opponent == 3):
				count_to_win[big_board_number] = 0

			elif(count_opponent == 0):
				pass

			elif(count_opponent == 1):
				count_ones = count_ones + 1

			elif(count_opponent == 2):
				count_twos = count_twos + 1


			if(count_twos > 0):
				count_to_win[big_board_number] = 1
			elif(count_ones > 0):
				count_to_win[big_board_number] = 2

		return count_to_win

	def count_map(self, val):
		if(val == 0):
			return 2000000000

		if(val == 1):
			return 800000

		if(val == 2):
			return 300000

		if(val == 3):
			return 0

		else:
			return 0

	def get_score(self, board, init_x, init_y, opponent):

		board_danger = [0, 0]

		line = [ [], [], [], [], [], [], [], [], [] ]

		line[0] = [(init_x, init_y), (init_x + 1, init_y), (init_x + 2, init_y)] #top row
		line[1] = [(init_x, init_y + 1), (init_x + 1, init_y + 1), (init_x + 2, init_y + 1)] #middle row
		line[2] = [(init_x, init_y + 2), (init_x + 1, init_y + 2), (init_x + 2, init_y + 2)]	#bottom row
		
		line[3] = [(init_x, init_y), (init_x, init_y + 1), (init_x, init_y + 2)]	#col 1
		line[4] = [(init_x + 1, init_y), (init_x + 1, init_y + 1), (init_x + 1, init_y + 2)]	#col 2
		line[5] = [(init_x + 2, init_y), (init_x + 2, init_y + 1), (init_x + 2, init_y + 2)]	#col 3
		
		line[6] = [(init_x, init_y), (init_x + 1, init_y + 1), (init_x + 2, init_y + 2)] #diag 1
		line[7] = [(init_x, init_y + 2), (init_x + 1, init_y + 1), (init_x + 2, init_y)] #diag 2 

		board_done_flag = [0, 0]

		for big_board_number in range (0,2):

			count_blocked = 0
			count_zeros = 0
			count_ones = 0
			count_twos = 0

			for i in range(0,8):
				count_opponent = 0
				count_blanks = 0

				flag = 0

				for j in range(0,3):
					# print(big_board_number, line[i][j][0], line[i][j][1], "has a ", board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]])

					if(board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == '-'):
						count_blanks = count_blanks + 1

					elif(board.big_boards_status[big_board_number][line[i][j][0]][line[i][j][1]] == opponent):
						count_opponent = count_opponent + 1
						
					else:
						flag = 1
						break

				if(flag == 1):
					count_blocked = count_blocked + 1
					continue

				if(count_opponent == 3):
					board_done_flag[big_board_number] = 1
					board_danger[big_board_number] = 0
					break

				elif(count_opponent == 0):
					count_zeros = count_zeros + 1

				elif(count_opponent == 1):
					count_ones = count_ones + 1

				elif(count_opponent == 2):
					count_twos = count_twos + 1

			board_danger[big_board_number] = count_ones * -500 + count_twos * -2000

		if(board_done_flag[0] == 1 and board_done_flag[1] == 1):
			board_danger[0] = -1000000
			board_danger[1] = -1000000

		return board_danger


	def heuristic(self, board):
		grid_a = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
		grid_b = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]

		final_heuristic = 0

		for i in [0, 3, 6]:
			for j in [0, 3, 6]:
				saved_values_opponent = self.get_score(board, i, j, self.opponent)
				saved_values_player = self.get_score(board, i, j, self.me)

				grid_a[i/3][j/3] = saved_values_opponent[0]  - saved_values_player[0]
				grid_b[i/3][j/3] = saved_values_opponent[1]  - saved_values_player[1]

				if(board.small_boards_status[0][i/3][j/3] == self.me):
					grid_a[i/3][j/3] = 10000

				if(board.small_boards_status[0][i/3][j/3] == self.opponent):
					grid_a[i/3][j/3] = -10000

				if(board.small_boards_status[1][i/3][j/3] == self.me):
					grid_b[i/3][j/3] = 10000

				if(board.small_boards_status[1][i/3][j/3] == self.opponent):
					grid_b[i/3][j/3] = -10000

				final_heuristic = final_heuristic + grid_a[i/3][j/3] + grid_b[i/3][j/3]

		grid_a_player = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
		grid_b_player = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]

		grid_a_opponent = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]
		grid_b_opponent = [ [0, 0, 0], [0, 0, 0], [0, 0, 0] ]

		for i in [0, 3, 6]:
			for j in [0, 3, 6]:
				saved_player = self.count_to_win_it(board, i, j, self.me)
				saved_opponent = self.count_to_win_it(board, i, j, self.opponent)

				grid_a_player[i/3][j/3] = saved_player[0]
				grid_b_player[i/3][j/3] = saved_player[1]

				grid_a_opponent[i/3][j/3] = saved_opponent[0]
				grid_a_opponent[i/3][j/3] = saved_opponent[1]

		line_a_player = [0, 0, 0, 0, 0, 0, 0, 0]
		line_a_opponent = [0, 0, 0, 0, 0, 0, 0, 0]

		line_b_player = [0, 0, 0, 0, 0, 0, 0, 0]
		line_b_opponent = [0, 0, 0, 0, 0, 0, 0, 0]

		line_a_player[0] = grid_a_player[0][0] + grid_a_player[0][1] + grid_a_player[0][2] #row 1
		line_a_player[1] = grid_a_player[1][0] + grid_a_player[1][1] + grid_a_player[1][2] #row 2
		line_a_player[2] = grid_a_player[2][0] + grid_a_player[2][1] + grid_a_player[2][2] #row 3
		line_a_player[3] = grid_a_player[0][0] + grid_a_player[1][0] + grid_a_player[2][0] #col 1
		line_a_player[4] = grid_a_player[0][1] + grid_a_player[1][1] + grid_a_player[2][1] #col 2
		line_a_player[5] = grid_a_player[0][2] + grid_a_player[1][2] + grid_a_player[2][2] #col 3
		line_a_player[6] = grid_a_player[0][0] + grid_a_player[1][1] + grid_a_player[2][2] #diag 1
		line_a_player[7] = grid_a_player[0][2] + grid_a_player[1][1] + grid_a_player[2][0] #diag 2

		line_b_player[0] = grid_b_player[0][0] + grid_b_player[0][1] + grid_b_player[0][2] #row 1
		line_b_player[1] = grid_b_player[1][0] + grid_b_player[1][1] + grid_b_player[1][2] #row 2
		line_b_player[2] = grid_b_player[2][0] + grid_b_player[2][1] + grid_b_player[2][2] #row 3
		line_b_player[3] = grid_b_player[0][0] + grid_b_player[1][0] + grid_b_player[2][0] #col 1
		line_b_player[4] = grid_b_player[0][1] + grid_b_player[1][1] + grid_b_player[2][1] #col 2
		line_b_player[5] = grid_b_player[0][2] + grid_b_player[1][2] + grid_b_player[2][2] #col 3
		line_b_player[6] = grid_b_player[0][0] + grid_b_player[1][1] + grid_b_player[2][2] #diag 1
		line_b_player[7] = grid_b_player[0][2] + grid_b_player[1][1] + grid_b_player[2][0] #diag 2

		line_a_opponent[0] = grid_a_opponent[0][0] + grid_a_opponent[0][1] + grid_a_opponent[0][2] #row 1
		line_a_opponent[1] = grid_a_opponent[1][0] + grid_a_opponent[1][1] + grid_a_opponent[1][2] #row 2
		line_a_opponent[2] = grid_a_opponent[2][0] + grid_a_opponent[2][1] + grid_a_opponent[2][2] #row 3
		line_a_opponent[3] = grid_a_opponent[0][0] + grid_a_opponent[1][0] + grid_a_opponent[2][0] #col 1
		line_a_opponent[4] = grid_a_opponent[0][1] + grid_a_opponent[1][1] + grid_a_opponent[2][1] #col 2
		line_a_opponent[5] = grid_a_opponent[0][2] + grid_a_opponent[1][2] + grid_a_opponent[2][2] #col 3
		line_a_opponent[6] = grid_a_opponent[0][0] + grid_a_opponent[1][1] + grid_a_opponent[2][2] #diag 1
		line_a_opponent[7] = grid_a_opponent[0][2] + grid_a_opponent[1][1] + grid_a_opponent[2][0] #diag 2

		line_b_opponent[0] = grid_b_opponent[0][0] + grid_b_opponent[0][1] + grid_b_opponent[0][2] #row 1
		line_b_opponent[1] = grid_b_opponent[1][0] + grid_b_opponent[1][1] + grid_b_opponent[1][2] #row 2
		line_b_opponent[2] = grid_b_opponent[2][0] + grid_b_opponent[2][1] + grid_b_opponent[2][2] #row 3
		line_b_opponent[3] = grid_b_opponent[0][0] + grid_b_opponent[1][0] + grid_b_opponent[2][0] #col 1
		line_b_opponent[4] = grid_b_opponent[0][1] + grid_b_opponent[1][1] + grid_b_opponent[2][1] #col 2
		line_b_opponent[5] = grid_b_opponent[0][2] + grid_b_opponent[1][2] + grid_b_opponent[2][2] #col 3
		line_b_opponent[6] = grid_b_opponent[0][0] + grid_b_opponent[1][1] + grid_b_opponent[2][2] #diag 1
		line_b_opponent[7] = grid_b_opponent[0][2] + grid_b_opponent[1][1] + grid_b_opponent[2][0] #diag 2


		for i in range (0, 8):
			final_heuristic = final_heuristic + (9 - line_a_player[i]) * 5000 + (9 - line_b_player[i]) * 5000 - (9 - line_a_opponent[i]) * 5000 - (9 - line_b_opponent[i]) * 5000

		count_win_me_a, count_win_me_b = self.count_to_win_big(board, self.me)
		count_win_opponent_a, count_win_opponent_b = self.count_to_win_big(board, self.opponent)

		final_heuristic = final_heuristic - self.count_map(count_win_opponent_a) - self.count_map(count_win_opponent_b) + (self.count_map(count_win_me_a) + self.count_map(count_win_me_b)) * 1
		if(count_win_me_a == 0 or count_win_me_b == 0):
			final_heuristic = 2000000000000
		elif(count_win_opponent_a == 0 or count_win_opponent_b == 0):
			final_heuristic = -2000000000000

		return final_heuristic


	def utility(self, board, last_move, player, carry):
		# BigBoard board
		temp = self.heuristic(board)

		init_x = last_move[1] % 3;
		init_y = last_move[2] % 3;

		[score_board_a, score_board_b] = [0, 0]

		if(player == 0):
			score_board_a, score_board_b = self.get_score(board, init_x * 3, init_y * 3, self.opponent)
		else:
			score_board_a, score_board_b = self.get_score(board, init_x * 3, init_y * 3, self.me)

		factor = 10
		if(player == 1):
			factor = -10

		consider = 0

		if(player == 0 and self.count_to_win_it(board, init_x * 3, init_y * 3, self.opponent) == 1):
			consider = -375000

		elif(player == 0 and self.count_to_win_it(board, init_x * 3, init_y * 3, self.opponent) == 2):
			consider = -15000

		elif(player == 1 and self.count_to_win_it(board, init_x * 3, init_y * 3, self.me) == 1):
			consider = 375000

		elif(player == 1 and self.count_to_win_it(board, init_x * 3, init_y * 3, self.me) == 2):
			consider = 15000

		return (score_board_a + score_board_b) * factor + temp + consider + carry

	def set_who_is_who(self, flag):
		if(flag == 'x'):
			self.me = 'x'
			self.opponent = 'o'

		else:
			self.me = 'o'
			self.opponent = 'x'

	def minimax(self, board, current_depth, player, last_move, bonus_flag, alpha, beta, last_recur_value):
		# BigBoard board
		# int current_depth
		# int player
		# (int, int, int) last_move

		# player 0 -> Our Move
		# player 1 -> Opponent's Move
		

		self.time_now = time.time()
		if(current_depth == self.depth or board.find_terminal_state()[0] != 'CONTINUE' or (self.time_now - self.start_time) >= 20):
			# ((self.time_now - self.start_time) >= 22)
			return (self.utility(board, last_move, player, last_recur_value), last_move)

		if(player == 0):
			# maximising player
			best_value = -999999999999
			best_move = (-1, -1, -1)
			child_nodes = board.find_valid_move_cells(last_move)
			count = len(child_nodes)

			child_nodes_util = []
			
			for node in child_nodes:
				recurrent_value = last_recur_value / 2

				new_board = copy.deepcopy(board)
				new_board.big_boards_status = copy.deepcopy(board.big_boards_status)
				new_board.small_boards_status = copy.deepcopy(board.small_boards_status)

				open_move_value = 0


				small_board_check_y = node[1] % 3
				small_board_check_x = node[2] % 3
				
				count_to_win_before = self.count_to_win_it(new_board, small_board_check_y * 3, small_board_check_x * 3, self.opponent)
				_, win_flag = new_board.update(last_move, node, self.me)
				count_to_win_after = self.count_to_win_it(new_board, small_board_check_y * 3, small_board_check_x * 3, self.opponent)
				improve = count_to_win_after[node[0]] - count_to_win_before[node[0]]
				if(improve > 0):
					recurrent_value = recurrent_value + 375000 * improve 

				if(new_board.find_terminal_state()[1] == 'WON' and new_board.find_terminal_state()[0] == self.me):
					recurrent_value = recurrent_value + 1000000000

				if(new_board.small_boards_status[0][small_board_check_y][small_board_check_x] != '-' and new_board.small_boards_status[1][small_board_check_y][small_board_check_x] != '-'):
					open_move_value = -1000000

				add_value = 0

				if(bonus_flag == 0 and win_flag == True):
					add_value = 375000
					bonus_flag = 1
					open_move_value = 1000000

				elif(bonus_flag == 2):
					bonus_flag = 0
				
				truth_values = self.win_possibility(new_board, ((node[1] % 3) * 3), ((node[2] % 3) * 3), self.me)
				
				if(truth_values[0] == True or truth_values[1] == True):
					recurrent_value = recurrent_value - 200000 + add_value + open_move_value
					child_nodes_util.append([node, new_board, self.utility(new_board, node, player, recurrent_value), recurrent_value])

				else:
					recurrent_value = recurrent_value + add_value + open_move_value
					child_nodes_util.append([node, new_board, self.utility(new_board, node, player, recurrent_value), recurrent_value])

			child_nodes_util = sorted(child_nodes_util, key = lambda x: x[2], reverse = True)

			track = 0
			limit = self.get_beam_length(current_depth)

			for element in child_nodes_util:
				value = 0
				if(bonus_flag == 1):
					value = self.minimax(element[1], current_depth + 1, 0, element[0], 2, alpha, beta, element[3])[0]
				else:
					value = self.minimax(element[1], current_depth + 1, 1, element[0], 0, alpha, beta, element[3])[0]

				best_value = max(best_value, value)
				if(current_depth == 0):
					print("level : ", current_depth, "player : ", player, "current_move : ", element[0], "heuristic : ", best_value)
				if(best_value == value):
					best_move = element[0]

				alpha = max(alpha, best_value)
				if(beta <= alpha):
					break

				track = track + 1
				if(track > limit):
					break

			#print (best_value, best_move)
			return (best_value, best_move)


		if(player == 1):
			best_value = 999999999999
			best_move = (-1, -1, -1)
			child_nodes = board.find_valid_move_cells(last_move)
			count = len(child_nodes)

			child_nodes_util = []

			for node in child_nodes:
				recurrent_value = last_recur_value / 2

				new_board = copy.deepcopy(board)
				new_board.big_boards_status = copy.deepcopy(board.big_boards_status)
				new_board.small_boards_status = copy.deepcopy(board.small_boards_status)

				open_move_value = 0

				small_board_check_y = node[1] % 3
				small_board_check_x = node[2] % 3

				count_to_win_before = self.count_to_win_it(new_board, small_board_check_y * 3, small_board_check_x * 3, self.me)
				_, win_flag = new_board.update(last_move, node, self.me)
				count_to_win_after = self.count_to_win_it(new_board, small_board_check_y * 3, small_board_check_x * 3, self.me)
				improve = count_to_win_after[node[0]] - count_to_win_before[node[0]]
				if(improve > 0):
					recurrent_value = recurrent_value - 375000 * improve 


				if(new_board.find_terminal_state()[1] == 'WON' and new_board.find_terminal_state()[0] == self.opponent):
					recurrent_value = recurrent_value - 1000000000

				if(new_board.small_boards_status[0][small_board_check_y][small_board_check_x] != '-' and new_board.small_boards_status[1][small_board_check_y][small_board_check_x] != '-'):
					open_move_value = 1000000

				add_value = 0

				if(bonus_flag == 0 and win_flag == True):
					add_value = -375000
					bonus_flag = 1
					open_move_value = -1000000

				truth_values = self.win_possibility(new_board, ((node[1] % 3) * 3), ((node[2] % 3) * 3), self.opponent)
				if(truth_values[0] == True or truth_values[1] == True):
					recurrent_value = recurrent_value + 200000 + add_value + open_move_value
					child_nodes_util.append([node, new_board, self.utility(new_board, node, player, recurrent_value), recurrent_value])

				else:
					recurrent_value = recurrent_value + add_value + open_move_value
					child_nodes_util.append([node, new_board, self.utility(new_board, node, player, recurrent_value), recurrent_value])


			child_nodes_util = sorted(child_nodes_util, key = lambda x: x[2]) #changing the reversal
			track = 0
			limit = self.get_beam_length(current_depth)

			for element in child_nodes_util:
				value = 0
				if(bonus_flag == 1):
					value = self.minimax(element[1], current_depth + 1, 1, element[0], 2, alpha, beta, element[3])[0]
				else:
					value = self.minimax(element[1], current_depth + 1, 0, element[0], 0, alpha, beta, element[3])[0]
				#element[0] is the node

				best_value = min(best_value, value)
				if(best_value == value):
					if(current_depth == 0):
						print("level : ", current_depth, "player : ", player, "current_move : ", element[0], "heuristic : ", best_value)
					best_move = element[0]

				beta = min(beta, best_value)

				if(beta <= alpha):
					break

				track = track + 1
				if(track > limit):
					break

			return (best_value, best_move)
			