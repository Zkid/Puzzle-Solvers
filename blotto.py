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

def blotto_mutation_generator(my_blotto, mutations):
	new_blotto = my_blotto[:]
	for i in range(mutations):
		(inc, dec) = random.sample(range(0, len(my_blotto)), 2)
		if new_blotto[dec] > 0:
			new_blotto[inc] += 1
			new_blotto[dec] -= 1
	return sorted(new_blotto)

def get_blotto_score(my_blotto, values, enemy_blottos=1000):
	BATTLEFIELDS = len(my_blotto)
	SOLDIERS = sum(my_blotto)
	points = 0.0
	for i in range(enemy_blottos):
		enemy_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
		points += match_blottos_2(my_blotto, enemy_blotto, values)
	return (points/enemy_blottos)

def generate_best_blottos(BATTLEFIELDS, SOLDIERS, values, blottos=20, steps=10):
	blotto_list = []
	blotto_scores = []
	for i in range(blottos):
		blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
		blotto_list.append(blotto)

	for step in range(steps):
		blotto_scores = []
		for blotto in blotto_list:
			blotto_scores.append(get_blotto_score(blotto, values))

		blotto_tuples = zip(blotto_scores, blotto_list)
		blotto_tuples.sort()
		print blotto_tuples[-1]
		new_blottos = []
		for i in range(-(blottos/10), 0): 
			new_blottos.append(blotto_tuples[i][1])
			for j in range(4):
				new_blottos.append(blotto_mutation_generator(blotto_tuples[i][1], 3+2*j))
			for k in range(5):
				new_blottos.append(gen_random_blotto(BATTLEFIELDS, SOLDIERS))
		blotto_list = new_blottos


BATTLEFIELDS = 7
SOLDIERS = 100
VALUES = [1, 1, 1, 1, 2, 2, 3]
VALUES_2 = [1, 1, 1, 1, 1, 1, 2]
TEST_BLOTTOS = 1000
ENEMY_BLOTTOS = 1000

best_points = -1
best_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
counter = 0

my_blotto = [1, 1, 4, 5, 21, 27, 41]

generate_best_blottos(BATTLEFIELDS, SOLDIERS, VALUES_2, 100, 100)

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







