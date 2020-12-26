from traditionalMarriage import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def updateWorld(men_array):
    # Function to plot the world based on current positions of men
    n = len(men_array)
    world = np.zeros((2*n+1, 2*n+1))
    # Fill in females
    for i in range(1,2*n+1,2):
            world[1, i]=0.7
    # Fill in males
    for man in men_array:
        current_row_position = man.getPosition()[0]
        current_col_position = man.getPosition()[1]
        if world[current_row_position, current_col_position] > 0.7:
            # Change the colour if there are men who reach the female tile.
            world[current_row_position, current_col_position] += 0.08
        elif world[current_row_position, current_col_position] == 0:
            # Change the colour if a man steps on an empty tile.
            world[current_row_position, current_col_position] = 0.3
        else:
            # Change the colour if two men step on the same tile.
            world[current_row_position, current_col_position] += 0.1
    return world
    # Update the world based on the movement of the men

# We'll represent our world as a numpy array.
# This function creates a world full of zeroes, with a tile occupied by men represented by a 0.3 and
# a tile occupied by a women represented by 0.7. The values are incremented if several people occupy
# the same tile.

# We need a function to show the men (bottom squares) moving to the corresponding top square!
def moveMen(world, men_array, women_array):
    for man in men_array:
        current_row_position = man.getPosition()[0]
        current_col_position = man.getPosition()[1]
        favourite_woman = man.getRemainingPreferences()[0]
        goal_row_position = women_array[favourite_woman].getPosition()[0]
        goal_col_position = women_array[favourite_woman].getPosition()[1]

        if current_col_position == goal_col_position and current_row_position == goal_row_position:
            # Men will not move if they are in the same position as their desired partner.
            pass
        elif current_col_position == goal_col_position:
             # Men will move vertically by one square if they are in the same column as their desired partner.
            man.updatePosition(current_row_position - 1, current_col_position)
        elif current_col_position > goal_col_position:
            # Men will move horizontally if they are in the wrong column. Here they move to the left.
            man.updatePosition(current_row_position, current_col_position - 1)
        elif current_col_position < goal_col_position:
            # Here they move to the right.
            man.updatePosition(current_row_position, current_col_position + 1)

def nightIterationVisual(ims, ax, nights, men_array, women_array):
    # Function for each night that passes
    world = updateWorld(men_array)
    text = ax.annotate('Night: '+ str(nights), (0,20), color = "white")
    ims.append((plt.imshow(world, cmap="inferno", vmin=0, vmax=1),text))

    for woman in women_array:
        woman.clearManList()

    for man in men_array:
        favourite_woman = man.getRemainingPreferences()[0]
        women_array[favourite_woman].addToList(man.getIdentity()) # add the men visiting them to their man_list

    while not all(man.getPosition()[1] == women_array[man.getRemainingPreferences()[0]].getPosition()[1] and man.getPosition()[0] == women_array[man.getRemainingPreferences()[0]].getPosition()[0] for man in men_array):
            moveMen(world, men_array, women_array)
            world = updateWorld(men_array)
            ims.append((plt.imshow(world, cmap="inferno", vmin=0, vmax=1),text))

    for woman in women_array:
        preferred_man = woman.chooseMan()
        if preferred_man is not None:
            rejected_men = woman.getRejectedMen(preferred_man)
            for rejected_man in rejected_men:
                men_array[rejected_man].getRejected()
    for man in men_array:
        man.resetPosition()

    return ims

def tmVisual(fig, ax, men, women):
    ims = []
    nights = 0
    while True:
        if all(len(woman.getManList()) == 1 for woman in women):
            return (fig,ims)
        else:
            ims = nightIterationVisual(ims, ax, nights, men, women)
            plt.figtext(x = 0, y = 1, s = ("Night: " + str(nights)), color = "white")
            nights += 1

fig = plt.figure()
plt.axis()
ax = fig.add_subplot(111)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

men, women = initializePeople(20)
frames = tmVisual(fig=fig, ax=ax, men=men, women=women)
im_ani = animation.ArtistAnimation(frames[0], frames[1], interval = 200, repeat_delay=3000)

# Save as gif
writergif = animation.PillowWriter(fps=30)
im_ani.save('im.gif', writer=writergif)
