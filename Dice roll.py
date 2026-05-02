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
