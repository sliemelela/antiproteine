from code.classes import district, cable
import random, copy

if __name__ == "__main__":
    
    # Generating district object
    data_folder = "district-2"
    district = dt.District(data_folder)

    # Generating cluster object
    clust = cluster.Cluster(district)
    result = clust.run_cluster()
    
    vis.visualise(result["district"])
