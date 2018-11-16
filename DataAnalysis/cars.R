# Robert Gotwals
# November 7, 2018
# cars.R
# this script looks at car data
#
# clean up, set directory, load the library
rm(list=ls())
setwd("~/Desktop/DataScienceSeminar")
library(ggplot2)
source("myfunctions.R")
#
# read and view the data
cars <- read.csv(file="cars.csv", header=T)
#
# look at the data
names(cars)
summary(cars)

#
# more look at the data
specs <- cars[,c(2, 4:8)]
specs
pairs(specs, upper.panel=panel.cor, diag.panel=panel.hist)
#
# create factors with value labels
names(cars)
cars$gear <- factor(cars$gear, levels=c(3,4,5), labels=c("3gears", "4gears", "5gears"))
cars$am <- factor(cars$am, levels=c(0,1), labels=c("Automatic", "Manual"))
cars$cyl <- factor(cars$cyl, levels=c(4,6,8), labels=c("4cyl", "6cyl", "8cyl"))
View(cars)
# Once we have applied labels and made gear, am and cyl into factors, we can use the tapply command to do a count of all of these:
tapply(cars$gear, cars$gear, length)
tapply(cars$am, cars$am, length)
tapply(cars$cyl, cars$cyl, length)
#
# Kernel density plot for mpg
qplot(mpg, data=cars, geom="density", fill=gear, alpha=I(0.5), main="Distribution of Gas mileage", xlab="MPG", ylab="Density")
#
# Scatterplot of mpg vs. hp
qplot(hp, mpg, data=cars, shape=am, color=am, facets=gear~cyl, size=I(3), xlab="Horsepower", ylab="MPG")
#
# regression plot
qplot(wt, mpg, data=cars, geom= c("point"), color=cyl, main="Regression of MPG on wt", xlab="Weight", ylab="MPG")
#
# boxplots
qplot(gear, mpg, data=cars, geom=c("boxplot", "jitter"), fill=gear, main="Mileage by gear number", xlab="", ylab="MPG")
                       
