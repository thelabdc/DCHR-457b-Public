'''
Functions for performing and plotting AB tests

- split_groups: split data our data into 3, the control group and the 2 treatment arms
- split_only2_groups: split data into only control and treatment groups, aggregating both
                      email arms into one (as pre-defined in pre-analysis plan)
                      
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Tuple

from . import ab_test


def split_groups(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split the data into treatment and control groups, where the treatment
    groups are split into the three different treatment arms.
    
    Returns:
        A three tuple of data frames: control, basic, and simple_choice frames.
    """
    control = df[df.treatment_real == 0]
    basic = df[df.treatment_real == 1]
    simple_choice = df[df.treatment_real == 2]
    return control, basic, simple_choice


def split_only2_groups(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split the data into treatment and control groups, combining the
    both treatment arms.
    
    Returns:
        A two tuple of data frames: control and treatment frames.
    """
    control = df[df.treatment_real == 0]
    treatment = df[(df.treatment_real == 1) | (df.treatment_real == 2)]
    return control, treatment


#Function for performing ab test
def perform_ab_test(control_df: pd.DataFrame, 
                    treatment_df: pd.DataFrame, 
                    column_of_interest: str):
    '''
    perform_ab_test is a function that takes in 4 parameters:
    
    1. the control group dataframe
    2. the treatment group dataframe
    3. the column of interest
       - in our case, this would be 
            (1) whether someone newly enrolled, or 
            (2) whether someone increased contribution amounts if they were already enrolled.
    '''
        
    ### --- Calculating baseline values for AB test --- ###
        
    ## Control Group 
    # total successes
    # successes are the number of participants who takes the action we want, eg
    # (1) newly enrolled, (2) increased their contributions, (3) clicked a link
    successes_a = sum(control_df[column_of_interest])
    
    # total failures
    # failures are the number of employees in the control df who did not take the desired action
    failures_a = len(control_df) - successes_a
    
    ## Treatment Group
    successes_b = sum(treatment_df[column_of_interest]) # total successes
    failures_b = len(treatment_df) - successes_b # total failures
    
    print('Number in control group:', len(control_df))
    print('Number in treatment group:', len(treatment_df))
    
    print('\nTotal successes, control:', successes_a)
    print('Total successes, treatment:', successes_b)
    
    
    #control_rate is the proportion of employees already enrolled in the control group
    control_rate = (successes_a) / len(control_df)

    #treatment is the proportion of employees enrolled in the treatment group
    treatment_rate = (successes_b) / len(treatment_df)

    num_participants = len(control_df) + len(treatment_df)
    
    
    print("\nConversion Rate:")
    print("Control Group Rate:", round(control_rate,5)*100, "%", sep = "")
    print("Treatment Group Rate:", round(treatment_rate,5)*100, "%", sep = "")
    
    if (control_rate == 0)|(treatment_rate==0):
        print("Percent change: 0.000%")
    else:
        print("Percent change:", round(treatment_rate/control_rate-1, 5)*100, "%", sep = "")
    
    ### --- Calculate degree of certainty. See the functions in the ab_test.py file --- ###
    
    deg_of_certainty = ab_test.degree_of_certainty(successes_a, failures_a, successes_b, failures_b)
    
    print('\nDegree of certainty:', round(deg_of_certainty, 3)) 
    print()
    
    
    ### --- Set up for degree of certainty plot --- ###
    #Set a seed
    random = np.random.RandomState(1234)
    
    #Randomly sample from a beta distribution of size 100k
    size = 100000
    #For the control group
    beta_c = random.beta(successes_a + 1, failures_a, size=size)
    #For the treatment group
    beta_t = random.beta(successes_b + 1, failures_b, size=size)
    
    posterior = beta_t - beta_c
    posterior.sort()
            
    #just need one for plotting
    return posterior, successes_a


def plot_abtest(posterior: np.ndarray, 
                successes_a: int, 
                action: str, 
                a: str, 
                b: str):
    '''
    plot ab_test is a function that takes in 2 parameters:
        
    posterior (np.ndarray): the posterior distribution from perform_abtest
    successes_a (int): the number of successes in group a (used to scale y axis)
    action (str): For the plot caption, what action/success is this plot describing?
                  For example, "clicking hyperlink", "newly enrolling" etc
    a (str): For the plot caption, what is A (the control group)? 
    b (str): For the plot caption, what is B (the treatment group)?
    '''
    
    plt.figure(figsize=(12,7))
    ## step one: use posterior to get all the bins (101 bins)
    bins = np.linspace(posterior[0], posterior[-1], 101)
    
    ## plot the histogram using all bins
    hist, edges = np.histogram(posterior, bins=bins)
    
    ## get the bins where the x is greater than 0
    bins_shading = bins[bins >= 0]
    bins_shading_index = bins >= 0
    hist_shading = hist[bins_shading_index[0:100]]
    
    ## plot
    plt.plot(bins[:-1], hist, color='#2b4888')
    plt.fill_between(x = np.linspace(bins_shading[0], bins_shading[-1], len(hist_shading)),
                 y1 = np.zeros(len(hist_shading)), #bottom of curve, i.e. on the line
                 y2 = hist_shading, #top of the curve
                 facecolor = '#2b4888',
                 alpha=1)
    plt.axvline(x = 0, linestyle='--', color='black') #line at zero
    
    plt.ylim(bottom = 0)
    plt.yticks([])
    plt.ylabel('Density of Draws')
    plt.xlabel("Posterior difference in the rate of employees " + action + ": " + b + " minus " + a + ".\n" + \
               "neg: " + b + " group had a lower rate, \n pos: " + b + " group had a higher rate,\n zero: same rate")