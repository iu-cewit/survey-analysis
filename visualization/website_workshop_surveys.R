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
data_file <- "/Users/nbrodnax/Indiana/CEWIT/evaluation/surveys/phd_website_workshop_15/data/marketing_data.csv"
promo <- read.csv(data_file, header=TRUE)

# convert missing to unknown values
data[data == '[]'] <- NA
data[data == "I Don't Know"] <- NA
promo[promo == '[]'] <- NA

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
  print(table(data[,col]))
  data[,col] <- factor(data[,col], levels = c('Very Poor', 'Poor', 'Neutral',
                                              'Good', 'Excellent'))
}
# 6) Built Site
data[,26] <- factor(data[,26], levels = c('Yes', 'No'))

## PART 1 ##

## Affiliation ##
table(data$p1_affiliation)
p1_affil <- (ggplot(data=data[which(!is.na(data$p1_affiliation)),], 
                    aes(x=p1_affiliation))
             + layer(geom = 'bar', stat = 'bin')
             + xlab('Affiliation')
             + ylab('Count')
             + ggtitle('Part I Attendee Affiliation'))
p1_affil

## Gender ##
table(data$p1_gender)
p1_sex <- (ggplot(data=data[which(!is.na(data$p1_gender)),], 
                    aes(x=p1_gender))
             + layer(geom = 'bar', stat = 'bin')
             + xlab('Gender')
             + ylab('Count')
             + ggtitle('Part I Attendee Gender'))
p1_sex

## Marketing Penetration ##
p1_market <- (ggplot(data=promo[which(!is.na(promo$p1_promotion)),], 
                  aes(x=p1_promotion))
           + layer(geom = 'bar', stat = 'bin')
           + xlab('Promotion Type')
           + ylab('Count')
           + coord_flip()
           + ggtitle('Part I Marketing Penetration'))
p1_market


## Statement Agreement ##
statements <- data[, 4:7, drop = FALSE]
statements <- rename(statements, c(
  p1_useful = 'I found the material presented to be useful for designing an 
  academic website.',
  p1_new_material = 'This workshop covered material that I did not already 
  know.',
  p1_enough_info = 'I have enough information to design a professional 
  academic website.',
  p1_plan_to_build = 'I plan to attend Part II to build my academic website.'
))
agreement1 <- likert(statements)
p1_agreement <- (plot(agreement1, wrap=20, ordered=FALSE, 
                      group.order=names(statements), text.size=2) 
                 + ggtitle('Please choose the extent to which you agree 
with the following statements.') 
                 + theme(title = element_text(size=11))
                 + theme(axis.text = element_text(size=9),
                         axis.text.y= element_text(hjust=1, angle=0))
                 + theme(legend.position="top")
                 + theme(legend.text = element_text(size=9),
                         legend.title = element_text(size=9)))
ggsave(file="p1_agreement.pdf")

## Workshop Ratings ##
ratings <- data[, 8:13, drop = FALSE]
ratings <- rename(ratings, c(
  p1_room = 'Comfort level of meeting room',
  p1_location = 'Convenience of location',
  p1_computers = 'Computer access',
  p1_photographer = 'Headshot access',
  p1_video = 'Video quality',
  p1_audio = 'Audio quality'
))
rating1 <- likert(ratings)
p1_rating <- (plot(rating1, wrap=20, ordered=FALSE, group.order=names(ratings),
                   text.size=2)
              + ggtitle('Please provide a rating for each feature of the workshop.') 
              + theme(title = element_text(size=11))
              + theme(axis.text = element_text(size=9),
                      axis.text.y= element_text(hjust=1, angle=0))
              + theme(legend.position="top")
              + theme(legend.text = element_text(size=9),
                      legend.title = element_text(size=9)))
ggsave(file="p1_rating.pdf")


## PART 2 ##

## Affiliation ##
table(data$p2_affiliation)
p2_affil <- (ggplot(data=data[which(!is.na(data$p2_affiliation)),], 
                    aes(x=p2_affiliation))
             + layer(geom = 'bar', stat = 'bin')
             + xlab('Affiliation')
             + ylab('Count')
             + ggtitle('Part II Attendee Affiliation'))
p2_affil


## Gender ##
table(data$p2_gender)
p2_sex <- (ggplot(data=data[which(!is.na(data$p2_gender)),], 
                  aes(x=p2_gender))
           + layer(geom = 'bar', stat = 'bin')
           + xlab('Gender')
           + ylab('Count')
           + ggtitle('Part II Attendee Gender'))
p2_sex

## Marketing Penetration ##
p2_market <- (ggplot(data=promo[which(!is.na(promo$p2_promotion)),], 
                     aes(x=p2_promotion))
              + layer(geom = 'bar', stat = 'bin')
              + xlab('Promotion Type')
              + ylab('Count')
              + coord_flip()
              + ggtitle('Part II Marketing Penetration'))
p2_market

## Statement Agreement ##
statements <- data[, 17:19, drop = FALSE]
statements <- rename(statements, c(
  p2_useful = 'I found the material presented to be useful for designing an 
  academic website.',
  p2_new_material = 'This workshop covered material that I did not already 
  know.',
  p2_enough_info = 'I have enough information to design a professional 
  academic website.'
))
agreement2 <- likert(statements)
p2_agreement <- (plot(agreement2, wrap=20, ordered=FALSE, 
                      group.order=names(statements), text.size=2) 
                 + ggtitle('Please choose the extent to which you agree 
with the following statements.') 
                 + theme(title = element_text(size=11))
                 + theme(axis.text = element_text(size=9),
                         axis.text.y= element_text(hjust=1, angle=0))
                 + theme(legend.position="top")
                 + theme(legend.text = element_text(size=9),
                         legend.title = element_text(size=9)))
ggsave(file="p2_agreement.pdf")

## Workshop Ratings ##
ratings <- data[, c(20:24,27:28), drop = FALSE]
ratings <- rename(ratings, c(
  p2_room = 'Comfort level of meeting room',
  p2_location = 'Convenience of location',
  p2_computers = 'Computer access',
  p2_platform_usable = 'Usability of Weebly platform',
  p2_platform_flexible = 'Flexibility of Weebly platform',
  p2_video = 'Video quality',
  p2_audio = 'Audio quality'
))
rating2 <- likert(ratings)
p2_rating <- (plot(rating2, wrap=20, ordered=FALSE, group.order=names(ratings),
                   text.size=2)
              + ggtitle('Please provide a rating for each feature of the workshop.') 
              + theme(title = element_text(size=11))
              + theme(axis.text = element_text(size=9),
                      axis.text.y= element_text(hjust=1, angle=0))
              + theme(legend.position="top")
              + theme(legend.text = element_text(size=9),
                      legend.title = element_text(size=9)))
ggsave(file="p2_rating.pdf")

