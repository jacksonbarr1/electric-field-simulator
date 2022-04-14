from vpython import *
#Web VPython 3.2

K = 9e9

draw_grid(10, 1)


# System takes a list of Charge objects and a tuple containing the location of an observation point
# System([], ())
class System():
    def __init__(self, charges, p_pos):
        self.charges = charges
        self.p_pos = p_pos
        
        # Creates a sphere on the grid at the location of the observation point as a reference point
        self.p=sphere(pos=vector(p_pos[0], p_pos[1], 0), radius=0.25, color=color.cyan)
        
        # Uses the three respective methods to determine the direction of the electric field due to each point charge, 
        # the magnitude of each field, and the sum of each field using Superposition Principle
        self.field_vectors = self.find_vectors()
        self.fields = self.calculate_fields()
        self.E = self.sum_fields()
        
        print("E = {} N/C".format(self.E))
        print("|E| = {} N/C".format(mag(self.E)))
        print("\u03B8 = {}\u00B0".format(round(atan(self.E.y/self.E.x)*180/pi)))
        
        # Creates an arrow in the direction of the electric field
        E_arrow=arrow(pos=self.p.pos, axis=norm(self.E), length=1.5)
        
    def find_vectors(self):
        # Loops through each charge and determines the direction of the charge's field vector at the observation point
        # Returns a dictionary with {charge name : vector} format
        field_vectors = {}
        for charge in self.charges:
            r = self.p.pos - charge.charge.pos
            field_vectors[charge.name] = r
        return field_vectors
    
    def calculate_fields(self):
        # Uses the field vectors previously determined via find_vectors() to calculate each specific charges magnetic field at the observation point
        # Returns a dictionary with {charge name : electric field vector} format
        fields = {}
        for charge in self.charges:
            r = self.field_vectors[charge.name]
            E = K*charge.q*norm(r)/mag(r)**2
            fields[charge.name] = E
        return fields
        
    def sum_fields(self):
        # Uses the superposition principle to sum each charge's electric field at the point to yield one final electric field vector
        E = vector(0,0,0)
        for key, value in self.fields.items():
            E += value
        return E
            
        
        
# Creates a charge object to be used in establishing a System
# Charge((), float, '')
            
class Charge():
    def __init__(self, position, q, name):
        self.position = position
        self.name = name
        self.q = q
        if q > 0:
            self.charge = sphere(pos=vector(position[0], position[1], 0), radius=1*10**8*q, color=color.red)
        else:
            self.charge = sphere(pos=vector(position[0], position[1], 0), radius=1*10**8*q, color=color.blue)
        self.label = label(pos=vector(position[0]-1, position[1], 0), text='q={} C'.format(q))
        
        
def draw_grid(grid_max, spacing):
    # grid_max is the maximum length of the grid in either direction
    # spacing represents the intervals in which grid lines are drawn
    
    for x in range(-grid_max, grid_max+spacing, spacing): 
        # Loops through all values of the grid with a step value of 'spacing' 
        # in order to create vertical lines for y axis
        curve(pos=[vector(x, grid_max, 0), vector(x, -grid_max, 0)])
        
    for y in range(-grid_max, grid_max+spacing, spacing):
        # Performs the same function as the above loop, creating lines in the x direction
        curve(pos=[vector(grid_max, y, 0), vector(-grid_max, y, 0)])


q1=Charge((5, 3), 3e-9, 'alpha')
q2=Charge((1, 5), 8e-9, 'beta')
q3=Charge((-2,3), -1e-8, 'zeta')
ex = System([q1, q2, q3], (1, 3))


