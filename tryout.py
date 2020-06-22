from code.classes import district as dt
from code.algorithms import randomize, random_swap, random_greedy_swap, greedy, annealing, cluster
from code.visualisation import visualise as vis

if __name__ == "__main__":
    
    # Generating district object
    data_folder = "district-3"
    district = dt.District(data_folder)

    # Generating cluster object
    clust = cluster.Cluster(district)
    result = clust.run_cluster()