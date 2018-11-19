rm(list=ls())

setwd("~/himcm/DataAnalysis")
library(ggplot2)
library(fpc)
library(factoextra)
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
set.seed(320)
df <- activities[,c(6,5)]
summary(df)
clusters <- kmeans(df, 13)
db <- fpc::dbscan(df[50000:75000,], eps=2.31, MinPts=10)

str(clusters)

X11()
clusters$cluster<- as.factor(clusters$cluster)
ggplot(activities, aes(start_time, Duration, color = clusters$cluster)) + geom_point()
X11()
plot(db, df[50000:75000,], main = "DBSCAN", frame = FALSE)
X11()
fviz_cluster(db, df[50000:75000,], stand = FALSE, frame = FALSE, geom = "point", ellipse = FALSE)
X11()
dbscan::kNNdistplot(df, k =  5)
abline(h = 1.15, lty = 2)


print(db)
summary(db)
names(db)
write.csv(db$cluster, "clusters.csv")
write.csv(df, "data_frame.csv")

#par(mfrow=c(1,90))
#dev.new()
##qplot(activities[50000:75000,6], activities[50000:75000,5], xlab="Start time (min)", ylab="Outing Duration")
#ggplot(activities, aes(start_time, Duration)) + geom_point()
#
#
## vary parameters for most readable graph
#library(cluster) 
#clusplot(activities[50000:75000,6:5], fit$cluster, color=TRUE, shade=TRUE, labels=0, lines=0)
#    # Centroid Plot against 1st 2 discriminant functions
#library(fpc)
#plotcluster(activities[50000:75000,5:6], fit$cluster)
#message("Press Return To Continue")
#invisible(readLines("stdin", n=1))
while (!is.null(dev.list())) Sys.sleep(1)

