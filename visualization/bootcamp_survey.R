library(ggplot2)
library(ggthemes)
library(likert)
library(scales)
library(reshape)

### DATA ###
data_file <- "/Users/nbrodnax/Indiana/CEWIT/iu-cewit/working/bootcamp_data.csv"
data <- read.csv(data_file, header=TRUE)

# need to subset data so "did not attend/not applicable" doesn't show up

### ACTIVITY RATING ###
for (col in c(4:13)) {
  data[,col] <- factor(data[,col], levels = c('Very Poor', 'Poor', 'Fair',
                                              'Good', 'Excellent'))
}
activities <- data[, 4:13, drop = FALSE]
activities <- rename(activities, c(
  resume = 'Group Resume',
  colors = 'Colors Assessment',
  dinner = 'Dinner w/ Laurie McRobbie',
  spaghetti = 'Spaghetti Towers',
  overview = 'CEWIT Overview',
  engagement = 'Engagement Drivers',
  plane = 'Plane Wreck Survival',
  student_needs = 'Student Interests/Needs',
  teams = 'Team Breakout Meetings',
  callout = 'WESIT Callout Planning'
  ))
activity_rating <- likert(activities)
title <- 'Leadership Bootcamp Activity Ratings'
activity_plot <- (plot(activity_rating, centered = FALSE) + ggtitle(title))
ggsave(file="activity.pdf")

### FACILITY RATING ###
for (col in c(14:20)) {
  data[,col] <- factor(data[,col], levels = c('Very Poor', 'Poor', 'Fair',
                                              'Good', 'Excellent'))
}
facility <- data[, 14:20, drop = FALSE]
facility <- rename(facility, c(
  location = 'Location Convenience',
  parking = 'Parking Convenience',
  comfort = 'Meeting Room Comfort',
  size = 'Meeting Room Size',
  food_dinner = 'Friday Dinner',
  food_lunch = 'Saturday Lunch',
  food_snack = 'Sunday Snack'
))
facility_rating <- likert(facility)
title <- 'Leadership Bootcamp Facility Ratings'
facility_plot <- (plot(facility_rating, centered = FALSE) + ggtitle(title))
ggsave(file="facility.pdf")

### STATEMENTS ###
for (col in c(21:28)) {
  data[,col] <- factor(data[,col], levels = c('Strongly Disagree', 'Disagree',
                                              'Neutral', 'Agree',
                                              'Strongly Agree'))
}
statements <- data[, 21:28, drop = FALSE]
statements <- rename(statements, c(
  purpose = 'I have a clear understanding of the purpose and goals of CEWIT.',
  my_role = 'I have a clear understanding of my role as a part of the CEWIT 
  leadership.',
  other_role = 'I have a clear understanding of the roles of WESIT executive 
  board members and directors, SIG interns, and CEWIT staff members.',
  needs = 'I have a clear understanding of what students want and need from CEWIT.',
  team = 'I feel more connected to members of my team.',
  leadership = 'I feel more connected to the CEWIT leadership as a whole.',
  effective = 'I am better prepared to work effectively with my team.',
  decision = 'I am better prepared to make decisions as a CEWIT leader.'
))

agreement <- likert(statements[,1:2], grouping = data$affiliation)
title <- 'Understanding'
agreement_plot0 <- (plot(agreement, centered = FALSE) + ggtitle(title))
ggsave(file="agreement0.pdf")

agreement <- likert(statements[,3:4], grouping = data$affiliation)
title <- 'Understanding'
agreement_plot1 <- (plot(agreement, centered = FALSE) + ggtitle(title))
ggsave(file="agreement1.pdf")

agreement <- likert(statements[,5:6], grouping = data$affiliation)
title <- 'Connectedness'
agreement_plot2 <- (plot(agreement, centered = FALSE) + ggtitle(title))
ggsave(file="agreement2.pdf")

agreement <- likert(statements[,7:8], grouping = data$affiliation)
title <- 'Preparation'
agreement_plot3 <- (plot(agreement, centered = FALSE) + ggtitle(title))
ggsave(file="agreement3.pdf")
