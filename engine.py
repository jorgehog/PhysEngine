import matplotlib.pyplot as plt
import numpy as np

class GridMatrix:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.objects = [0];
        
        self.grid = np.zeros([n,m])

    def reset_grid(self):
        self.grid = np.zeros([n,m])

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
        
        origin_x, origin_y = Object.origin
        print "Green light given to object with origin", origin_x, " ",origin_y
        self.objects.append(Object);
        

    def RedLight(self, Object):
        Object.color = "r";
        origin_x, origin_y = Object.origin
        print "Red light given to object with origin", origin_x, " ",origin_y
        self.objects.append(Object);

    def remove_object(self, location):
          self.objects[self.grid[location[0],location[1]]] = 0;



 


class Engine:
    def __init__(self, grid_resolution=[100,100], T=60, dt=0.01):
        self.res = grid_resolution
        self.set_parameters_default();

        self.current_time = 0;

    def initialize_grid(self, Lx, Ly):
        self.boundaries = [Lx,Ly]
        self.world = GridMatrix(Lx*self.res[0], Ly*self.res[1])

    def set_parameters_default(self):
        self.parameters = {}
        self.parameters['g'] = 9.81

    def add_object(self, newobject):
        newobject.scale_parameters(self.res)
       

        self.world.append(newobject)

    def initialize_world(self, objects, size):
        self.initialize_grid(size[0],size[1])

        for newobject in objects:
            self.add_object(newobject)

        self.draw()

    def draw(self):
        my_objects = []
        for exsisting in self.world.objects:
            if exsisting != 0:
                my_objects.append(exsisting)

        for Object in my_objects:
            Object.draw(self.res)
            plt.hold("on")

        plt.axis([0,self.boundaries[0],0,self.boundaries[1]])
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.title("time = %g s" % self.current_time)
        plt.show()

    def iterate(self):
        """stress"""

        self.current_time += self.dt;
    def start(self):
        pass        


class Object:
    def __init__(self, sticky=True, mass="std"):
        self.sticky = sticky
        self.origin = "not implemented"
        self.color = 'b'

        self.mass = set_mass(mass)
    def set_origin(self, origin):
        self.origin = origin;
    def set_mass(self, M):
        return self.area()
    
    def draw():
        """Implement"""
    def check_blocked(self, world):
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
        
    def area(self):
        return self.dx*self.dy;
    
    def draw(self, res):
        c = self.color;
        x0, y0 = self.origin;
        dx = self.dx;
        dy = self.dy;

        hx = np.array([x0, x0+dx])/res[0]
        hy_bottom = np.array([y0,y0])/res[1];
        hy_top = np.array([y0+dy,y0+dy])/res[1];
        
        hx_left = np.array([x0,x0])/res[0]
        hy = np.array([y0,y0+dy])/res[1]
        hx_right = np.array([x0+dx, x0+dx])/res[0];

        plt.plot(hx,hy_bottom,c)
        plt.plot(hx,hy_top,c)
        plt.plot(hx_left, hy, c)
        plt.plot(hx_right, hy, c)

    def check_grid_space(self, world):
        origin_x, origin_y = self.origin
        dx = self.dx
        dy = self.dy

    
        if (origin_x + dx) < 0 or (origin_x + dx) > world.n:
            print "Object placement failed. Outside grid."
            return False
        elif (origin_y +dy) < 0 or (origin_y + dy) > world.m:
            print "Object placement failed. Outside grid."
            return False
        return True

    def check_blocked(self, world):
        origin_x, origin_y = self.origin
        dx = self.dx
        dy = self.dy

        for x in range(origin_x+1, origin_x+dx):
            for y in range(origin_y+1, origin_y +dy):
                    if world.grid[x][y] != 0:
                        if world.objects[int(world.grid[x][y])] != 0:
                            print "Object path blocked"
                        
                            return False
     
                    
        return True

    def scale_parameters(self, res):
        for i in [0,1]:
            self.origin[i]*=res[i];
        self.dx*=res[0];
        self.dy*=res[1];
        
    def mark_grid(self, world):
        x0, y0 = self.origin
        dx, dy = self.dx, self.dy;
        
        world.grid[x0:(x0 + dx), y0:(y0 + dy)] = len(world.objects)-1;



class Circle(Object):
    def __init__(self, r, sticky=True):
        self.r = r;
        self.sticky = sticky;

    def area(self):
        return np.pi*self.r**2    

    def mark_grid(self,world):
        x0, y0 = self.origin
        r = self.r

        for theta in np.linspace(0,2*np.pi):
            for ri in np.linspace(0,r):
                x = x0 + round(ri*np.cos(theta))
                y = y0 + round(ri*np.sin(theta))

                world.grid[x,y] = len(world.objects)-1;

        
        
    def check_blocked(self, world):
        origin_x, origin_y = self.origin
        r = self.r

        for theta in np.linspace(0,2*np.pi,100):
            x = origin_x + round((self.res[0]*r-1)*np.cos(theta))
            y = origin_y + round((self.res[1]*r-1)*np.sin(theta))
            if world.objects[int(world.grid[x][y])] != 0:
                print "Object path blocked"
                        
                return False

        return True

    def check_grid_space(self, world):
        origin_x, origin_y = self.origin
        r = self.r

        for theta in np.linspace(0,2*np.pi,100):
            x = origin_x + int((self.res[0]*r-1)*np.cos(theta))
            y = origin_y + int((self.res[1]*r-1)*np.sin(theta))
            if x < 0 or x > world.n:
                print "Object placement failed. Outside grid."
                return False
            
            elif y < 0 or y > world.m:
                print "Object placement failed. Outside grid."
                return False
        return True

    def scale_parameters(self, res):
        for i in [0,1]:
            self.origin[i]*=res[i];

        self.res = res;

    def draw(self, res):
        c = self.color;
        x0, y0 = self.origin;
        r = self.r

        theta = np.linspace(0,2*np.pi,100)
        x = x0/res[0] + r*np.cos(theta)
        y = y0/res[1] + r*np.sin(theta)
           
        plt.plot(x, y, c)


        
def main():
    physics = Engine()

    object0 = Circle(2, sticky=False)
    object0.set_origin([10,18])
    
    object1 = Box(10,2)
    object1.set_origin([2,5])
    
    object2 = Box(5,2)
    object2.set_origin([12,4])

    object3 = Circle(1)
    object3.set_origin([2,2])

    objects = [eval("object%d" % k) for k in range(3)]

    world_dim = [20,20]

    physics.initialize_world(objects,world_dim)
    physics.start()

    

main()
    

            
        
        
        
