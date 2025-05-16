from vpython import *

ceiling = 2

#width/2
wall = 1.5

#ball radius
r = 0.2

#floor thick
th = 0.05


class ball:
    def __init__(self, position, col, mass, acc, vel, netF):
        self.position = position
        self.mass = mass
        self.acc = acc
        self.vel = vel
        self.body = sphere(pos=position, radius=r, color=col)
        self.netF = netF

    def KE(self):
        return 0.5 * self.mass * mag(self.vel)**2
        

        
#dampening factor
elastic = 1

g = 9.81

dt = 0.001

balls = [
ball(position=vec(-1,0.4,0), col=color.red, mass=1, acc=vec(0,0,0), vel=vec(1,0,0), netF=vec(0,0,0)),
ball(position=vec(1,0.6,0), col=color.green, mass=1, acc=vec(0,0,0), vel=vec(-1,0,0), netF=vec(0,0,0)),
ball(position=vec(1.5,0.85,0), col=color.orange, mass=1, acc=vec(0,0,0), vel=vec(-3,3,0), netF=vec(0,0,0)),
ball(position=vec(-1.3,1,0), col=color.purple, mass=1, acc=vec(0,0,0), vel=vec(-3,3,0), netF=vec(0,0,0)),
]

t = 0
while True:
    rate(700)
    
    for i in range(0, len(balls)):
        Fgrav = vec(0, -balls[i].mass * g, 0)

        balls[i].netF = Fgrav

        balls[i].acc = balls[i].netF/balls[i].mass
        balls[i].vel += balls[i].acc * dt
        balls[i].body.pos += balls[i].vel * dt

        if (balls[i].body.pos.y <= r) or (balls[i].body.pos.y >= ceiling-r):
            balls[i].vel.y *= -1 * elastic

        if (balls[i].body.pos.x <= -wall) or (balls[i].body.pos.x >= wall):
            balls[i].vel.x *= -1 * elastic
            
        for j in range(1, len(balls)):
            if (i != j) and (mag(balls[i].body.pos - balls[j].body.pos) <= (balls[i].body.radius + balls[j].body.radius)):
                line_col = balls[i].body.pos - balls[j].body.pos
                theta = -atan(line_col.y/line_col.x)
                
                #balls[i].pos = vec((balls[i].body.radius + balls[j].body.radius)*cos(-theta),(balls[i].body.radius + balls[j].body.radius)*sin(-theta), 0)
                
                #change of basis
                v1 = vec(balls[i].vel.x * cos(theta) - balls[i].vel.y * sin(theta), balls[i].vel.x * sin(theta) + balls[i].vel.y * cos(theta), 0)
                v2 = vec(balls[j].vel.x * cos(theta) - balls[j].vel.y * sin(theta), balls[j].vel.x * sin(theta) + balls[j].vel.y * cos(theta), 0)
                
                v1f = vec(0,0,0)
                v2f = vec(0,0,0)
                
                #conservation of momentum/energy
                v1f.x = (balls[i].mass*v1.x + 2*balls[j].mass*v2.x - balls[j].mass*v1.x)/(balls[i].mass + balls[j].mass)
                v2f.x = v1.x - v2.x + v1f.x
                v1f.y = v1.y
                v2f.y = v2.y
                
                #change of basis
                balls[i].vel = vec(v1f.x*cos(theta) + v1f.y * sin(theta), -v1f.x*sin(theta) + v1f.y*cos(theta), 0)
                balls[j].vel = vec(v2f.x*cos(theta) + v2f.y * sin(theta), -v2f.x*sin(theta) + v2f.y*cos(theta), 0)
    
    t += dt
    
    
