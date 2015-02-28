# Recommender System using Collaborative Filtering

Language used : Python 2.7

Dataset used  : MovieLens 100k, available at http://grouplens.org/datasets/movielens/

Features Implemented  :
  1. User Based Recommendation
  2. Item Based Recommendation

How to use it:

Step 1: Import Recommender Class

Step 2: Initialise the Recommendation System
        
        Recommender function requires four arguments:
          
          1.Rmin -> minimum rating in a rating scale
          
          2.Rmax -> maximum rating in a rating scale 
          
          3.User Dataset
          
          4.Item Dataset 
          
Step 3a: For UserBased Recommendation System, UserRecommendation method is implemented
            
            It requires 2 arguments:
              
              1. UserID
              
              2. Method for Similarity measures
        
        Six different similarity measures are implemented:
          
          1.Proximity-Impact-Popularity (PIP) measure, as proposed by Hyung Jun Ahn in "A new similarity measure for              collaborative filtering to alleviate the new user cold-starting problem", available at 
            http://www.sciencedirect.com/science/article/pii/S0020025507003751
          
          2.Euclidean distance
          
          3.Pearson’s Correlation (COR)
          
          4.Cosine (Cos)
          
          5.Constrained Pearson’s Correlation(CPC)
          
          6.Spearman’s Rank Correlation (SRC)
          
Step 3b:  For ItemBased Recommendation System, ItemRecommendation method is implemented
            
            It takes 3 arguments:
              
              1. UserID
              
              2. Method for Similarity measures
              
              3. Top n matches required
