import random
import itertools

class Dice:
    def __init__(self, faces):
        if isinstance(faces, int):
            self.face_count = faces
            self.face_labels = list(range(1, faces + 1))
        else:
            self.face_count = len(faces)
            self.face_labels = faces

    def roll(self):
        return random.choice(self.face_labels)

    def roll_n(self, times):
        return [self.roll() for _ in range(times)]

class DiceRoll:
    
    def __init__(self, roll, modifier=0):
        self.dice = [pair[0] for pair in roll]
        self.count = [pair[1] for pair in roll]
        self.modifier = modifier

    def roll(self):
        raw_rolls = []
        for die, num in zip(self.dice, self.count):
            raw_rolls.extend(die.roll_n(num))
        
        total = sum(raw_rolls) + self.modifier
        return (total, raw_rolls)

    def possible_outcomes(self):
        all_die_options = []
        for die, num in zip(self.dice, self.count):
            for _ in range(num):
                all_die_options.append(die.face_labels)
                
        permutations = list(itertools.product(*all_die_options))
        
        results = []
        for p in permutations:
            results.append((sum(p) + self.modifier, list(p)))
        return results
        
class RollAnalyser:
    def __init__(self, dice_roll):
        self.outcomes = dice_roll.possible_outcomes()

    def get_distribution(self):
        dist = {}
        for total, _ in self.outcomes:
            dist[total] = dist.get(total, 0) + 1
        return dict(sorted(dist.items()))

    def print_histogram(self):
        dist = self.get_distribution()
        print("\n--- Roll Distribution Histogram ---")
        for total, freq in dist.items():
            bar = '*' * freq
            print(f"{total:2}: {bar} ({freq})")

# TEST SCRIPT
if __name__ == "__main__":
    print('Running test script.\n')
    
    # 1. Basic Dice Setup
    d4 = Dice(4)
    d6 = Dice(6)
    d6_unlucky = Dice([1,1,1,1,1,6])

    # 2. Part 1 Tests
    print('--- Part 1: Basic Dice Tests ---')
    print(f'1d4: {d4.roll()}, 20d4: {d4.roll_n(20)}')
    print(f'1d6 (unlucky): {d6_unlucky.roll()}\n')

    print('--- Part 1: Complex DiceRoll Test (4d4 + 1d20 - 2) ---')
    mixed_roll = DiceRoll([(d4, 4), (Dice(20), 1)], -2)
    roll_result, raw_rolls = mixed_roll.roll()

    # 1. Show the result of the Complex Roll
    print(f'Result: {roll_result} (Raw rolls: {raw_rolls} with -2 modifier)\n')

    # 2. Run the Part 2 Analysis
    print('--- Part 2: Distribution Analysis (2d2 + 10) ---')
    simple_roll = DiceRoll([(Dice(2), 2)], 10)
    analyser = RollAnalyser(simple_roll)
    analyser.print_histogram()
