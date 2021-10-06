import random
import copy

def read_file(file_name):
    f = open(file_name, "r")
    n_jobs, n_machines = [int(valor) for valor in f.readline().split()]

    operations = []

    for i in range(1, n_jobs+1):
        line = f.readline().split()

        for j in range(0, n_machines*2, 2):
            operations.append( (i, int(line[j]), int(line[j+1])) )

    f.close()
    return n_jobs, n_machines, operations

def evaluate_makespan(particle,n_jobs,n_machines):
    # each machine has a end time
    machine_time = [0 for _ in range(n_machines)]

    # more recent end time of the job
    job_time = [0 for _ in range(n_jobs)]

    for operation in particle:
        job,machine,time = operation

        max_time = max(machine_time[machine],job_time[job-1])

        machine_time[machine] = max_time + time
        job_time[job-1] = machine_time[machine]
    
    # job that has the max time to complete
    makespan = max(job_time)
    return makespan

# represents a solution to the problem
def create_particle(n_jobs,n_machines,operations):
    sequences = []   # operations sequences of the jobs
    start = 0
    stop = n_machines
    
    for _ in range(n_jobs):
        sequences.append(operations[start:stop])
        
        start = stop
        stop += n_machines 

    particle = []
    for _ in range(n_jobs*n_machines):
        first_operations = [(sequence[0],idx) for idx,sequence in enumerate(sequences) if len(sequence)>0]
        operation = random.choice(first_operations)
        
        idx = operation[1]
        sequences[idx].remove(operation[0])
        
        particle.append(operation[0])
    
    return particle

def generate_swarm(swarm_size, n_jobs, n_machines, operations):
    swarm = []
    for _ in range(swarm_size):
        particle = create_particle(n_jobs, n_machines, operations)
        swarm.append(particle)
    
    return swarm

# discovery particle and global best position
def find_best(swarm,particle_best,particle_makespan,n_jobs,n_machines):
    min_makespan = float("inf")
    
    for position,particle in enumerate(swarm):
        makespan = evaluate_makespan(particle,n_jobs,n_machines)

        # update particle best position
        if makespan < particle_makespan[position]:
            particle_best[position] = particle
            particle_makespan[position] = makespan
        
        # update swarm best position
        if makespan < min_makespan:
            min_makespan = makespan
            global_best = particle
    
    return global_best

def insert_position(operations,position):
    for idx,operation in enumerate(operations):
        
        if operation not in position:
            position.append(operation)
            break
        
    return operations[idx+1:]

def update_position(wc,wb,n,swarm,particle_best,global_best,idx):
    new_position = []

    # copys of particles because of the pop function use
    aux_swarm = copy.deepcopy(swarm[idx])
    aux_part_best = copy.deepcopy(particle_best[idx])
    aux_glob_best = copy.deepcopy(global_best)

    for _ in range(n):
        u = random.random()
        u = round(u,2)

        # position from current position
        if u <= wc:
            aux_swarm = insert_position(aux_swarm,new_position)

        # position from best particle position
        elif u > wc and u <= wc+wb:
            aux_part_best = insert_position(aux_part_best,new_position)

        # position from best global position
        else:
            aux_glob_best = insert_position(aux_glob_best,new_position)
    
    return new_position

def execute(swarm,wc,wb,n_jobs,n_machines,iterations=100):
    swarm_size = len(swarm)
    
    # the start position for each particle is the best position
    particle_best = copy.deepcopy(swarm)

    # number of operations
    n_ops = n_jobs * n_machines

    # stopping criteria: iterations number
    for _ in range(iterations):
        # makespan of each particle best position
        particle_makespan = [evaluate_makespan(p,n_jobs,n_machines) for p in particle_best]
        
        # global best position
        global_best = find_best(swarm,particle_best,particle_makespan,n_jobs,n_machines)
        
        for idx in range(swarm_size):
            new_position = update_position(wc,wb,n_ops,swarm,particle_best,global_best,idx)
            swarm[idx] = new_position
    
    return global_best

def main():
    file = "datasets//ft06.txt"
    n_jobs, n_machines, operations = read_file(file)

    # cognitive coefficients
    wc = 0.20   # particle current position
    wb = 0.30   # particle best position
    wg = 0.50   # swarm best position
    
    values = []
    for _ in range(10):
        swarm_size = 100
        swarm = generate_swarm(swarm_size,n_jobs,n_machines,operations)

        iterations = 50
        best_particle = execute(swarm,wc,wb,n_jobs,n_machines,iterations)
        values.append(evaluate_makespan(best_particle,n_jobs,n_machines))
    
    print(min(values))

main()
