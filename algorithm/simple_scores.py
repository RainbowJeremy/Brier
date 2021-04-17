# this file is an open source algorithm to optimise predictions about the future
from decimal import Decimal

####################### individual

"""def single_score(collapse, estimates):
    truth = np.array([collapse])
    guess = np.array([estimates])/100
    score = round(bsl(truth, guess), 7)
    return score
"""
def single_score(collapse, estimates):
    guess = round(estimates/100)
    difference = collapse -estimates
    score = difference * difference
    return score

def predictor_score(collapse, estimates, total_estimates, old_score):
    new_score = single_score(collapse, estimates)
    new_score = Decimal(new_score)
    updated_score =(old_score*(total_estimates-1))/total_estimates + new_score/total_estimates
    return updated_score
###################### group

def find_median(queryset):
    midpoint = int(round(len(queryset)/2, 0))
    return queryset[midpoint]

def find_predictions(estimates):  # QuerySet -> int:
    all_guesses = []
    for est in estimates:
        if est.author.profile.score:
            guess = est.estimate
            multiplier = est.author.profile.score
            weighted_guess = guess*multiplier
            all_guesses.append(float(weighted_guess))

    median_pred = find_median(all_guesses)
    return median_pred
