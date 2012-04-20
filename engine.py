from scitools.std import *

class GridMatrix:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.objects = [0];
        
        self.grid = zeros([n,m])

    def reset_grid(self):
        self.grid = zeros([n,m])

    def append(self, Object):
        NotBlocked = False
        
        WithinGrid = Object.check_grid_space(self)
        if WithinGrid:
            NotBlocked = Object.check_blocked(self)
        
        if NotBlocked:
            self.GreenLight(Object);
            return True
        else:
            self.RedLight(Object);
            return False

    def GreenLight(self, Object):
        Object.color = "g";
        Object.mark_grid(self);
        
        COM_x, COM_y = Object.COM
        #print "Green light given to object with COM", COM_x, " ",COM_y
        self.objects.append(Object);
        

    def RedLight(self, Object):
        Object.color = "r";
        COM_x, COM_y = Object.COM
        #print "Red light given to object with COM", COM_x, " ",COM_y
        self.objects.append(Object);

    def remove_object(self, location):
          self.objects[self.grid[location[0],location[1]]] = 0;



 


class Engine:
    def __init__(self, grid_resolution=[100,100]):
        self.res = grid_resolution
        self.set_parameters_default();

        self.t = 0;

    def initialize_grid(self, Lx, Ly):
        self.boundaries = [Lx,Ly]
        self.world = GridMatrix(Lx*self.res[0], Ly*self.res[1])

    def set_parameters_default(self):
        self.parameters = {}
        self.parameters['g'] = 9.81

    def add_object(self, newobject):
        self.world.append(newobject)

    def initialize_world(self, objects, size):
        for newobject in objects:
            newobject.scale_parameters(self.res)
            
        self.initialize_grid(size[0],size[1])

        for newobject in objects:
            self.add_object(newobject)

        self.draw()
        
    def update_world(self, objects):
        self.initialize_grid(self.boundaries[0], self.boundaries[1])
        for newobject in objects:
            self.add_object(newobject)
        self.draw()
        

    def draw(self):
        my_objects = []
        
   
        a = 0
        i=1
        display = False
        for exsisting in self.world.objects:
            if exsisting != 0:
                my_objects.append(exsisting)

        for Object in my_objects:
            if i==len(my_objects):
                display=True
            Object.draw(self.res, display)
            if a == 0:
                axis([0,self.boundaries[0],0,self.boundaries[1]])
                xlabel("x [m]")
                ylabel("y [m]")
                title("time = %g s" % self.t)
                hold("on")
                a = 1
            i += 1
        hold("off")        

        

        
    def start(self, T=60, dt=0.01):
        g = self.parameters['g'];

        self.t = 0;
        while self.t < T:
            new_objects=[]
            for cobject in self.world.objects:
                if cobject != 0:
                    new_objects.append(cobject)
                    if cobject.sticky is False:
                        COM = cobject.COM;
                        
                        a_vec = array([0,-g])
                        cobject.v = cobject.v + a_vec*dt;
                        v = cobject.get_v();
                        cobject.COMprev = COM.copy()
                        cobject.set_COM(COM + dt*cobject.v*(v > 0.1))
                        
                        NoContact, target, impact = cobject.check_blocked(self.world, ret_info = True)

##                        if target != 0:
##                            if target.sticky ==False and target.ID in [a[0] for a in cobject.recent_collisions]:
##                                print target.ID, "   -    ", cobject.ID
##                                NoContact = True;
                            
                        if not NoContact:
                    
                            cobject.set_COM(0.5*(cobject.COM + cobject.COMprev))
                            
                            target_angle = target.map_angle(impact)
                            target_angle += target.get_angle()
                            print "DETECTED: ", cobject.name(), "colliding with ", target.name(), " at an angle of ", target_angle*180/pi, " degrees."
                            projectile_angle = cobject.get_direction()
                            incl = projectile_angle - target_angle;

                            avg_elasticity = (0.3*target.elasticity+0.7*cobject.elasticity)
                            cobject.v = sign(cobject.v[0])*avg_elasticity*array([v*cos(incl - target_angle), -v*sin(incl - target_angle)])

                            if target.sticky == False:
                                target.v[1] += v*avg_elasticity**2*sin(incl - target_angle);
##                                cobject.recent_collisions.append([target.ID,self.t])
##                                target.recent_collisions.append([cobject.ID,self.t])
        
            self.update_world(new_objects)
            self.t += dt;
##            for old_object in new_objects:
##                if old_object.sticky == False:
##                    for i in range(len(old_object.recent_collisions)):
##                        time, ID = old_object.recent_collisions[i]
##                        if self.t - time > 7*dt:
##                            old_object.recent_collisions.pop(i)
            
            


class Object:
    def __init__(self, sticky=True, mass="std", v0 = [0,0]):
        self.sticky = sticky
        self.color = 'b'
        self.v = array(v0);
        self.angle = 0;

        self.mass = self.set_mass(mass)

    def set_COM(self, COM):
        self.COM = array(COM);
    def set_ID(self, ID):
        self.ID = ID;
    def get_v(self):
        return (self.v[0]**2 + self.v[1]**2)**0.5
    def get_direction(self):
        return arctan(self.v[1]/(self.v[0]+0.00000001))
    def set_mass(self, M):
        return self.area()
    def get_angle(self):
        return 0;
    def area(self):
        "Implement"
##    def get_COM(self):
##        "Implement"
    def draw():
        """Implement"""
    def check_blocked(self, world, ret_info = False):
        """Implement"""
    def check_grid_space(self, world):
        """Implement"""
    def scale_parameters(self, res):
        """Implement"""
    def mark_grid(self, world):
        """Implement"""

class Box(Object):
    def __init__(self, lx, ly, sticky=True):
        self.dx, self.dy = lx, ly
        self.sticky = sticky
        self.angle = 0;
        self.elasticity = 0.3;
        self.ID = None
##    def get_COM(self):
##        th = self.angle;
##        dx, dy = self.dx, self.dy
##        return 0.5*[cos(th)*dx + sin(th)*dx,-sin(th)*dx + cos(th)*dy]
        
    def area(self):
        return self.dx*self.dy;
    def name(self):
        return "box"
    def get_angle(self):
        return self.angle;
    def map_angle(self, impact):
        x, y = impact;
        x0, y0 = self.COM;
        dx = float(self.dx);
        dy = float(self.dy);

        if (x0 - dx/2 + dy/2) <= x <= (x0 + dx/2 - dy/2):
            if y > y0:
                return 0
            else:
                return pi
        else:
            if x > x0 and y > y0:
                xp = x - x0 - dx/2 + dy/2
                yp = y - y0
                if xp > yp:
                    return pi/2
                else:
                    return 0
                
            elif x > x0 and y < y0:
                xp = x - x0 - dx/2 + dy/2
                yp = y - y0 + dy/2

                if yp < dy/2 - xp:
                    return pi
                else:
                    return pi/2;

            elif x < x0 and y < y0:
                xp = x - x0 + dx/2;
                yp = y - y0 + dy/2;
                if xp > yp:
                    return pi
                else:
                    return -pi/2

            elif x < x0 and y > y0:
                xp = x - x0 + dx/2
                yp = y - y0

                if yp < dy/2 - xp:
                    return -pi/2
                else:
                    return 0
            else:
                return "WEIRD"
    
        
        
                
        
    def draw(self, res, display):
        c = self.color;
        x0, y0 = self.COM;
        dx = float(self.dx);
        dy = float(self.dy);

        hx = array([x0-dx/2, x0+dx/2])/res[0]
        hy_bottom = array([y0-dy/2,y0-dy/2])/res[1];
        hy_top = array([y0+dy/2,y0+dy/2])/res[1];
        
        hx_left = array([x0-dx/2,x0-dx/2])/res[0]
        hy = array([y0-dy/2,y0+dy/2])/res[1]
        hx_right = array([x0+dx/2, x0+dx/2])/res[0];

        plot(hx,hy_bottom,c,show=False)
        plot(hx,hy_top,c,show=False)
        plot(hx_left, hy, c,show=False)
        plot(hx_right, hy, c,show=display)

    def check_grid_space(self, world):
        COM_x, COM_y = self.COM
        dx = self.dx
        dy = self.dy

    
        if (COM_x - dx/2) < 0 or (COM_x + dx/2) > world.n:
            print "Object placement failed. Outside grid."
            return False
        elif (COM_y -dy/2) < 0 or (COM_y + dy/2) > world.m:
            print "Object placement failed. Outside grid."
            return False
        return True

    def check_blocked(self, world, ret_info = False):
        COM_x, COM_y = self.COM
        dx = self.dx
        dy = self.dy

        for x in range(COM_x - dx/2 +1, COM_x + dx/2):
            y1 = COM_y - dy/2 + 1
            y2 = COM_y + dy/2 - 1
            if world.grid[x][y1] != 0:
                if world.objects[int(world.grid[x][y1])] != 0:
                        if ret_info == False:
                            print "Object path blocked"
                            return False
                        elif ret_info:
                            return False, world.objects[int(world.grid[x][y1])], 0
            elif world.grid[x][y2] != 0:
                if world.objects[int(world.grid[x][y2])] != 0:
                    if ret_info == False:
                            print "Object path blocked"
                            return False
                    elif ret_info:
                            return False, world.objects[int(world.grid[x][y2])], pi
            
                
        for y in range(COM_y - dy/2 + 1, COM_y + dy/2):
            x1 = COM_x - dx/2 + 1
            x2 = COM_x + dx/2 - 1
            if world.grid[x1][y] != 0:
                if world.objects[int(world.grid[x1][y])] != 0:
                    if ret_info == False:
                        print "Object path blocked"
                        return False
                    elif ret_info:
                        return False, world.objects[int(world.grid[x1][y])], -pi/4
            elif world.grid[x2][y] != 0:
                if world.objects[int(world.grid[x2][y])] != 0:
                    if ret_info == False:
                        print "Object path blocked"
                        return False
                    elif ret_info:
                        return False, world.objects[int(world.grid[x2][y])], pi/4

        if ret_info == False:
            return True
        else:
            return True, 0, 0
    def scale_parameters(self, res):
        for i in [0,1]:
            self.COM[i]*=res[i];

        self.dx*=res[0];
        self.dy*=res[1];
        
    def mark_grid(self, world):
        x0, y0 = self.COM
        dx, dy = self.dx, self.dy;
        self.ID = len(world.objects)

        world.grid[(x0-dx/2):(x0 + dx/2), (y0-dy/2):(y0 + dy/2)] = self.ID;



class Circle(Object):
    def __init__(self, r, sticky=True, v0=[0,0]):
        
        self.r = r;
        Object.__init__(self, v0=v0)
        self.sticky = sticky;
        self.elasticity = 0.99;
        self.ID = None
        self.recent_collisions = []

    def area(self):
        return pi*self.r**2
    def name(self):
        return "circle"
    def map_angle(self, impact):
        return 0;

    def mark_grid(self,world):
        x0, y0 = self.COM
        r = self.r
        self.ID = len(world.objects);

        for theta in linspace(0,2*pi):
            for ri in linspace(0,r):
                x = x0 + round(ri*cos(theta))
                y = y0 + round(ri*sin(theta))
                
                world.grid[x,y] = self.ID;

        
        
    def check_blocked(self, world, ret_info = False):
        COM_x, COM_y = self.COM
        r = self.r

        for theta in linspace(0,2*pi):
            x = COM_x + round((self.res[0]*r)*cos(theta))
            y = COM_y + round((self.res[1]*r)*sin(theta))
            ID = int(world.grid[x][y])
            if ID != self.ID and ID != 0:
                if ret_info == False:
                    print "Object path blocked"
                    return False
                elif ret_info:
                    #print int(world.grid[x][y]), world.objects[int(world.grid[x][y])]
                    return False, world.objects[ID], [x,y]

        if ret_info == False:
            return True
        else:
            return True, 0, 0

    def check_grid_space(self, world):
        COM_x, COM_y = self.COM
        r = self.r

        for theta in linspace(0,2*pi,100):
            x = COM_x + int((self.res[0]*r)*cos(theta))
            y = COM_y + int((self.res[1]*r)*sin(theta))
            if x < 0 or x > world.n:
                print "Object placement failed. Outside grid."
                return False
            
            elif y < 0 or y > world.m:
                print "Object placement failed. Outside grid."
                return False
        return True

    def scale_parameters(self, res):
        for i in [0,1]:
            self.COM[i]*=res[i];
            self.v[i] *= res[i];
        self.res = res;

    def draw(self, res, display):
        c = self.color;
        x0, y0 = self.COM;
        r = self.r

        theta = linspace(0,2*pi,100)
        x = x0/res[0] + r*cos(theta)
        y = y0/res[1] + r*sin(theta)
           
        plot(x, y, c, show=display)


        
def main():
    physics = Engine(grid_resolution=[15,15])

    object0 = Circle(0.1, sticky=False, v0=[0.5,0])
    object0.set_COM([3,5])
    
    object1 = Box(3,1)
    object1.set_COM([3,3])
    
    object2 = Box(1,4)
    object2.set_COM([6,5])

    object3 = Box(7,1)
    object3.set_COM([4,1])

    object4 = Circle(0.1, sticky=False, v0 = [0.5,1])
    object4.set_COM([2,4])

    object5 = Circle(0.1, sticky=False, v0 = [1,0])
    object5.set_COM([1,4])

    object6 = Circle(0.25, sticky=False, v0 = [-3,-3])
    object6.set_COM([8,8])

    object7 = Box(1,4)
    object7.set_COM([8,4])

    object8 = Box(1,1)
    object8.set_COM([1,2])

    object9 = Box(1,1)
    object9.set_COM([7,2])

    objects = [eval("object%d" % k) for k in range(10)]

    world_dim = [10,10]

    physics.initialize_world(objects,world_dim)
    physics.start(dt = 0.07, T = 8)

    

main()
    

            
        
        
        
