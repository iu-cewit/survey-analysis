library(ggplot2)
library(ggthemes)
library(likert)
library(scales)
library(reshape)
library(extrafont)
loadfonts()

## DATA ##
data_file <- "/Users/nbrodnax/Indiana/CEWIT/evaluation/surveys/phd_website_workshop_15/data/website_workshop_data.csv"
data <- read.csv(data_file, header=TRUE)

# convert missing to unknown values
data[data == '[]'] <- NA

# format variables to appropriate type
# 1) affiliation
for (col in c(2,15)) {
  data[,col] <- factor(data[,col], levels = c('PhD Student',
                                              'Other (please specify)'))
}
# 2) Gender
for (col in c(14,25)) {
  data[,col] <- factor(data[,col], levels = c('Female', 'Male'))
}
# 3) Marketing: Not sure what to do because some responses are lists
# 4) Statement Agreement
for (col in c(4:7,17:19)) {
  data[,col] <- factor(data[,col], levels = c('Strongly Disagree', 'Disagree',
                                              'Neutral', 'Agree',
                                              'Strongly Agree'))
}
# 5) Workshop Ratings
for (col in c(8:13,20:24,27:28)) {
  data[,col] <- factor(data[,col], levels = c('Very Poor', 'Poor', 'Fair',
                                              'Good', 'Excellent'))
}
# 6) Built Site
data[,26] <- factor(data[,26], levels = c('Yes', 'No'))

## PART 1 ##

## Affiliation ##
table(data$p1_affiliation)

## Gender ##
table(data$p1_gender)

## Marketing Penetration ##

## Statement Agreement ##
statements <- data[, 4:7, drop = FALSE]
statements <- rename(statements, c(
  p1_useful = 'I found the material presented to be useful for designing an 
  academic website.', p1_new_material = 'This workshop covered material that 
  I did not already know.', p1_enough_info = 'I have enough information to 
  design a professional academic website.', p1_plan_to_build = 'I plan to 
  attend Part II to build my academic website.'))

agreement1 <- likert(statements)
title <- 'Part I Statement Agreement'
agreement_plot1 <- (plot(agreement1))
pdf("agreement1.pdf", family="CM Roman")
agreement_plot1
dev.off()

## Workshop Ratings ##


## PART 2 ##

