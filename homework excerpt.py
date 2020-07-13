import numpy as np
import pylab as plt # pylab == matplotlib.pyplot

def numerical_simulation(f,t,x,t0=0.,dt=1e-4,ut=None,ux=None,utx=None,return_u=False):
  """
  simulate x' = f(x,u) 

  input:
    f : R x X x U --> X - vector field
      X - state space (must be vector space)
      U - control input set
    t - scalar - final simulation time
    x - initial condition; element of X

    (optional:)
    t0 - scalar - initial simulation time
    dt - scalar - stepsize parameter
    return_u - bool - whether to return u_

    (only one of:)
    ut : R --> U
    ux : X --> U
    utx : R x X --> U

  output:
    t_ - N array - time trajectory
    x_ - N x X array - state trajectory
    (if return_u:)
    u_ - N x U array - state trajectory
  """
  t_,x_,u_ = [t0],[x],[]
  
  inputs = sum([1 if u is not None else 0 for u in [ut,ux,utx]])
  assert inputs <= 1, "more than one of ut,ux,utx defined"

  if inputs == 0:
    assert not return_u, "no input supplied"
  else:
    if ut is not None:
      u = lambda t,x : ut(t)
    elif ux is not None:
      u = lambda t,x : ux(x)
    elif utx is not None:
      u = lambda t,x : utx(t,x)

  while t_[-1]+dt < t:
    if inputs == 0:
      _t,_x = t_[-1],x_[-1]
      dx = f(t_[-1],x_[-1]) * dt
    else:
      _t,_x,_u = t_[-1],x_[-1],u(t_[-1],x_[-1])
      dx = f(_t,_x,_u) * dt
      u_.append( _u )

    x_.append( _x + dx )
    t_.append( _t + dt )

  if return_u:
    return np.asarray(t_),np.asarray(x_),np.asarray(u_)
  else:
    return np.asarray(t_),np.asarray(x_)
# DE parameters
m = 250
k = 50
c = 10
dt = 1e-2 # coarse timestep
freq = 1/(2*np.pi) # one radian/second
t = 5/freq # five periods
x0 = np.hstack((0.,0.)) # start at rest at origin

def u(t):
  return a*np.sin(w*t)

def f1(t,x,u):
    p1,dp1 = x[0],x[1] # position, velocity
    return np.hstack([dp1,-(c/m)*dp1 - (k/m)*p1 + (k/(m))*u])
  
def f2(t,x,u):
    p2,dp2 = x[0],x[1] # position, velocity
    return np.hstack([dp2,-(c/m)*dp2 + (k/m)*p2 - (k/(m))*u])
  

a = 0.01 # meters
w = 1 # rad/sec


t2,x2 = numerical_simulation(f2,t,x0,dt=dt,ut=u)
t1,x1 = numerical_simulation(f1,t,x0,dt=dt,ut=u)
u_t = np.array([u(t) for t in t1])





motion = 0.5*(x1[:,0] + x2[:,0])

fig = plt.figure(figsize=(8,8));

ax = plt.subplot(511)
ax.plot(t1,x1[:,0],'.-')
ax.set_xticklabels([])
ax.set_ylabel(r'position $q_1$')

ax = plt.subplot(512)
ax.plot(t2,x2[:,0],'.-')
ax.set_xticklabels([])
ax.set_ylabel(r'position $q_2$')


ax = plt.subplot(513)
ax.plot(t1,u_t,'.-')
ax.set_xlabel('time (sec)')
ax.set_ylabel('input $u$ ')

plt.tight_layout()