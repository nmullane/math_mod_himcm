rm(list=ls())

setwd("~/himcm/DataAnalysis")
library(ggplot2)
source("myfunctions.R")

activities <- read.table("not_at_home_activities.csv", header=T, sep=",")
activities <- activities[,2:8]
summary(activities)


## Determine number of clusters
#wss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
#for (i in 2:15) wss[i] <- sum(kmeans(mydata, 
#    centers=i)$withinss)
#    plot(1:15, wss, type="b", xlab="Number of Clusters",
#      ylab="Within groups sum of squares")





## get cluster means 
#aggregate(mydata,by=list(fit$cluster),FUN=mean)
## append cluster assignment
#mydata <- data.frame(mydata, fit$cluster)


# K-Means Clustering with 5 clusters
fit <- kmeans(activities[c(7, 6)])

# vary parameters for most readable graph
library(cluster) 
clusplot(mydata, fit$cluster, color=TRUE, shade=TRUE, labels=2, lines=0)
    # Centroid Plot against 1st 2 discriminant functions
library(fpc)
plotcluster(activities[c(7,6)], fit$cluster)
