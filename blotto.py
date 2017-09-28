import random
import math

# Returns a random sorted list of <nums> values that sum to <total>.
def gen_random_blotto(nums, total):
	vals = [0] * (nums - 1)
	for i in range(nums - 1):
		vals[i] = random.randint(1, total)

	vals = sorted(vals)
	diffs = [0] * (nums)
	diffs[0] = vals[0]
	for i in range(1, nums - 1):
		diffs[i] = vals[i] - vals[i - 1]
	diffs[nums - 1] = total - vals[-1]
	diffs = sorted(diffs)
	return diffs

#
def gen_random_blotto_3(nums, total):
	num1 = random.randint(0, 9)
	if num1 == 0:
		coeff1 = random.randint(1, 5)
	else:
		coeff1 = random.randint(1, nums - 3)
	coeff2 = nums - coeff1

	if coeff2 == 0:
		blotto = [num1] * coeff1
		return blotto

	num2 = (total - (coeff1 * num1)) / coeff2
	if num1 >= num2:
		blotto = [num2] * coeff2 + [num1] * coeff1
	else:
		blotto = [num1] * coeff1 + [num2] * coeff2

	return blotto

def print_blotto_tests(blottos, tests, nums, total, values):
	for i in range(tests):
		enemy_blotto = gen_random_blotto_3(nums, total)
		for blotto in blottos:
			points = match_blottos(blotto, enemy_blotto, values)
			print str(blotto) + " vs " + str(enemy_blotto) + ": " + str(points) + " points."
		print "---------------------------"

def match_blottos(my_blotto, random_blotto, values):
	points = 0
	for i in range(len(my_blotto)):
		if my_blotto[i] > random_blotto[i]:
			points += values[i]
		elif my_blotto[i] == random_blotto[i]:
			points += .5 * values[i]

	return points

def match_blottos_2(my_blotto, random_blotto, values):
	points = 0
	for i in range(len(my_blotto)):
		if my_blotto[i] > random_blotto[i]:
			points += values[i] * math.sqrt(my_blotto[i])
		elif my_blotto[i] == random_blotto[i]:
			points += .5 * values[i] * math.sqrt(my_blotto[i])

	return points

def match_blottos_4(my_blotto, random_blotto, values):
	points = 0
	my_blotto_copy = my_blotto[:]
	random_blotto_copy = random_blotto[:]
	for i in range(len(my_blotto_copy) - 1):
		if my_blotto_copy[i] > random_blotto_copy[i]:
			points += values[i]
			my_blotto_copy[i + 1] += my_blotto_copy[i] / 3
		elif my_blotto_copy[i] < random_blotto_copy[i]:
			random_blotto_copy[i + 1] += random_blotto_copy[i]/3
		else:
			points += values[i]/2.0

	return points


def blotto_mutation_generator(my_blotto, mutations):
	new_blotto = my_blotto[:]
	for i in range(mutations):
		(inc, dec) = random.sample(range(0, len(my_blotto)), 2)
		if new_blotto[dec] > 0:
			new_blotto[inc] += 1
			new_blotto[dec] -= 1
	return sorted(new_blotto)

def get_blotto_score(BATTLEFIELDS, SOLDIERS, my_blotto, values, enemy_blottos):
	points = 0.0
	for enemy_blotto in enemy_blottos:
		points += match_blottos_4(my_blotto, enemy_blotto, values)
	return (points/len(enemy_blottos))

def generate_best_blottos(BATTLEFIELDS, SOLDIERS, values, blottos=20, steps=10):
	blotto_list = []
	blotto_scores = []
	for i in range(blottos):
		blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
		while blotto in blotto_list:
			blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
		blotto_list.append(blotto)

	for step in range(steps):
		blotto_scores = []
		enemy_blottos = []
		for i in range(50000):
			enemy_blottos.append(gen_random_blotto(BATTLEFIELDS, SOLDIERS))

		for blotto in blotto_list:
			blotto_scores.append(get_blotto_score(BATTLEFIELDS, SOLDIERS, blotto, values, enemy_blottos))

		blotto_tuples = zip(blotto_scores, blotto_list)
		blotto_tuples.sort()
		print "top 3: " + str(blotto_tuples[-3]) + ", " + str(blotto_tuples[-2]) + ", " + str(blotto_tuples[-1])
		new_blottos = []
		best_blottos = []
		for i in range(-(blottos/10), 0):
			best_blottos.append(blotto_tuples[i][1])
		for blotto in best_blottos:
			new_blottos.append(blotto)
			for j in range(4):
				new_blottos.append(blotto_mutation_generator(blotto_tuples[i][1], 3+2*j))
			for k in range(5):
				new_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
				while (new_blotto in new_blottos) or (new_blotto in best_blottos):
					new_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
				new_blottos.append(new_blotto)
		blotto_list = new_blottos


BATTLEFIELDS = 7
SOLDIERS = 100
VALUES = [6, 7, 8, 9, 10, 11, 12]

generate_best_blottos(BATTLEFIELDS, SOLDIERS, VALUES, blottos=20, steps=1000)
#blottos = [[0,0,0,14,14,14,14,14,14,14],[2,2,2,2,2,2,22,22,22,22],[0,0,0,0,0,20,20,20,20,20]]

#print_blotto_tests(blottos, 10, 10, 100, VALUES)

'''while True:
	counter += 1
	new_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
	if counter % 5000 == 0:
		print counter
	average_points = 0.0
	for j in range(ENEMY_BLOTTOS):
		enemy_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
		average_points += match_blottos_2(new_blotto, enemy_blotto, VALUES_2)

	average_points /= ENEMY_BLOTTOS
	if average_points > best_points:
		matchup_points = 0
		for k in range(100000):
			enemy_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
			matchup_points += match_blottos_2(new_blotto, enemy_blotto, VALUES_2) - \
				match_blottos_2(best_blotto, enemy_blotto, VALUES_2)

		if matchup_points > 0:
			best_points = average_points
			best_blotto = new_blotto
			print str(best_blotto) + ", " + str(best_points) + ", "  + str(counter)'''

'''
best_blotto = [0, 0, 1, 2, 4, 34, 59]
new_blotto = []
matchup_points = 0
match_counter = 0
while True:
	(inc, dec) = random.sample(range(0, 7), 2)
	new_blotto = best_blotto[:]
	if new_blotto[dec] > 0:
		new_blotto[inc] += 1
		new_blotto[dec] -= 1
		print best_blotto
		print new_blotto
		for i in range(100000):
			enemy_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
			matchup_points += match_blottos_2(best_blotto, enemy_blotto, VALUES_2) - \
					match_blottos_2(new_blotto, enemy_blotto, VALUES_2)
		if matchup_points < 0:
			best_blotto = new_blotto

		print "Best: " + str(best_blotto) + ", " + str(matchup_points/100000)
		matchup_points = 0'''







