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

def evaluate_makespan(individual,n_jobs,n_machines):
    # each machine has a end time
    machine_time = [0 for _ in range(n_machines)]

    # more recent end time of the job
    job_time = [0 for _ in range(n_jobs)]

    for operation in individual:
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

    individual = []
    for _ in range(n_jobs*n_machines):
        first_operations = [(sequence[0],idx) for idx,sequence in enumerate(sequences) if len(sequence)>0]
        operation = random.choice(first_operations)
        
        idx = operation[1]
        sequences[idx].remove(operation[0])
        
        individual.append(operation[0])
    
    return individual

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

def update_position():
    pass

def execute(swarm,wc,wb,wg,n_jobs,n_machines):
    # the start position for each particle is the best position
    particle_best = copy.deepcopy(swarm)

    # criterio de parada (depois colocar como parametro vindo main)
    iteracoes = 3
    
    # makespan of each particle best position
    particle_makespan = [evaluate_makespan(p,n_jobs,n_machines) for p in particle_best]
    
    global_best = find_best(swarm,particle_best,particle_makespan,n_jobs,n_machines)


def main():
    file = "datasets//exemplo1.txt"
    n_jobs, n_machines, operations = read_file(file)

    swarm_size = 3
    swarm = generate_swarm(swarm_size,n_jobs,n_machines,operations)

    # cognitive coefficients
    wc = 0.2   # particle current position
    wb = 0.3   # particle best position
    wg = 0.5   # swarm best position
    
    execute(swarm,wc,wb,wg,n_jobs,n_machines)

main()
