
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.animation as animation
from os import path
import math


# This will output animations of 2d lattice slices. The adjustable parameters are as follows: 
# PATH - the location of the data files
# field - which field to plot. For example, 0 for phi, 1 for chi
# nbox - number of grid points on a side
# grid_spacing - not currently used
# time_index - not currently used
# high, low - specify the range of the plot z-axis
# speed - multiplier to shorten output video
# PATH_OUT - where to save the video
# output_name - name of output video file
# overwrite - if set to True, then overwrite video file from previous run. If set to False, append number onto the end of video file name and write new video. 

# NOTE : videos with a high number of frames take a long time to render. The render is not finished until the "Done" message appears

PATH = "/home/reagan/Documents/latticeeasy2.1/Coleman_data_128/"
PATH_OUT = PATH
output_name = "coleman"
overwrite = False
field = 0
nbox = 128
grid_spacing = 1
time_index = 0
high = 1.5
low = -1
speed = 10

def main () :

    #Read in times
    with open(PATH + "slicetimes_0.dat") as slice_times_file :
        lines = slice_times_file.readlines() #read in each line of the slicetimes file as a lsit entry

        slice_times = [float(line) for line in lines if not line == "\n"] #Get rid of any pesky newlines

        num_times = len(slice_times)
        print(slice_times[-1])

    #Read in slice data
    with open(PATH + "slices" + str(field) + "_0.dat") as slice_data_file:

        lines = slice_data_file.readlines()#read in each line of the slice data file as a list entry
        raw_data = [float(line) for line in lines if not line == "\n"] # get rid of empty newline entries

        #The data structure for the slice data is formatted as follows: 
        # frames[time_index_value] gives a 2D array of size nbox*nbox corresponding to the field at time time_index_value
        # frames[times_index_value][row] gives a 1D array of size nbox. 
        # frames[times_index_value][row][column] gives the value of the field at time times_index_value at (column, row

        frames = [] #empty array to hold field data
        for i in range(num_times) : # loop over all time frames
            time_frame = [] #temporary array to store all lattice data correspinding to a specific time
            for j in range(nbox) : #loop through each row
                start_index = i * nbox**2 + (j * nbox) #start_index is the location of the first element in the frame at time i
                time_frame.append(raw_data[start_index:start_index+nbox]) #add row to the time_frame array
            frames.append(time_frame) # append time_frame[] (2d array) to frames[]

    print(len(frames))

    def update(i, Z, plot): #update plot with new data each frame
        ax.clear()
        Z = np.asarray(frames[i])
        plot = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0.1, antialiased=True, edgecolor = 'black')
        ax.set_zlim(low, high)
        return plot, 

    fig = plt.figure()

    plt.subplots_adjust(bottom=0.25)                
    ax = fig.add_subplot(111, projection='3d')   

    x = np.linspace(0, nbox, nbox) # create an array from 0 to nbox with spacing 1 so {0,1,2,3, ... nbox - 1}
    y = np.linspace(0, nbox, nbox) # create an array from 0 to nbox with spacing 1 so {0,1,2,3, ... nbox - 1}
    X, Y = np.meshgrid(x, y)
    Z = np.asarray(frames[time_index])
    ax.set_zlim(low, high)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    
    ax.azim = -39
    ax.elev = 68

    plot = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0.1, antialiased=True, edgecolor = 'black')

    ani = animation.FuncAnimation(fig, update, frames=num_times, fargs=(Z, plot), interval = 1000 * ((slice_times[-1] / len(frames))) / speed  , blit=False)

    if not overwrite and path.exists(PATH_OUT + output_name + ".mp4") : # if output file already exists and overwrite == False, choose a new name and output
        print("found \"" + PATH_OUT + output_name + ".mp4\"")
        run = 1
        while path.exists(PATH_OUT + output_name + "_" + str(run) + ".mp4") :
            print("found \"" + PATH_OUT + output_name + "_" + str(run) + ".mp4\"")
            run += 1

        print("Saving to file \"" + PATH_OUT + output_name + "_" + str(run) + ".mp4\" ...")
        ani.save(PATH_OUT + output_name + "_" + str(run) + ".mp4", fps=math.ceil(speed * len(frames) / slice_times[-1]))

    else : # first time save or overwrite
        print("Saving to file \"" + PATH_OUT + output_name + ".mp4\" ...")
        ani.save(PATH_OUT + output_name + ".mp4", fps=math.ceil(speed * len(frames) / slice_times[-1]))

    print("Done.")
    #plt.show()

if __name__ == "__main__" :
    main()


