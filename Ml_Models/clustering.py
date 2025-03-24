import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class Clustering:
    def __init__(self, data):
        """
        Initialize the Clustering class with data.
        """
        self.data = data

    def preprocess_data(self, features):
        """
        Preprocess the data for clustering.

        Parameters:
            features (list): List of feature columns to use for clustering.
        """
        # Select relevant features
        self.X = self.data[features]

        # Normalize the data
        scaler = StandardScaler()
        self.X_scaled = scaler.fit_transform(self.X)

    def find_optimal_clusters(self, max_clusters=10):
        """
        Find the optimal number of clusters using the Elbow Method.

        Parameters:
            max_clusters (int): Maximum number of clusters to try.
        """
        wcss = []  # Within-Cluster-Sum-of-Squares
        for i in range(1, max_clusters + 1):
            kmeans = KMeans(n_clusters=i, random_state=42)
            kmeans.fit(self.X_scaled)
            wcss.append(kmeans.inertia_)

        # Plot the Elbow Method graph
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, max_clusters + 1), wcss, marker='o', linestyle='--')
        plt.title('Elbow Method')
        plt.xlabel('Number of Clusters')
        plt.ylabel('WCSS')
        plt.show()

    def perform_clustering(self, n_clusters):
        """
        Perform K-Means clustering.

        Parameters:
            n_clusters (int): Number of clusters.
        """
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.data['cluster'] = self.kmeans.fit_predict(self.X_scaled)

    def visualize_clusters(self):
        """
        Visualize the clusters using PCA for dimensionality reduction.
        """
        # Reduce dimensions to 2D using PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.X_scaled)

        # Add PCA components to the data
        self.data['pca_1'] = X_pca[:, 0]
        self.data['pca_2'] = X_pca[:, 1]

        # Plot the clusters
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='pca_1', y='pca_2', hue='cluster', data=self.data, palette='viridis', s=100)
        plt.title('Clustering of Countries')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend(title='Cluster')
        plt.show()


# Helper Functions
def cluster_countries(data):
    """
    Perform clustering on countries based on COVID-19 trends.
    """
    # Initialize the Clustering class
    clustering = Clustering(data)

    # Select features for clustering
    features = ['people_vaccinated_per_hundred', 'cfr', 'stringency_index', 'trend']
    clustering.preprocess_data(features)

    # Find the optimal number of clusters
    clustering.find_optimal_clusters(max_clusters=10)

    # Perform clustering with the optimal number of clusters
    n_clusters = int(input("Enter the optimal number of clusters: "))
    clustering.perform_clustering(n_clusters=n_clusters)

    # Visualize the clusters
    clustering.visualize_clusters()

    # Return the clustered data
    return clustering.data


# Main Function
def main():
    # Load datasets with only required columns
    required_columns = {
        'cases_deaths': ['country', 'date', 'cfr'],
        'vaccinations': ['country', 'date', 'people_vaccinated_per_hundred'],
        'government_response': ['country', 'date', 'stringency_index'],
        'mobility': ['country', 'date', 'trend']
    }

    cases_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
    vaccinations_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv'
    government_response_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Government_response_policy_cleaned.csv'
    mobility_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\google_mobility_cleaned.csv'

    cases_data = pd.read_csv(cases_path, usecols=required_columns['cases_deaths'])
    vaccinations_data = pd.read_csv(vaccinations_path, usecols=required_columns['vaccinations'])
    government_response_data = pd.read_csv(government_response_path, usecols=required_columns['government_response'])
    mobility_data = pd.read_csv(mobility_path, usecols=required_columns['mobility'])

    # Convert date columns to datetime
    cases_data['date'] = pd.to_datetime(cases_data['date'])
    vaccinations_data['date'] = pd.to_datetime(vaccinations_data['date'])
    government_response_data['date'] = pd.to_datetime(government_response_data['date'])
    mobility_data['date'] = pd.to_datetime(mobility_data['date'])

    # Merge datasets
    merged_data = pd.merge(cases_data, vaccinations_data, on=['country', 'date'], how='inner')
    merged_data = pd.merge(merged_data, government_response_data, on=['country', 'date'], how='inner')
    merged_data = pd.merge(merged_data, mobility_data, on=['country', 'date'], how='inner')

    # Aggregate data by country (e.g., mean values)
    aggregated_data = merged_data.groupby('country').mean().reset_index()

    # Perform clustering
    clustered_data = cluster_countries(aggregated_data)

    # Display the clustered data
    print(clustered_data[['country', 'cluster']])


if __name__ == "__main__":
    main()
