import json
import numpy as np
from sklearn.cluster import KMeans

def main():
    data = json.load(open('./graph.json', 'r'))
    buildings = data['buildings']
    coordinates = np.array([[building['center']['lat'], building['center']['lon']] for building in buildings])

    # Choose the number of clusters (K)
    num_clusters = 20

    # Initialize KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters)

    # Fit the KMeans model
    kmeans.fit(coordinates)

    # Get cluster labels for each data point
    cluster_labels = kmeans.labels_

    # Get cluster centers
    cluster_centers = kmeans.cluster_centers_

    # Display cluster labels
    print("Cluster Labels:", len(cluster_labels), cluster_labels)

    # Display cluster centers
    print("Cluster Centers:", cluster_centers)

    # visualize
    import matplotlib.pyplot as plt
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c=cluster_labels, cmap='rainbow')
    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], c='black', marker='x')
    plt.savefig('./images/clusters.png')

    # Store as json
    cluster_centers = cluster_centers.tolist()
    cluster_labels = cluster_labels.tolist()
    data = [{
        "center": center,
        "nodes": [i for i in range(len(buildings)) if cluster_labels[i] == j]
    } for j, center in enumerate(cluster_centers)]

    with open("./data/clusters.json", "w") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    main()