rm(list=ls())

setwd("~/himcm")
library(ggplot2)

#Load activities data
activities <- read.table("atus_00001.dat", header=T, sep = " ")

#Analyze Structure
#names(activities)
#summary(activities)
#dim(activities)

#Take activities at home
not_at_home <- activities[activities$Location != 101,]
start_times <- not_at_home$Start_time
summary(start_times)
substringed_data <- sapply(start_times, substring, 1, 2)
substringed_data


#Analyze structure
summary(not_at_home)
dim(not_at_home)


#GUI Things
x11()


#par(mfrow=c(1,2))

#Graph histograms of activity duration
dev.new()
hist(activities$Duration)
dev.new()
hist(not_at_home$Duration)

dev.new()
hist(not_at_home$Start_time, freq = FALSE, density=not_at_home$duration)

locator(1)
