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

#Analyze structure
summary(not_at_home)
dim(not_at_home)

x11()


#par(mfrow=c(1,2))
dev.new()
hist(activities$Duration)
dev.new()
hist(not_at_home$Duration)


locator(1)
