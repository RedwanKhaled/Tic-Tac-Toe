import random,os


states = []
gameStates = []
v = []
Move = [1,2]
board = [0,0,0,0,0,0,0,0,0]
Sign = [' ','X','O']


def FeedInput(player):
	
	for i in range(0,9):
		new_board = [0,0,0,0,0,0,0,0,0]
		new_board[i] = Move[player]
		states[player].append(new_board[:])
		v[player].append(0.5)
	for i in range(0,9):
		new_board = [0,0,0,0,0,0,0,0,0]
		new_board[i] = Move[changePlayer(player)]
		states[player].append(new_board[:])
		v[player].append(0.5)


def changePlayer(player):
	
	if player==1:
		return 0
	else:
		return 1

def _gameOver(board,one,two,three):
	
	if board[one] == board[two] and board[two] == board[three]:	return 1
	else:	return 0


def gameOver(board,player):


	if board[0] == Move[player]:
	
		if _gameOver(board,0,1,2): return 1
		elif _gameOver(board,0,4,8): return 1
		elif _gameOver(board,0,3,6): return 1
		
	
	if board[2] == Move[player]:
		if _gameOver(board,2,5,8): return 1
		elif _gameOver(board,2,4,6): return 1
		
	if board[3] == Move[player]:
		if _gameOver(board,3,4,5): return 1
	
	if board[6] == Move[player]:
		if _gameOver(board,6,7,8): return 1
	
	if board[1] == Move[player]:
		if _gameOver(board,1,4,7): return 1
	
	
	available_move = getAvailableMove(board)
	if len(available_move) == 0:
		return -1
	
	return 0

def getAvailableMove(board):

	move = []
	for i in range(0,9):
		if board[i]!=1 and board[i]!=2:
			move.append(i)
	
	return move



def getGreedyMove(board,player):

	max_index = -1
	if len(v[player])>0:
		
		new_board = board
		max_value = 0
		for i in range(0,9):
			if board[i]==0:
				new_board[i] = Move[player]

				if new_board[:] in states[player]:
					board_index = states[player].index(new_board[:])
					value_index = v[player][board_index]

				else:
					states[player].append(new_board[:])
					v[player].append(0.5)
					value_index = 0.5

				if value_index > max_value:
					max_value = value_index
					index = i

				new_board[i] = 0

		return max_index
		#get_max = max(v[player])
		#print "get_max: ",get_max 
		#index = v[player].index(get_max)
		#new_board = states[player][index]
		#print "board : ",new_board
		#max1 = -100
		#new_move = []
		#for i in range(0,9):
		#	if new_board[i] == Move[player]:
		#		if board[i] == 0:
					#new_board2 = board
					#new_board2[i] = Move[player]
					
					#if states[player].count(new_board2)>0:
					#	value = states[player].index(new_board2)
					#else: 
					#	if value > max1:
					#		max1 = value
					#		max_index = i
		#			new_move.append(i)
		
		#if len(new_move) == 0:
		#	return -1
		#return new_move[random.randint(0,len(new_move)-1)]
	return max_index

def getRandomMove(nextMove):
	
	value = random.randint(0,len(nextMove)-1)
	return nextMove[value]
	

def gamePlay(board,player,ex):
	
	win = gameOver(board,player)
	win1 = gameOver(board,changePlayer(player))
	
	if win == 1 or win == -1:
		#print "Done"
		return
	if win1 == 1 or win1 == -1:
		#print "Done"
		return 
	
	
	
	nextMove = getAvailableMove(board)
	
	random_value = random.random()

	if random_value <= ex:
		index = getRandomMove(nextMove)
	else:
		index = getGreedyMove(board,player)
	
	#print index
	if states[player].count(board[:])==0:
		states[player].append(board[:])
		v[player].append(0.5)
	
	board[index] = Move[player]
	#print board
	#print type(board)
	
	if states[player].count(board[:])==0:
		states[player].append(board[:])
		v[player].append(0.5)
	#print "working ",player," ",states[player]
	
	#print "player ",player,board
	#if player == 1: print "------------------------------"
	gameStates[player].append(board[:])
	
	gamePlay(board,changePlayer(player),ex)



def updateValue(player,win):

	value = 0
	if win==1:
		value = 1
	elif win == -1:
		value = 0.5
	
	while len(gameStates[player])>0:
		
		new_board = gameStates[player].pop();
		
		index = states[player].index(new_board[:])
		
		previous = v[player][index]
		update  = previous + 0.01*(value - previous)
		v[player][index] = update
		
		
	
def print_data(player):

	
	#for i in range(0,len(v[player])):
	#	print states[player][i],v[player][i]
	#print
	print len(states[player])


def print_board(board):
	
	print " ",0 if board[0]==0 else Sign[board[0]],"|",1 if board[1]==0 else Sign[board[1]],"|",2 if board[2]==0 else Sign[board[2]]
	print "","-----------"
	print " ",3 if board[3]==0 else Sign[board[3]],"|",4 if board[4]==0 else Sign[board[4]],"|",5 if board[5]==0 else Sign[board[5]]
	print "","-----------"
	print " ",6 if board[6]==0 else Sign[board[6]],"|",7 if board[7]==0 else Sign[board[7]],"|",8 if board[8]==0 else Sign[board[8]]
	

def writeToFile(filename):

	fp = open(filename,'w')
	length = len(states[0])
	for i in range(0,length):
		st = ''
		x = states[0][i]
		for j in range(0,9):
			st = st + str(x[j])
			if j!=8: st+=','
		fp.write("%s %s\n" %(st,str(v[0][i])))
	fp.close()

def ComputerMove(board,player):

	nextMove = getAvailableMove(board)
	#print nextMove
	index = getGreedyMove(board,player)
	
	if index == -1:
		index = getRandomMove(nextMove)
	
	#print index
		
	board[index] = Move[player]
	
	if states[player].count(board[:])==0:
		states[player].append(board[:])
		v[player].append(0.5)
	
	gameStates[player].append(board[:])
	
	
def HumanMove(board,player):

	print_board(board)

	x = int(raw_input('Your Move(put position): '))
	#print board
	while board[x]!=0:
		print "Invalid input"
		x = int(raw_input("Put position: "))

	board[x] = Move[player]


def load_File(fp):

	while True:
		line = fp.readline()
		if line == "":
		    break
		first_split = line.split(' ')
		state = map(int,first_split[0].split(','))
		value = float(first_split[1])
		states[0].append(state)
		v[0].append(value)
	    #totalStates = totalStates + 1


states.append([])	#creating two dimensional state list
states.append([])
v.append([])		
v.append([])
gameStates.append([])
gameStates.append([])
player1_won = 0
player2_won = 0
draw = 0
playtime = 50000


filename="tictactoe.txt"


if os.path.isfile(filename):			# If file exist then take states from file
    fp = open(filename, "r")
    print "Building states from file..."
    load_File(fp)
    fp.close()
else:
	print "Computer is playing with itself..."

	FeedInput(0)
	FeedInput(1)	
	while playtime>0:
		playtime-=1
		
		board = [0,0,0,0,0,0,0,0,0]
		
		#print type(board)
		#print type(board[0])
		
		player1 = random.randint(0,1)
		player2 = 1 - player1
		
		
		gamePlay(board,player1,0.1)
		#print board
		win = gameOver(board,0)
		win1 = gameOver(board,1)
		
		if win==1:
			player1_won+=1
		elif win1 == 1:
			player2_won+=1
		else:
			draw += 1
		if win ==1:
			updateValue(0,1)
			updateValue(1,0)
		elif win1 == -1 or win == -1:
			updateValue(0,-1)
			updateValue(1,-1)
		else:
			updateValue(0,0)
			updateValue(1,1)
	
	
	#if win == 1 or win == -1:
		
	#else:
	
	#print "player 0: ",states[0]
	#print "player 1: ",states[1]

#print_data(0)
#print_data(1)	


while(1):
	

	#print_data(0)
	#print_data(1)
	board = [0,0,0,0,0,0,0,0,0]
	#print_board(board)

	
	player1 = random.randint(0,1)
	#player1 = 0
	won = 0
	won1 = 0
	if player1 == 0:
		print "Player 1: Computer"
		print "Player 2: You"

		while len(gameStates[0])>0:
			gameStates[0].pop()

		
		turn = 0
		while (True):

			won = gameOver(board,0)
			won1 = gameOver(board,1)
			#print won,won1
			if won == 1 or won1 == 1 or won == -1 or won1 == -1:
				break

			if turn%2==0:
				ComputerMove(board,0)
			else:
				HumanMove(board,1)

			turn+=1

	else:
		print "Player 1: You"
		print "Player 2: Computer"

		while len(gameStates[0])>0:
			gameStates[0].pop()

		turn = 0
		while (True):

			won = gameOver(board,0)
			won1 = gameOver(board,1)
			#print won,won1
			if won == 1 or won1 == 1 or won == -1 or won1 == -1:
				break

			if turn%2==1:
				ComputerMove(board,0)
			else:
				HumanMove(board,1)

			turn+=1
	
	print
	print_board(board)
	print
	if won == 1:
		print "Computer Won"
		updateValue(0,1)
	elif won1==1:
		print "You Won"
		updateValue(0,0)
	else:
		print "Game Draw"
		updateValue(0,-1)
	
	x = raw_input('Do you want to play more[y]: ')
	if x != 'y':
		break


writeToFile("tictactoe.txt")

		
			

print "Player 0 won : ",player1_won
print "Player 1 won : ",player2_won
print "Draw : ",draw	
	
print "len 0 : ",len(states[0])
print "len 1 : ",len(states[1])
