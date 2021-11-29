import numpy as np
import draw_utils


############ plot nullclines and vector fields ############

'''
Consider following equations:
dx/dt = -x + a*x + y*x**2
dy/dt = b - a*y - y*x**2
'''

def F(X, Y, params):
    return -X + params[0]*X + Y*X**2

def G(X, Y, params):
    return params[1] - params[0]*Y + Y*X**2

def f_null1(x, params):
    return x / (params[0] + x**2)

def f_null2(x, params):
    return params[1] / (params[0] + x**2)

params = [.1,.2]
draw_utils.plot_phaseplane(F, G, f_null1, f_null2, extra_params=params,
                           x_range=[0,3], y_range=[0,3])



############ create animation ############

t = np.linspace(0, 100, 1000)
var1 = np.sin(0.2*t)
var2 = np.cos(0.3*t)

draw_utils.phaseplane_animation(t, var1, var2)

# You can also plot nullclines by passing nullcline information with a list:
# draw_utils.phaseplane_animation(t, var1, var2, [f_null1, f_null2, extra_params])

