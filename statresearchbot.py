"""
Title: Stat Research Bot
Date Started: July 18, 2019
Version: 1.1
Version Start Date: Mar 29, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the Stat Research Bot is to perform various research tests.

TO DO:
--create function that inputs various data into the num_trial_bot and finds the regression model.

Version 1.1:  Added sharpe and sharpemad to stat_summarizer
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
#   LOCAL APPLICATION IMPORTS


'''RETURNS NUMBER OF TRIALS IT TAKES FOR A ADDITIONAL SAMPLE TO MOVE THE AVERAGE LESS THAN THE TOLERANCE SET.  EVEN THOUGH AN ADDITIONAL SAMPLE MAY MOVE THE AVERAGE LESS THAN TOLERANCE, THE FOLLOWING SAMPLE COULD MOVE THE AVERAGE EVEN MORE, BY AN AMOUNT ABOVE TOLERANCE.  SO, THE FUNCTION SEARCHES FOR THE POINT AT WHICH THE MAX MOVEMENT FOR THE MOST RECENT 50% OF ALL TRIALS TAKEN FALLS BELOW THE TOLERANCE.
'''


def num_trial_bot(randmin, randmax, tolerance, verbose, plot):

    num_trials = 0
    data = [(randmax - randmin) * np.random.random() + randmin]

    all_readings = []
    recent_max = 1
    while recent_max > tolerance:
        num_trials += 1
        avg_before = np.mean(data)
        sample = (randmax - randmin) * np.random.random() + randmin
        if verbose == "verbose":
            print("%s %s || %s %s || %s %s || %s %s" % ("Trial:", num_trials, "Data:", data, "Data size:", len(data), "New Sample:", sample))
            print("%s %s" % ("Average Before:", avg_before))
        data.append(sample)
        avg_after = np.mean(data)
        reading = abs(avg_after - avg_before) / avg_before
        all_readings.append(reading)
        if verbose == "verbose":
            print("%s %s" % ("Average After:", avg_after))
            print("Current Reading: The additional sample moved the average by ", reading * 100, " %.")

        # COUNT IF READING IS BELOW TOLERANCE
        window = int(np.ceil(0.5 * (len(all_readings))))
        recent_max = np.max(all_readings[-window:])

    print("Out of the latter half of all trials, the maximum percentage by which an additional data point moved the overall mean is", recent_max * 100, "%.  Number of trials it took for the data to have the max be below the tolerance of", tolerance * 100, "%:", num_trials)

    # PLOT RESULTS
    if plot == 'plot':
        plt.plot(all_readings)
        x = np.linspace(0, num_trials + 1)
        y = [tolerance] * len(x)
        plt.plot(x, y, '-r', label='tolerance', linewidth=2.0)
        plt.ylabel('Diff between Mean before and after')
        plt.xlabel('Trials')
        plt.show()

    print('Min:', np.min(data))
    print('Max:', np.max(data))
    return num_trials


# GRAPHS THE COMBINATION FORMULA
def graph_combination_formula(n):

    numerator = np.math.factorial(n)
    results = [numerator / (np.math.factorial(k) * np.math.factorial(n - k)) for k in range(0, n + 1)]
    # PLOT RESULTS
    plt.plot(results)
    plt.ylabel('No. of combinations')
    plt.xlabel('Value of k')
    plt.show()


def stat_summarizer(figure):
    avg_perf = np.nanmean(figure)
    min_perf = np.nanmin(figure)
    q1_perf = np.nanquantile(figure, 0.25)
    med_perf = np.nanmedian(figure)
    q3_perf = np.nanquantile(figure, 0.75)
    max_perf = np.nanmax(figure)
    stdev = np.nanstd(figure)
    medianabdev = stats.median_absolute_deviation(figure, nan_policy='omit')
    sharpe = avg_perf / stdev
    sharpemad = med_perf / medianabdev

    finaldict = {
        'avg_perf': avg_perf,
        'med_perf': med_perf,
        'stdev': stdev,
        'medianabdev': medianabdev,
        'min_perf': min_perf,
        'max_perf': max_perf,
        'q1_perf': q1_perf,
        'q3_perf': q3_perf,
        'sharpe': sharpe,
        'sharpemad': sharpemad
    }

    return finaldict


def stat_summarizer_old(figure):
    avg_perf = np.nanmean(figure)
    min_perf = np.nanmin(figure)
    q1_perf = np.nanquantile(figure, 0.25)
    med_perf = np.nanmedian(figure)
    q3_perf = np.nanquantile(figure, 0.75)
    max_perf = np.nanmax(figure)
    iqr_perf = q3_perf - q1_perf
    max_min = max_perf - min_perf
    maxq3 = max_perf - q3_perf
    q1min = q1_perf - min_perf
    stdev = np.nanstd(figure)
    medianabdev = stats.median_absolute_deviation(figure, nan_policy='omit')

    finaldict = {
        'avg_perf': avg_perf,
        'min_perf': min_perf,
        'q1_perf': q1_perf,
        'med_perf': med_perf,
        'q3_perf': q3_perf,
        'max_perf': max_perf,
        'iqr_perf': iqr_perf,
        'max_min': max_min,
        'maxq3': maxq3,
        'q1min': q1min,
        'stdev': stdev,
        'medianabdev': medianabdev
    }

    return finaldict


# TAKES A LIST AND FILTERS OUT OUTLIERS
def outlier_remover(verbose, plot, strength, figure):

    q1_perf = np.nanquantile(figure, 0.25)
    q3_perf = np.nanquantile(figure, 0.75)
    iqr = q3_perf - q1_perf
    outlier_base = (strength * iqr)
    upper_limit = q3_perf + outlier_base
    lower_limit = q1_perf - outlier_base

    filtered_figure = [elem for elem in figure if elem <= upper_limit and elem >= lower_limit]
    outliers = list(set(figure).difference(set(filtered_figure)))

    num_outliers = len(outliers)
    num_orig = len(figure)
    num_filtered = len(filtered_figure)
    num_check = num_filtered + num_outliers

    if verbose == 'verbose':

        print('original (sorted):', sorted(figure))
        print('filtered (sorted):', sorted(filtered_figure))
        print('outliers (sorted):', sorted(outliers))
        print('upper_limit:', upper_limit)
        print('lower_limit:', lower_limit)
        print('CORRECT NUMBER OF OUTLIERS WERE REMOVED:', num_check == num_orig)
        print('num_outliers:', num_outliers)
        print('num_orig:', num_orig)
        print('num_filtered:', num_filtered)
        print('num_filtered + num_outliers:', num_check, '(if this matches num_orig, then outlier removal operation was successful)')

    if plot == 'plot':

        plt.plot(figure, 'bo')
        plt.plot(outliers, 'ro')
        plt.ylabel('strength: ' + str(strength))
        plt.xlabel('Outlier Range: ' + str(lower_limit) + ' to ' + str(upper_limit))
        plt.title('Number of Outliers: ' + str(num_outliers), loc='right')
        plt.title('% Outliers: ' + str(100 * (num_outliers / num_orig)) + '%', loc='left')
        plt.show()

    return filtered_figure


# TAKES A LIST AND RETURNS AGGREGATE NUMBER BASED ON METHOD REQUESTED
def list_aggregator(aggregatemethod, all_data):

    # AGGREGATE METHOD
    if aggregatemethod == 'mean':
        answer = np.nanmean(all_data)
    if aggregatemethod == 'median':
        answer = np.nanmedian(all_data)
    if aggregatemethod == 'minimum':
        answer = np.nanmin(all_data)
    if aggregatemethod == 'q1':
        answer = np.nanquantile(all_data, 0.25)
    if aggregatemethod == 'q3':
        answer = np.nanquantile(all_data, 0.75)
    if aggregatemethod == 'maximum':
        answer = np.nanmax(all_data)
    if aggregatemethod == 'stdev':
        answer = np.nanstd(all_data)
    if aggregatemethod == 'medianabdev':
        answer = stats.median_absolute_deviation(all_data, nan_policy='omit')
    if aggregatemethod == 'iqr':
        q1_perf = np.nanquantile(all_data, 0.25)
        q3_perf = np.nanquantile(all_data, 0.75)
        answer = q3_perf - q1_perf
    if aggregatemethod == 'range':
        min_perf = np.nanmin(all_data)
        max_perf = np.nanmax(all_data)
        answer = max_perf - min_perf
    if aggregatemethod == 'maxq3':
        max_perf = np.nanmax(all_data)
        q3_perf = np.nanquantile(all_data, 0.75)
        answer = max_perf - q3_perf
    if aggregatemethod == 'q1min':
        q1_perf = np.nanquantile(all_data, 0.25)
        min_perf = np.nanmin(all_data)
        answer = q1_perf - min_perf
    if aggregatemethod == 'q3q1avg':
        q1_perf = np.nanquantile(all_data, 0.25)
        q3_perf = np.nanquantile(all_data, 0.75)
        answer = (q3_perf + q1_perf) / 2
    if aggregatemethod == 'q3q1avgoveriqr':
        q1_perf = np.nanquantile(all_data, 0.25)
        q3_perf = np.nanquantile(all_data, 0.75)
        iqr = q3_perf - q1_perf
        answer = ((q3_perf + q1_perf) / 2) / iqr
    if aggregatemethod == 'maxminavg':
        min_perf = np.nanmin(all_data)
        max_perf = np.nanmax(all_data)
        answer = (max_perf + min_perf) / 2
    if aggregatemethod == 'maxminavgoverrange':
        min_perf = np.nanmin(all_data)
        max_perf = np.nanmax(all_data)
        maxmin = max_perf - min_perf
        answer = ((max_perf + min_perf) / 2) / maxmin

    return answer
