
#Definere posisjon og fart sånn som masse og radius så det ser bedre ut?
class Disc:
    #Class attributes, common for all discs
    mass = 1
    radius = 0.01

    collision_count = 0 #Teller alle gangene en partikkel har krasja, hvis den øker så fjernes eller kanselleres? de framtidige krasjene til lista med en mindre collision_count
    last_collided = 0 #Alle starter med 0 her (eller -1 kanskje?), forrige tid den krasja, brukes i TC_model. Lage en funksjon som legger til en når den kolliderer?
    t_c = 0.1 #Bare valgt selv, global variabel?

    def __init__(self, position: list, velocity: list):
        self.position = position    #Position x and y
        self.velocity = velocity    #Velocity v_x and v_y
    
    def set_velocity(self, velocity: list):
        self.velocity = velocity

    def set_last_collided(self, time_collision):
        last_collided = time_collision
    
    #Returns true or false so Xi = 1 or Xi != 1
    def TC_model(self, time):
        if (time - self.last_collided) < self.t_c:
            return True
        return False

    def move_disc(self, time):
        self.position[0] += self.velocity[0]*time
        self.position[1] += self.velocity[1]*time