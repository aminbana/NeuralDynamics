from matplotlib import colors as colors
from matplotlib import pyplot as plt
from matplotlib import animation as animation
import numpy as np

def plot_phaseplane(F, G, f_null1, f_null2, extra_params=[], x_range=[-2.,2.],
                    y_range=[-0.6, 2.], step=0.01, name='phaseplane', figsize=5):
    
    x = np.arange(x_range[0], x_range[1], step)
    y = np.arange(y_range[0], y_range[1], step)
    X,Y = np.meshgrid(x, y)
      
    plt.figure(figsize=(figsize*(x_range[1] - x_range[0])/
                        (y_range[1] - y_range[0]), 5))
    plt.plot(x, f_null1(x, extra_params), label='nullcline 1')
    plt.plot(x, f_null2(x, extra_params), label='nullcline 2')
    
    dx = F(X, Y, extra_params)
    dy = G(X, Y, extra_params)
    
    plt.streamplot(X, Y, dx, dy)
    plt.xlim(x_range)
    plt.ylim(y_range)
    
    plt.xlabel('x')
    plt.ylabel('y')
    
    plt.legend(loc='best')
    
    plt.savefig(name + '.png')    
    

    
def phaseplane_animation(times, var1_vals, var2_vals, Nullclines=None, name='animation', figylen=3,
         figxlen=6, fps = 14., animspeed = 18., traj_color = "C0", plot_color = "C1"):

    '''
    adapted from https://github.com/ruhugu/brainythings/blob/master/scripts/phaseplane.py
    '''
    tmax = max(times)
    t_step = times[1] - times[0]
    fig = plt.figure(figsize = (figxlen, figylen))
    ax_phase = fig.add_subplot(121) 
    ax_var2 = fig.add_subplot(224, xlim=(0, tmax), ylim=(min(var2_vals), max(var2_vals)))
    ax_var1 = fig.add_subplot(222, xlim=(0, tmax), ylim=(min(var1_vals), max(var1_vals)),
                              sharex=ax_var2)
    plt.setp(ax_var1.get_xticklabels(), visible=False)
    ax_phase.set_xlabel("var1")
    ax_phase.set_ylabel("var2")
    ax_var1.set_ylabel("var1")
    ax_var2.set_xlabel("time")
    ax_var2.set_ylabel("var2")
    

         
    if Nullclines != None:
    
        x = np.linspace(min(var1_vals), max(var1_vals), 500)
        f_null1=Nullclines[0]
        f_null2=Nullclines[1]
        extra_params=Nullclines[2]
        plot_null1, = ax_phase.plot(x, f_null1(x, extra_params), linestyle="--", color="gray", 
                               label="var1 nullcline")
        plot_null2, = ax_phase.plot(x, f_null2(x, extra_params), linestyle="-.", color="gray",
                               label="var2 nullcline")
    
    plot_phase, = ax_phase.plot(var1_vals, var2_vals, color=traj_color)
    plot_phasedot, = ax_phase.plot(var1_vals, var2_vals, linestyle="", 
                                  marker="o", color=traj_color)
    plot_var1, = ax_var1.plot(times[0:1], var1_vals[0:1], color=plot_color)
    plot_var2, = ax_var2.plot(times[0:1], var2_vals[0:1], color=plot_color)
    
    ax_phase.legend()
    fig.tight_layout()
    
    # Create the animation
    def update(i_anim, stepsperframe, times, plot_phase, plot_phasedot,
               plot_var1, plot_var2):
        """
        Update function for the animation.
        """
        i = i_anim*stepsperframe
        
        # Update plot
        plot_phase.set_data(var1_vals[:i], var2_vals[:i])
        plot_phasedot.set_data(var1_vals[i-1:i], var2_vals[i-1:i])
        plot_var1.set_data(times[:i], var1_vals[:i])
        plot_var2.set_data(times[:i], var2_vals[:i])
    
        return plot_phase, plot_phasedot, plot_var1, plot_var2
    
    points_per_second = int(animspeed/t_step)
    points_per_frame = int(points_per_second/fps)
    anim_interval = 1000./fps  # Interval between frames in ms
    nframes = int(times.size/points_per_frame)
    
    anim = animation.FuncAnimation(fig, update, frames=nframes,
                                   interval=anim_interval, blit=True,
                                   fargs=(points_per_frame, times,
                                   plot_phase, plot_phasedot, plot_var1, 
                                   plot_var2))

    anim.save(name + '.gif', dpi=100, writer='imagemagick')