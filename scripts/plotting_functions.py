#Function to show datalabels in plots
import matplotlib.pyplot as plt
import numpy as np

def showDataLabels(f, n_precision = 0, fontsize = 10):
    if f =='int':
        value_format = '%d'
        label = ''
    else:
        label = '%'
        if n_precision == 0:
            value_format = '%d'
        elif n_precision == 1:
            value_format = '%.1f'
        elif n_precision == 2:
            value_format = '%.2f'
        elif n_precision == 3:
            value_format = '%.3f'
        elif n_precision == 4:
            value_format = '%.4f'

    # Get current axis on current figure
    ax = plt.gca()

    # Iterate through the list of axes' patches
    for p in ax.patches:
        height = p.get_height()
        #If the height is missing (this happens when we force a label and a label does not exist), assign 0 to height
        #otherwise, keep height as is. 
        height = np.where(np.isnan(height), 0, height)
        ax.text(x = p.get_x() + p.get_width()/2., 
                y = height, 
                s = value_format % height + label, 
                fontsize=fontsize, 
                color='black', 
                ha='center', 
                va='bottom')
    plt.show()
    
def showProportionLabels(df): 
    # Get current axis on current figure
    ax = plt.gca()

    #get the list of the number of employees to iterate over 
    num_employees = list((df['OCTO_total_emp']).astype(int))
    #this is to start at the beginning of the list, and iterate over 
    num_emp = 0

    #These are the starting, middle, and ending indexes for the bars themselves
    start = 0
    mid = int(len(ax.patches)/2)
    end = len(ax.patches)
    
    #For the employee sizes
    for p in ax.patches[start:mid]: #I only want the labels at the top of the plot, not the ones with the percentage. 
        height = p.get_height()
        width = p.get_x() + p.get_width()/2.
            #If the height is missing (this happens when we force a label and a label does not exist), assign 0 to height
            #otherwise, keep height as is. 
        height = np.where(np.isnan(height), 0, height)
        ax.text(x = width, 
                y = height, 
                s = 'n='+ str(num_employees[num_emp]),
                fontsize=14, 
                color='black', 
                ha='center', 
                va='bottom')
        if num_emp < len(num_employees)-1:
            num_emp +=1

    #For the percentage of employees not enrolled in 457(b)
    for p in ax.patches[mid:end]: #I only want the labels with the percentage. 
        height = p.get_height()
        width = p.get_x() + p.get_width()/2.
            #If the height is missing (this happens when we force a label and a label does not exist), assign 0 to height
            #otherwise, keep height as is. 
        height = np.where(np.isnan(height), 0, height)
        ax.text(x = width, 
                y = height, 
                s = '%.2f'%(height),
                fontsize=16, 
                color='white', 
                ha='center', 
                va='bottom')
        if num_emp < len(num_employees)-1:
            num_emp +=1