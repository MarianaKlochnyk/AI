import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.spatial.distance import cdist

def generate_data(N=1000):
    data = np.random.rand(N, 2)
    return data

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b)**2))

def kmeans_clustering(data, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(data)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    return labels, centers

def hierarchical_clustering(data, n_clusters=5):
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    labels = hierarchical.fit_predict(data)
    return labels

def weighted_cluster_size(data, labels):
    total_size = 0
    for cluster_id in np.unique(labels):
        cluster_points = data[labels == cluster_id]
        center = np.mean(cluster_points, axis=0)
        avg_distance = np.mean([euclidean_distance(p, center) for p in cluster_points])
        total_size += avg_distance * len(cluster_points)
    return total_size / len(data)

if __name__ == "__main__":
    data = generate_data(N=3000)

    k_labels, k_centers = kmeans_clustering(data, n_clusters=5)
    k_weighted_size = weighted_cluster_size(data, k_labels)

    h_labels = hierarchical_clustering(data, n_clusters=5)
    h_weighted_size = weighted_cluster_size(data, h_labels)

    print("Результати кластеризації:")
    print(f"K-means: {len(np.unique(k_labels))} кластерів, середньо-зважений розмір: {k_weighted_size:.4f}")
    print(f"Ієрархічна: {len(np.unique(h_labels))} кластерів, середньо-зважений розмір: {h_weighted_size:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(12,5))

    axes[0].scatter(data[:,0], data[:,1], c=k_labels, cmap='tab10', s=10)
    axes[0].scatter(k_centers[:,0], k_centers[:,1], c='black', s=50, marker='x')
    axes[0].set_title("K-means")

    axes[1].scatter(data[:,0], data[:,1], c=h_labels, cmap='tab10', s=10)
    axes[1].set_title("Ієрархічна кластеризація")

    plt.show()