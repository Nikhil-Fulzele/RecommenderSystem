# Code to work with Recommender System
# MovieLens Data set is used

# Import Recommender Class
import Recommender as Rec

# Initialise the Recommendation System
# Recommender function takes four argument:
# 1.Rmin -> minimum rating in a rating scale
# 2.Rmax -> maximum rating in a rating scale
# 3.User Dataset
# 4.Item Dataset
R = Rec.Recommender(1,5,'u.data','u.item')

# For UserBased Recommendation System
# UserRecommendation method is implemented
# It takes 2 arguments:
# 1. UserID
# 2. Method for Similarity measures
# Six different similarity measures are implemented:
# 1.Proximity-Impact-Popularity (PIP) measure, as proposed by Hyung Jun Ahn in 
# "A new similarity measure for collaborative filtering to alleviate the new user cold-starting problem"
# 2.Euclidean distance
# 3.Pearson’s Correlation (COR)
# 4.Cosine (Cos)
# 5.Constrained Pearson’s Correlation(CPC)
# 6.Spearman’s Rank Correlation (SRC)
print 'UserBased Recommendation: \n'
print 'PIP :: ', R.UserRecommendation('87',R.PIP)[0:10],'\n'
print 'Eucli :: ', R.UserRecommendation('87',R.Eucli)[0:10],'\n'
print 'COR :: ', R.UserRecommendation('87',R.COR)[0:10],'\n'
print 'Cos :: ', R.UserRecommendation('87',R.Cos)[0:10],'\n'
print 'CPC :: ', R.UserRecommendation('87',R.CPC)[0:10],'\n'
print 'SRC :: ', R.UserRecommendation('87',R.SRC)[0:10],'\n'

# For ItemBased Recommendation System
# ItemRecommendation method is implemented
# It takes 3 arguments:
# 1. UserID
# 2. Method for Similarity measures
# 3. Top n matches required
print 'ItemBased Recommendation: \n'
print R.ItemRecommendation('87',R.Eucli,50)
