# ## 1. The raw data files and their format

# Check the name of the current folder
current_dir = get_ipython().getoutput('pwd')
print(current_dir)

# List all files in this folder
file_list = get_ipython().getoutput('ls')
print(file_list)

# List all files in the datasets directory
dataset_list = get_ipython().getoutput('ls datasets/')
print(dataset_list)

# View the first 20 lines of datasets/road-accidents.csv
accidents_head = get_ipython().getoutput('head -20 datasets/road-accidents.csv')
accidents_head


# ## 2. Read in and get an overview of the data

# Import the `pandas` module as "pd"
import pandas as pd

# Read in `road-accidents.csv`
car_acc = pd.read_csv('datasets/road-accidents.csv', sep = '|', comment = '#')

# Save the number of rows columns as a tuple
rows_and_cols = car_acc.shape
print('There are {} rows and {} columns.\n'.format(
    rows_and_cols[0], rows_and_cols[1]))

# Generate an overview of the DataFrame
car_acc_information = car_acc.info()
print(car_acc_information)

# Display the last five rows of the DataFrame
car_acc.tail()


# ## 3. Create a textual and a graphical summary of the data

# import seaborn and make plots appear inline
import seaborn as sns
get_ipython().magic('matplotlib inline')

# Compute the summary statistics of all columns in the `car_acc` DataFrame
sum_stat_car = car_acc.describe()
print(sum_stat_car)

# Create a pairwise scatter plot to explore the data
sns.pairplot(car_acc)


# ## 4. Quantify the association of features and accidents

# Compute the correlation coefficent for all column pairs
corr_columns = car_acc.corr()
corr_columns


# ## 5. Fit a multivariate linear regression

# Import the linear model function from sklearn
from sklearn import linear_model

# Create the features and target DataFrames
features = car_acc[['perc_fatl_speed', 'perc_fatl_alcohol', 'perc_fatl_1st_time']]
target = car_acc['drvr_fatl_col_bmiles']

# Create a linear regression object
reg = linear_model.LinearRegression()

# Fit a multivariate linear regression model
reg.fit(features, target)

# Retrieve the regression coefficients
fit_coef = reg.coef_
fit_coef


# ## 6. Perform PCA on standardized data

# Standardize and center the feature columns
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Import the PCA class function from sklearn
from sklearn.decomposition import PCA
pca = PCA()

# Fit the standardized data to the pca
pca.fit(features_scaled)

# Plot the proportion of variance explained on the y-axis of the bar plot
import matplotlib.pyplot as plt
plt.bar(range(1, pca.n_components_ + 1),  pca.explained_variance_ratio_)
plt.xlabel('Principal component #')
plt.ylabel('Proportion of variance explained')
plt.xticks([1, 2, 3])

# Compute the cumulative proportion of variance explained by the first two principal components
two_first_comp_var_exp = pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]
print("The cumulative variance of the first two principal components is {}".format(
    round(two_first_comp_var_exp, 5)))


# ## 7. Visualize the first two principal components

# Transform the scaled features using two principal components
pca = PCA(n_components = 2)
p_comps = pca.fit_transform(features_scaled)

# Extract the first and second component to use for the scatter plot
p_comp1 = p_comps[:, 0]
p_comp2 = p_comps[:, 1]

# Plot the first two principal components in a scatter plot
plt.scatter(p_comp1, p_comp2)


# ## 8. Find clusters of similar states in the data

# Import KMeans from sklearn
from sklearn.cluster import KMeans

# A loop will be used to plot the explanatory power for up to 10 KMeans clusters
ks = range(1, 10)
inertias = []
for k in ks:
    # Initialize the KMeans object using the current number of clusters (k)
    km = KMeans(n_clusters= k, random_state=8)
    # Fit the scaled features to the KMeans object
    km.fit(features_scaled)
    # Append the inertia for `km` to the list of inertias
    inertias.append(km.inertia_)
    
# Plot the results in a line plot
plt.plot(ks, inertias, marker='o')


# ## 9. KMeans to visualize clusters in the PCA scatter plot

# Create a KMeans object with 3 clusters, use random_state=8 
km = KMeans(n_clusters = 3, random_state = 8)

# Fit the data to the `km` object
km.fit(features_scaled)
y_pred = km.predict(features_scaled)

# Create a scatter plot of the first two principal components
# and color it according to the KMeans cluster assignment 
plt.scatter(features_scaled[:, 0], features_scaled[:, 1], c = y_pred)


# ## 10. Visualize the feature differences between the clusters

# Create a new column with the labels from the KMeans clustering
car_acc['cluster'] = km.labels_
#print(car_acc.head())

# Reshape the DataFrame to the long format
melt_car = pd.melt(car_acc, id_vars = 'cluster', value_vars = features, var_name = 'measurement', value_name = 'percent')
#print(melt_car)

# Create a violin plot splitting and coloring the results according to the km-clusters
sns.violinplot(data = melt_car, x = 'percent', y = 'measurement', hue = 'cluster')


# ## 11. Compute the number of accidents within each cluster

# Read in the new dataset
miles_driven = pd.read_csv('datasets/miles-driven.csv', sep='|')
print(miles_driven.head())

# Merge the `car_acc` DataFrame with the `miles_driven` DataFrame
car_acc_miles = car_acc.merge(miles_driven, on = 'state')

# Create a new column for the number of drivers involved in fatal accidents
car_acc_miles['num_drvr_fatl_col'] = car_acc_miles['drvr_fatl_col_bmiles'] * car_acc_miles['million_miles_annually'] / 1000.00

# Create a barplot of the total number of accidents per cluster
sns.barplot(x =car_acc_miles['cluster'], y = car_acc_miles.groupby(by = 'cluster')['num_drvr_fatl_col'].sum(), estimator= sum, ci = None)


# Calculate the number of states in each cluster and their 'num_drvr_fatl_col' mean and sum.
count_mean_sum = car_acc_miles.groupby(by = 'cluster').agg({'state': 'count',  'num_drvr_fatl_col': ['mean', 'sum']})
count_mean_sum


# ## 12. Make a decision when there is no clear right choice

# Which cluster would you choose?
cluster_num = 3

