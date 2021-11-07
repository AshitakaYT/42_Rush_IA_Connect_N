import sys
import math
import random
import copy

width, height, win_len, start, time, gain = int(input()),int(input()),int(input()),int(input()),int(input()),int(input())

Matrix = [[0 for x in range(width)] for y in range(height)] 

surface = width * height


#########################################################NOTES#############################################################
##
## Joueur 1 : Nous
## Joueur 2 : Ennemy
##
## 
## O(B^n(N)) = (nbr de colonnes dispo) ^ (surface - N_total - N)
##													^
##													|
##												   = N
##
## Surface = width * height
##
## L'idee de minmax : 
## 		- On initialise le score du coup a -infini (score tres bas) pour qu'on execute une action quoi qu'il arrive
## 		- On teste les actions N + 1 découlant de la situation N
##		- On en deduit un score sur la qualite de la position pour nous (Utilite)
##		- Apres avoir teste les possibilites, on ne garde que celle avec l'utilite la plus elevee;
##			il faut donc avoir en parametre la position et l'utilite associee ("pos_score()")
##		- On repete tout sur N + n iteration, où n est la profondeur testee et est idealement basé sur le temps
##	
##
## O(B^n) sera approximativement (width) ^ (surface); par exemple pour un 7 * 4, d'un ordre de grandeur 10^23
##
## Python fait un million de calcul en 2 minutes environ, donc pour une partie de 10 secondes, on irait 
## 	jusqu'a 7 ^ 5 (n = 5) pour 1.6 secondes d'execution (temps le plus raisonnable pour cette complexite).
## PyPy compiler va 28x plus vite, donc on peut esperer atteindre raisonnablement n = 6 avec ce compilateur
##
##
## Minmax doit renvoyer la position optimale a la fin
##
##  
##
###########################################################################################################################




## Ajoute un jeton dans la colonne donnee, la matrice donnee et le joueur donne
def add_token(y, Matrix, player):
	i = 0
	
	## We go to column up while its not empty
	while Matrix[i][y] > 0 and i < height - 1:
		i += 1
	
	## We give to the case the player value
	Matrix[i][y] = player
	return i


## Joue le jeton
def play():
	col = 0
	y = 0
	score_max = -math.inf
	for col in range(width):
		if pos_score(col) > score_max:
			score_max = pos_score(col)
			y = col
	add_token(y, Matrix, 1)
	return y

## Checks left and right sides of line until less
def is_line(x, y, matrix, less):
	n = 0
	flag = 0
	while n < less:
		if y >= width - less:
			flag += 1
			break
		if matrix[x][y + n] != 1:
			flag += 1
			break
		n += 1;
	while less > 0:
		if y <= less:
			flag += 1
			break
		if matrix[x][y - less + 1] != 1:
			flag += 1
			break
		less -= 1
	if flag == 2:
		return (0)
	return 1

def is_column(x, y, matrix, less):
	n = 0
	flag = 0
	while n < less:
		if x >= height - less:
			flag += 1
			break
		if Matrix[x + n][y] != 1:
			flag += 1
			break
		n += 1;
	while less > 0:
		if x <= less:
			flag += 1
			break
		if Matrix[x - less + 1][y] != 1:
			flag += 1
			break
		less -= 1
	if flag == 2:
		return 0
	return 1

def ft_print_matrix(matrix):
    for x in matrix:
        for value in x:
            print(value, end="")
        print('\n', end="")


def is_win(matrix, player):
	if win_len == 3:
		for i in range(width - 2):
			for j in range(height):
				if matrix[j][i] == player and matrix[j][i+1] == player and matrix[j][i+2] == player:
					return 1
		for i in range(width):
			for j in range(height-2):
				if matrix[j][i] == player and matrix[j+1][i] == player and matrix[j+2][i] == player:
					return 1
		for i in range(width - 2):
			for j in range(height - 2):
				if matrix[j][i] == player and matrix[j+1][i+1] == player and matrix[j+2][i+2] == player:
					return 1
		for i in range(width - 2):
			for j in range(2, height):
				if matrix[j][i] == player and matrix[j-1][i+1] == player and matrix[j-2][i+2] == player:
					return 1
	if win_len == 4:
		for i in range(width - 3):
			for j in range(height):
				if matrix[j][i] == player and matrix[j][i+1] == player and matrix[j][i+2] == player and matrix[j][i+3] == player:
					return 1
		for i in range(width):
			for j in range(height-3):
				if matrix[j][i] == player and matrix[j+1][i] == player and matrix[j+2][i] == player and matrix[j+3][i] == player:
					return 1
		for i in range(width - 3):
			for j in range(height - 3):
				if matrix[j][i] == player and matrix[j+1][i+1] == player and matrix[j+2][i+2] == player and matrix[j+3][i+3] == player:
					return 1
		for i in range(width - 3):
			for j in range(3, height):
				if matrix[j][i] == player and matrix[j-1][i+1] == player and matrix[j-2][i+2] == player and matrix[j-3][i+3] == player:
					return 1
	if win_len == 5:
		for i in range(width - 4):
			for j in range(height):
				if matrix[j][i] == player and matrix[j][i+1] == player and matrix[j][i+2] == player and matrix[j][i+3] == player and matrix[j][i+4] == player:
					return 1
		for i in range(width):
			for j in range(height-4):
				if matrix[j][i] == player and matrix[j+1][i] == player and matrix[j+2][i] == player and matrix[j+3][i] == player and matrix[j+4][i] == player:
					return 1
		for i in range(width - 4):
			for j in range(height - 4):
				if matrix[j][i] == player and matrix[j+1][i+1] == player and matrix[j+2][i+2] == player and matrix[j+3][i+3] == player and matrix[j+4][i+4] == player:
					return 1
		for i in range(width - 4):
			for j in range(4, height):
				if matrix[j][i] == player and matrix[j-1][i+1] == player and matrix[j-2][i+2] == player and matrix[j-3][i+3] == player and matrix[j-4][i+4] == player:
					return 1
	return 0

## Calcule le score d'un play
def pos_score(y):
	score = 0
	
	## Temp to not modify main one
	tmpmatrix = copy.deepcopy(Matrix)
	x = add_token(y, tmpmatrix, 1)
	
	## Are we in the middle?
	if y == (width / 2):
		score += 4
	
	## Are we making a line of win_len - 3 ? (case win_len = 5)
	if (is_line(x, y, tmpmatrix, 3)):
		score += 1
	if (is_column(x, y, tmpmatrix, 3)):
		score += 1
	## Are we making a line of win_len - 2? (case win_len >= 4)
	if (is_line(x, y, tmpmatrix, 2)):
		score += 2
	if (is_column(x, y, tmpmatrix, 2)):
		score += 2
	#if (is_diag(x, y, matrix, 2)):
	#	score += 2
	
	## Are we making a line of win_len - 1?
	if (is_line(x, y, tmpmatrix, 1)):
		score += 5
	if (is_column(x, y, tmpmatrix, 1)):
		score += 5
	#if (is_diag(x, y, matrix, 1)):
	#	score += 5
	
	## Are we making a winning line ?
	if is_win(tmpmatrix, 1):
		score += 10000000
	
	## Does the ennemy have a win_len - 3 line ? (case win_len = 5)
	#score -= 1
	
	## Does the ennemy have a win_len - 2 line ? (case win_len >= 4)
	#score -= 2
	
	## Does the ennemy have a win_len - 1 line ?
	if is_win(tmpmatrix, 2):
		score -= 100000
	print(score)
	return score

##					   ##
#						#
#		   MAIN			#
#						#
##					   ##


## We start second
if start == 2:
	add_token(int(input()), Matrix, 2)

## No need to check if we win or not, the Referee does it
while (1):
	## We play
	sys.stdout.write(str(random.randint(0, width) + "\n"))
	## They play and we add their token
	add_token(int(input()), Matrix, 2)