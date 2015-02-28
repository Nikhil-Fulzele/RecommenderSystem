#
# Movie Recommender System
#

from math import sqrt
import collections

class Recommender:

    # Initialize the Recommender System
    def __init__(self,Rmin,Rmax,user_dataset,item_dataset):
        self.Rmin = Rmin
        self.Rmax = Rmax
        self.Rmid = (self.Rmin + self.Rmax)/2.0
        
        # Movie id with title
        self.movies = {}
        for line in open(item_dataset):
            (id,title) = line.split('|')[0:2]
            self.movies[id]=title

        # Load users data
        self.userData ={}
        for line in open(user_dataset):
            (user,movieid,rating,ts)=line.split('\t')
            self.userData.setdefault(user,{})
            self.userData[user][self.movies[movieid]]=float(rating)        

        # Creating User list
        self.UsersList = [i for i in self.userData]
    
    # Method for finding Agreement
    def Agreement(self,r1,r2):
        self.r1 = r1
        self.r2 = r2
        if (self.r1 > self.Rmid and self.r2 < self.Rmid) or (self.r1 < self.Rmid and self.r2 > self.Rmid):
            return False
        return True

    # Method for calculating Proximity
    def Proximity(self,r1,r2):
        if self.Agreement(r1,r2):
            self.absDist = abs(r1-r2)
        self.absDist = 2*abs(r1-r2)
        return ((2*(self.Rmax-self.Rmin)+1)-self.absDist)**2

    # Method for calculating Impact
    def Impact(self,r1,r2):
        return (((abs(r1-self.Rmid)+1)*(abs(r2-self.Rmid)+1)) if self.Agreement(r1,r2) else (1.0/((abs(r1-self.Rmid)+1)*(abs(r2-self.Rmid)+1))))

    # Method for calculating Popularity
    def Popularity(self,r1,r2,item):
        itemRating = []
        for itm in self.itemData[item]:
            itemRating.append(self.itemData[item][itm])
                
        self.avg = self.mean(itemRating)
        return ((1 + (((r1+r2)/2.0 - self.avg)**2)) if (r1 > self.avg and r2 > self.avg) or (r1 < self.avg and r2 < self.avg) else 1)

    #
    # Similarity measures
    #

    # Proximity-Impact-Popularity (PIP) measure
    def PIP(self,user1,user2,choice):
        self.createItemData()
        if choice:
            data = self.userData
        else:
            data = self.itemData
        # Get the list of the shared_items
        commonItem = {}
        for item in data[user1]:
            if item in data[user2]:
                commonItem[item] = 1
                     
        # if no common items
        if len(commonItem)==0: return 0

        # PIP calculation        
        result = 0
        for item in data[user1]:
            if item in data[user2]:
                r1 = data[user1][item]
                r2 = data[user2][item]
                result += self.Proximity(r1,r2)*self.Impact(r1,r2)*self.Popularity(r1,r2,item)

        return result
                
    # Euclidean distance (Eucli)
    def Eucli(self,user1,user2,choice):
        if choice:
            data = self.userData
        else:
            data = self.itemData
        # Get the list of the shared_items
        commonItem = {}
        for item in data[user1]:
            if item in data[user2]:
                commonItem[item] = 1
                     
        # if no common items
        if len(commonItem)==0: return 0

        # Euclidean distance calculation
        sum_of_squares=sum([pow(data[user1][item]-data[user2][item],2) for item in data[user1] if item in data[user2]])

        return 1/(1+sum_of_squares)


    # Pearson’s Correlation (COR)
    def COR(self,user1,user2,choice):
        if choice:
            data = self.userData
        else:
            data = self.itemData
        
        # Get the list of the shared_items
        commonItem = {}
        for item in self.userData[user1]:
            if item in self.userData[user2]: commonItem[item]=1

        # Find the number of elements
        n = len(commonItem)

        # If no common items
        if n==0: return 0

        # Sum all the common data rating of both the users
        s1 = sum([self.userData[user1][it] for it in commonItem])
        s2 = sum([self.userData[user2][it] for it in commonItem])

        # Sum and square all the common data rating of both the users
        s1Sq = sum([pow(self.userData[user1][it],2) for it in commonItem])
        s2Sq = sum([pow(self.userData[user2][it],2) for it in commonItem])

        # Sum of their the products
        pSum = sum([self.userData[user1][it]*self.userData[user2][it] for it in commonItem])

        # Pearson score calculation
        neu = pSum-(s1*s2/n)
        deno = sqrt((s1Sq-(s1**2)/n)*(s2Sq-(s2**2)/n))
        if deno==0: return 0

        return neu/deno
        

    # Cosine (COS)
    def Cos(self,user1,user2,choice):
        if choice:
            data = self.userData
        else:
            data = self.itemData
        
        # Get the list of the shared_items
        commonItem = {}
        for item in self.userData[user1]:
            if item in self.userData[user2]: commonItem[item]=1

        # Find the number of elements
        n = len(commonItem)

        # If no common items
        if n==0: return 0

        # Sum and square all the common data rating of both the users
        s1Sq = sum([pow(self.userData[user1][it],2) for it in commonItem])
        s2Sq = sum([pow(self.userData[user2][it],2) for it in commonItem])

        # Sum of their the products
        neu = sum([self.userData[user1][it]*self.userData[user2][it] for it in commonItem])

        # Constrained Pearson score calculation
        deno = sqrt(s1Sq*s2Sq)
        if deno==0: return 0

        return neu/deno


    # Constrained Pearson’s Correlation(CPC)
    def CPC(self,user1,user2,choice):
        if choice:
            data = self.userData
        else:
            data = self.itemData
            
        # Get the list of the shared_items
        commonItem = {}
        for item in self.userData[user1]:
            if item in self.userData[user2]: commonItem[item]=1

        # Find the number of elements
        n = len(commonItem)

        # If no common items
        if n==0: return 0

        # Sum all the common data rating of both the users
        s1 = sum([self.userData[user1][it]-self.Rmid for it in commonItem])
        s2 = sum([self.userData[user2][it]-self.Rmid for it in commonItem])

        # Sum and square all the common data rating of both the users
        s1Sq = sum([pow(self.userData[user1][it]-self.Rmid,2) for it in commonItem])
        s2Sq = sum([pow(self.userData[user2][it]-self.Rmid,2) for it in commonItem])

        # Sum of their the products
        pSum = sum([self.userData[user1][it]*self.userData[user2][it] for it in commonItem])

        # Constrained Pearson score calculation
        neu = s1*s2
        deno = sqrt(s1Sq*s2Sq)
        if deno==0: return 0

        return neu/deno

    # Spearman’s Rank Correlation (SRC)
    def SRC(self,user1,user2,choice):

        if choice:
            data = self.userData
        else:
            data = self.itemData
            
        # Get the list of the shared_items
        commonItem = {}
        for item in self.userData[user1]:
            if item in self.userData[user2]: commonItem[item]=1

        # Find the number of elements
        n = len(commonItem)

        # If no common items
        if n==0: return 0

        # Spearman's Rank calculation
        neu = 6*sum([abs(self.userData[user1][it]-self.userData[user2][it]) for it in commonItem])
        deno = n*(pow(n,2)-1)
        if deno==0: return 0
        return 1 - neu/deno

        
    # Mean calculation -- utility function
    def mean(self,listinput):
        total = 0.0
        for entry in listinput:
            total += entry
        return total/len(listinput)

                    
    # Method for getting recommendation
    def UserRecommendation(self,user,distanceType):
        tot = collections.defaultdict(float)
        sums = collections.defaultdict(float)

        for other in self.userData:

            # Don't compare me to myself
            if other == user: continue
            simi = distanceType(user,other,True)

            # Ignore scores of zero or lower
            if simi <= 0: continue
            for item in self.userData[other]:

                # Only scores movies I haven't seen yet
                if item not in self.userData[user] or self.userData[user][item]==0:
                    # Similarity * Score
                    tot[item]+=self.userData[other][item]*simi
                    # Sum of similarities
                    sums[item]+=simi

        # Create the normalized list
        rankings = [(total/sums[item],item) for (item, total) in tot.items()]

        # Return the sorted list
        rankings.sort()
        rankings.reverse()
        return rankings

    # Method for item recommendation
    def ItemRecommendation(self,user,distType,n=10):
        item = {}
        userRatings = self.userData[user]
        scrs = {}
        tot = {}        

        # Create Item Dictionary
        self.createItemData()
        for itm in self.itemData:
            # Find the most similar items to this one
            scores = [(distType(itm,other,False),other) for other in self.itemData if other != itm]
            scores.sort()
            scores.reverse()
            item[itm]=scores[0:n]

        # Item rated by user
        for (itm,rating) in userRatings.items():

            # Loop over similar items for user
            for (similar,itm2) in item[itm]:

                # If item alrady rated
                if itm2 in userRatings: continue

                # Weight sum of rating items similarity
                scrs.setdefault(itm2,0)
                scrs[itm2]+=similar*rating

                # Sum of all the similarities
                tot.setdefault(itm2,0)
                tot[itm2]+=similar

        # Divide each total score by total weighting to get an average
        rankings=[(score/tot[itm],itm) for itm, score in scrs.items()]

        # Return the lowest rankings from higest to lowest
        rankings.sort(reverse=True)
        return rankings

    # Finding similar items based on given item
    def createItemData(self):
        result = collections.defaultdict(dict)
        for person in self.userData:
            for item in self.userData[person]:
                # Flip item and person
                result[item][person] = self.userData[person][item]
        self.itemData = result
