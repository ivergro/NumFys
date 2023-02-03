import Disc
import collisions
import heapq
import CollisionObject

#List element = tuple(tid kollisjon, tuple(disc_i, disc_j/vegg), sum_collision_counters)
def main():
    global_clock = 0.0
    listy, disc_list = one_particle()
    #length = len(listy) 

    #Kjører til tiden første kollisjon vil skje 
    print(f"""Values at start\n
        velocity: {disc_list[0].velocity}
        position: {disc_list[0].position}
        collisions: {disc_list[0].collision_count} """ )
    counter = 0
    while counter < 6:
        # if len(listy) > 0:
        forward_time, collision_object = heapq.heappop(listy)

        #Checks if the collision counter has changed over collisions
        temp_collision_counter = collision_object.object_1.collision_count
        collision_with_wall = True
        if not isinstance(collision_object.object_2, str):
            temp_collision_counter += collision_object.object_2.collision_count
            collision_with_wall = False

        if collision_object.collision_counter == temp_collision_counter:
            for i in range(len(disc_list)):
                disc_list[i].move_disc(forward_time)
            global_clock += forward_time

            #Kollisjon!
            if collision_with_wall:
                if collision_object.object_2 == "h_wall":
                    new_velocity_1 = collisions.velocity_after_collision_horizontal_wall(collision_object.object_1)
                else:
                    new_velocity_1 = collisions.velocity_after_collision_vertical_wall(collision_object.object_1)
                
            else:
                new_velocity_1, new_velocity_2 = collision_object.velocity_after_particle_particle_collision(collision_object.object_1, collision_object.object_2)
                collision_object.object_2.set_velocity(new_velocity_2)
                collision_object.object_2.set_last_collided(global_clock)
                collision_object.object_2.collision_count += 1

            collision_object.object_1.set_velocity(new_velocity_1)
            collision_object.object_1.set_last_collided(global_clock)
            collision_object.object_1.collision_count += 1
            
            #Kalkuler nye kollsijoner etc
            print(f"""Values after collision
                    velocity: {disc_list[0].velocity}
                    position: {disc_list[0].position}
                    collisions: {disc_list[0].collision_count} 
                    
                    After time: {global_clock}""" )
            #Recalcuclating collisions
            if collision_with_wall:
                new_collision_list = collisionRecheck([collision_object.object_1], disc_list, global_clock)
            else:
                new_collision_list = collisionRecheck([collision_object.object_1, collision_object.object_2], disc_list, global_clock)
            listy.extend(new_collision_list)
        counter += 1
    





def one_particle():
    disc_1                 = Disc.Disc([0.5, 0.0], [0.1, 0.1])
    disc_list              = [disc_1]        #Trengs den i det hele tatt?

    time_until_collision_h = collisions.time_to_collision_horizontal_wall(disc_1)
    time_until_collision_v = collisions.time_to_collision_vertical_wall(disc_1)
    collision_object_v     = CollisionObject.CollisionObject(disc_1, "v_wall")
    collision_object_h     = CollisionObject.CollisionObject(disc_1, "h_wall")
    listy                  = [(time_until_collision_v, collision_object_v), (time_until_collision_h, collision_object_h)]
    return listy, disc_list

#Checks all new collisions for the disc/discs that collided
def collisionRecheck(discs_collided, disc_list, global_clock):
    new_collisions = []
    for disc in discs_collided:

        #Checking wall collisions first
        time_collision_h_wall = collisions.time_to_collision_horizontal_wall(disc)
        time_collision_v_wall = collisions.time_to_collision_vertical_wall(disc)
        if time_collision_h_wall < 10000.0:
             new_collisions.append((time_collision_h_wall, CollisionObject.CollisionObject(disc, "h_wall")))
        if time_collision_v_wall < 10000.0:
            new_collisions.append((time_collision_v_wall, CollisionObject.CollisionObject(disc, "v_wall")))
        #Recalculating all new crash possibilities with all the oter discs
        for i in range(len(disc_list)):
            #Making sure that I only include collisions with a reasonable time, and do not include collision with itself
            if collisions.time_to_particle_particle_collision(disc, disc_list[i]) < 1000 and (disc_list[i] != disc):
                new_collisions.append(collisions.time_to_particle_collision(disc,disc_list[i]) + global_clock, CollisionObject.CollisionObject(disc, disc_list[i]))
    return new_collisions


    

def initializer():
    pass


main()