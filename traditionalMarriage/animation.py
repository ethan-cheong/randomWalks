from traditionalMarriage import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
