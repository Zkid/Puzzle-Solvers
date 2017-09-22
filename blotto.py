import random
import math

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

BATTLEFIELDS = 7
SOLDIERS = 100
VALUES = [1, 1, 1, 1, 2, 2, 3]
VALUES_2 = [1, 1, 1, 1, 1, 1, 2]
TEST_BLOTTOS = 1000
ENEMY_BLOTTOS = 1000

best_points = -1
best_blotto = gen_random_blotto(BATTLEFIELDS, SOLDIERS)
counter = 0

while True:
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
			print str(best_blotto) + ", " + str(best_points) + ", "  + str(counter)
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







