import Disc
from cmath import sqrt


#Functions for collision with walls

#Typespesifiserer discen til å være en Disc
def time_to_collision_vertical_wall(disc: Disc):
    r = disc.radius
    x_position = disc.position[0]
    x_velocity = disc.velocity[0]
    if x_velocity > 0:
        return (1 - r - x_position)/x_velocity
    elif x_velocity < 0:
        return (r-x_position)/x_velocity
    else:
        return 10000.0 #"Infinity"

def time_to_collision_horizontal_wall(disc: Disc):
    r = disc.radius
    y_position = disc.position[1]
    y_velocity = disc.velocity[1]
    if y_velocity > 0:
        return (1 - r - y_position)/y_velocity
    elif y_velocity < 0:
        return (r-y_position)/y_velocity
    else:
        return 10000.0 #"Infinity"

def velocity_after_collision_vertical_wall(disc: Disc):
    Xi = 1
    return [-Xi*disc.velocity[0], Xi*disc.velocity[1]]    
                                                    #Endre farten til partikkelen med en gang istedenfor å returnere en verdi?

def velocity_after_collision_horizontal_wall(disc: Disc):
    # if disc.TC_model():
    #     Xi = 1
    # else:
    #     Xi = 0.5
    Xi = 1
    return [Xi*disc.velocity[0], -Xi*disc.velocity[1]]    
                                                    #Endre farten til partikkelen med en gang?


#Functions for particle-particle collision
#Using pos instead of x to avoid misunderstandings

def time_to_particle_particle_collision(disc_i: Disc, disc_j: Disc):
    delta_v = [disc_j.velocity[0] - disc_i.velocity[0], disc_j.velocity[1] - disc_i.velocity[1]] #Absoluttverdier?
    delta_pos = [disc_j.position[0] - disc_i.position[0], disc_j.position[1] - disc_i.position[1]]
    product_delta_vx = delta_v[0]*delta_pos[0] + delta_v[1]*delta_pos[1]
    R_ij    = (disc_i.radius + disc_j.radius)                                                    #Kjøres flere ganger, forenkle litt
    d       = (product_delta_vx)**2 - (delta_v[0]**2 + delta_v[1]**2)*((delta_pos[0]**2 + delta_pos[1]**2) - R_ij**2)
    if (product_delta_vx >= 0) or (d >= 0): 
        return 10000        #Uendelig
    else:
        return -(product_delta_vx + sqrt(d))/(delta_v[0]**2 + delta_v[1]**2)

#Returns velocities for both particles
def velocities_after_particle_particle_collision(disc_i: Disc, disc_j: Disc):
    if disc_i.TC_model() or disc_j.TC_model():
        Xi = 1
    else:
        Xi = 0.5
    R_ij            = (disc_i.radius + disc_j.radius)
    delta_t         = time_to_particle_particle_collision(disc_i, disc_j)
    #x_i'
    pos_i_collision = [disc_i.position[0] + disc_i.velocity[0]*delta_t, disc_i.position[1] + disc_i.velocity[1]*delta_t] #[x_i + v_xi*delta_t, y_i + v_yi*delta_t]
    pos_j_collision = [disc_j.position[0] + disc_j.velocity[0]*delta_t, disc_j.position[1] + disc_j.velocity[1]*delta_t]
    delta_v         = [disc_j.velocity[0] - disc_i.velocity[0], disc_j.velocity[1] - disc_i.velocity[1]]                 #Absoluttverdier?
    delta_pos       = [disc_j.position[0] - disc_i.position[0], disc_j.position[1] - disc_i.position[1]]                 #------||-------
    #Taking all the values that doesn't change between v_i and v_j and putting it into a constant
    constant        = (1 + Xi)(delta_v[0]*delta_pos[0] + delta_v[1]*delta_pos[1])/(R_ij**2*(disc_i.mass + disc_j.mass)) 

    velocity_i_after = [disc_i.velocity[0] + disc_j.mass*constant*pos_i_collision[0], disc_i.velocity[1] + disc_j.mass*constant*pos_i_collision[1]]
    velocity_j_after = [disc_j.velocity[0] - disc_i.mass*constant*pos_j_collision[0], disc_j.velocity[1] - disc_i.mass*constant*pos_j_collision[1]]

    return velocity_i_after, velocity_j_after

