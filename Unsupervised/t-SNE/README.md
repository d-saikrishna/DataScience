# t-SNE

**Stochastic Neighbour Embedding**

t-SNE helps in dimensionality reduction. You will be able to visualise 4+ dimensions (variables) in the form of a 2/3-Dimensions without losing much information/variance.

PCA and MDS are other methods of this category.

PCA is a Linear Approach.

## t-SNE steps
1. Determine similarity scores between all points (distances)
2. Plot the distances on a normal curve - get scaled similarity scores
3. Matrix of similarity scores
4. t-Distribution

## tSNE vs PCA

Both are trying to compress the high-dimensional information into 2-3 Dimensions. But:

1. t-SNE is trying to preserve the relationship (similarity) between original datapoints in the new data of 2/3 dimensions (pairwise). PCA works at a more global level (total variance of the entire dataset is preserved)
2. PCA is just a bunch of linear transformations on the data. tSNE works pairwise - non-linear.


## References
1. [StatQuest](https://www.youtube.com/watch?v=NEaUSP4YerM)
2. [Tubingen ML Lecture](https://www.youtube.com/watch?v=MnRskV3NY1k)