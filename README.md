# DCHR-457b-Public
@authors: [Vicky Mei](vicky.mei@dc.gov), Peter Casey, [Katie Gan](katie.gan@dc.gov)

## Introduction
This repository contains scripts and some of the data used to analyze the results of a randomized control trial we ran with the DC Department of Human Resources in 2018. Working with DCHR, we wondered whether a behaviorally-informed email would encourage DC employees to 1) start saving in a 457(b) plan, or 2) increase the amount they were saving if already enrolled. The analysis was pre-registered on the Open Science Framework (OSF). You can read the pre-analysis plan [here](https://osf.io/u2wv9/) and the final report [here](https://osf.io/dqeg9/). 


## Organization
The repo is organized into three primary folders:
- analysis
- data
- scripts

## scripts folder: 

This folder contains two scripts: 

- `ab_test.py`, which contains the functions for calculating the degree of certainty in an ab test
- `perform_ab.py` which contains the function for splitting up the datasets, and performing and plotting the ab tests. 
- `plotting_functions.py` which contains functions for creating data labels for our plots


## analysis folder:
Note: You cannot run the first 3 notebooks, because we have not made these data publicly available. However, these notebooks just peform the cleaning and preparation of the data. We do include output where we can. 

Additionally, we made the decision to remove salary information in all of our data available to the public, because of the potential to trace back the salaries to the employees. This means that you cannot completely run Script 4 without the _original_ data files containing salary information either. 

### 1-data-clean-and-merge.ipynb
When this project was first started, we forgot to set a seed to reproduce the random numbers that were generated in determining which treatment arms employees were assigned to. Based on the email lists that we sent to GovDelivery (the vendor we use to send out emails), we recreated the group assignments based on the email lists that and do some cleaning to prep our baseline DCHR data. 

### 2-email-outcomes-analysis.ipynb 
This notebook analyzes email-throughs  that were sent to DCHR employees using GovDelivery. This is based on original DCHR data and analysis was completed before we actually received outcomes for the analysis that was pre-registered.

### 3-457b-Peoplesoft-Data-Clean-Public.ipynb 
These notebooks clean the Peoplesoft data that OCTO gave to The Lab, and merges the PeopleSoft data to the baseline DCHR data. 

We discovered here that there is a discrepancy between the number of employees in OCTO data compared the number of employees in DCHR data (see the notes in the Google Drive for more information). This might have something to do with the fact that the OCTO data pulls included “active employees”. Our analysis uses OCTO data as our authoritative source. February data is used for our confirmatory outcomes and March data is used for our exploratory outcomes. The last section of the notebook also performs some baseline descriptive analysis of the baseline data for the report. 


### 4-457b-AB-Test-Prep.ipynb
This notebook preps the data for the AB analysis for both confirmatory and exploratory data, by 
(1) correcting data & human errors, e.g. people who contribute $18,000 or 100% contributions per paycheck, 
(2) implementing decision rules as it pertains to actual 457(b) enrollment and contributions, e.g. maximum allowable amounts,
    calculating annual amounts contributed for employees who chose to contribute a percentage of their salary rather than a flat amount, etc.
(3) generating outcome variables, e.g., a boolean for whether an employee increased contributions or newly enrolled,
(4) checking that 1-3 were done correctly

Additionally, we remove salary, grade, and title information before writing outputs for this script, and round the total annual amounts contributed to the nearest $25 for those employees who opted to contribute a percentage of their salary, to avoid reverse calculating salary. This affects the amounts contributed for 59 employees. This may affect the results when you run the data through the later scripts. 

*Starting from this point, you can run the analysis using the data from the data folder*

### 5-457b-AB-Test-Binary-Confirmatory-Analysis.ipynb
This notebook runs through the AB analysis for research questions 1-4 for both the confirmatory and exploratory data. 

### 6-Percentile-Bootstrapping.ipynb
This notebook runs through the percentile bootstrapping problems as described in research questions 5-8 for confirmatory data.
Note: Try to clear up processes running in the background since this notebook uses quite a bit of memory.

### 7-Exploratory-Analysis.ipynb
This notebook conducts some basic exploratory analysis, including looking at how much employees changed their savings between treatment arms, and how agencies differ in terms of 

### 8-457b-Sensitivity-Analysis.ipynb 
Re-runs AB tests for things we were curious about; eg what happens if we consider those who were enrolled but contributed nothing to be not enrolled at baseline. 

