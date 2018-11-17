rm(list=ls())

setwd("~/himcm/DataAnalysis")
library(ggplot2)
source("myfunctions.R")

#Load activities data
activities <- read.table("atus_00001.dat", header=T, sep = " ")

#Analyze Structure
#names(activities)
#summary(activities)
#dim(activities)

#Remove activities at home
not_at_home <- activities[activities$Location != 101,]
#Analyze structure

"Structure of not at home"
summary(not_at_home)
dim(not_at_home)

#Analyze start times
start_times <- as.character(not_at_home$Start_time)
end_times <- as.character(not_at_home$end_time)
#Analyze structure
"Start Times Character Array"
summary(start_times)

#Convert to numeric data
start_times <- sapply(strsplit(start_times,":"),
    function(x) {
        x <- as.numeric(x)
        x[1]+x[2]/60+x[3]/3600
    }
)
end_times <- sapply(strsplit(end_times,":"),
    function(x) {
        x <- as.numeric(x)
        x[1]+x[2]/60+x[3]/3600
    }
)
#Analyze vals
"Start Times Numeric times"
summary(start_times)

"End Times Numeric times"
summary(end_times)

colnames(not_at_home)[colnames(not_at_home)=="Start_time"] <- "start_time"

not_at_home$start_time <- start_times
not_at_home$end_time <- end_times
write.csv(not_at_home, "not_at_home_activities.csv")

"Not at home summary"
summary(not_at_home)
not_at_home
#GUI Things
x11()


#par(mfrow=c(1,2))

#Graph histograms of activity duration
par(mfrow=c(1,90))
dev.new()
hist(activities$Duration)
hist(not_at_home$Duration)
hist(start_times)
#plot(start_times, not_at_home$Duration)
qplot(not_at_home$start_time[1:10000], not_at_home$Duration[1:10000], xlab="Start time (min)", ylab="Outing Duration")
qplot(not_at_home$start_time[10000:20000], not_at_home$Duration[10000:20000], xlab="Start time (min)", ylab="Outing Duration")
qplot(not_at_home$start_time[15543:25543], not_at_home$Duration[10000:20000], xlab="Start time (min)", ylab="Outing Duration")
not_at_home$Duration[1:100]
not_at_home <- not_at_home[sample(nrow(not_at_home)),]
not_at_home$Duration[1:100]
qplot(not_at_home$start_time[1:10000], not_at_home$Duration[1:10000], xlab="Start time (min)", ylab="Outing Duration")
qplot(not_at_home$start_time[10000:20000], not_at_home$Duration[10000:20000], xlab="Start time (min)", ylab="Outing Duration")
qplot(not_at_home$start_time[15543:25543], not_at_home$Duration[10000:20000], xlab="Start time (min)", ylab="Outing Duration")

#ggplot(activities, aes(x=activities$Duration)) + geom_histogram()
#ggplot(not_at_home, aes(x=not_at_home$Duration)) + geom_histogram()
#ggplot(not_at_home, aes(x=start_times, y=not_at_home$Duration)) + geom_histogram(stat="identity")


#ggplot2.histogram(data=activities$Duration, xName="Activity Duration")
#ggplot2.histogram(data=not_at_home$Duration, xName="Outing Duration")
#ggplot2.histogram(data=start_times,weight=not_at_home$duration, xName="Time of Day", yName="Outing Duration")

locator(1)
