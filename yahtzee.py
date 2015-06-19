"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""
#play at http://www.codeskulptor.org/#user40_K7aFiu3ro7_12.py

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = [0 for dummy in range(max(hand))]
    for item in hand:
        scores[item-1] += item
    return max(scores)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    #scores = [0 for dummy in range(len(held_dice)+num_free_dice)]
    scores = []
    die = [(num + 1) for num in range(num_die_sides)]
    outcomes = gen_all_sequences(die,num_free_dice)
    for trial in outcomes:
        hand = list(held_dice) + list(trial)
        scores.append(score(hand))
    num_trials = len(outcomes) + 0.0
    total_sum = 0
    for result in scores:
        total_sum += result
    return total_sum/num_trials
    
    
def check_extras(item, hand):
    """Helper function for gen_all_holds function"""
    for value in item:
        if item.count(value) > hand.count(value):
            return False
    return True
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    temp = list(hand)
    result = set([()])
    for length in range(len(temp) + 1):
        trial = gen_all_sequences(temp, length)
        final_trial = set([])
        for item in trial:
            if (check_extras(list(item), temp)):
                final_trial.add(tuple(sorted(item)))
        result = result.union(final_trial)
    return result


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    curr_max = 0.0
    for hold in all_holds:
        exp_val = expected_value(hold, num_die_sides, len(hand) - len(hold))

        if exp_val > curr_max:
            curr_max = exp_val
            result = hold
    return (curr_max, result)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
        
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)