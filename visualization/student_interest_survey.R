library(ggplot2)
library(ggthemes)
library(likert)
library(scales)

### DATA ###
data = read.csv("/Users/nbrodnax/Indiana/CEWIT/iu-cewit/working/data.csv", 
                header=FALSE)

#convert missing to unknown values
data[data == '[]'] <- NA

# update variable names
colnames(data) = c('id', 'first_name', 'last_name', 'email', 'mailing', 
                   'level', 'field', 'school', 'category', 'it_career', 
                   'major1', 'minor1', 'data_analysis', 'blogging', 
                   'programming', 'graphics', 'humanities', 'social_justice', 
                   'social_good', 'social_media', 'game_dev', 'gaming', 
                   'interaction', 'mobile_app', 'web_dev', 'phys_computing', 
                   'project_mgmt', 'research', 'security', 'education', 
                   'higher_ed', 'mentor')

# convert variables to correct type
for (col in c(1:4,7,11:12)) {
  data[,col] <- as.character(data[,col])
  }
for (col in c(8:9)) {
  data[,col] <- factor(data[,col])
}
data$mailing <- factor(data$mailing, levels = c('Yes', 'No', 'No Answer'))
# data$level <- factor(data$level, levels = c('Freshman', 'Sophomore', 'Junior',
#                                             'Senior', 'Master', 'PhD', 'JD',
#                                             'Other'))
data$level <- factor(data$level, levels = c('Other', 'JD', 'PhD', 'Master',
                                            'Senior', 'Junior', 'Sophomore',
                                            'Freshman'))
data$mentor <- factor(data$mentor, levels = c('peer', 'faculty', 'staff',
                                              'serve'))
data$it_career <- factor(data$it_career, levels = c('Strongly Agree',
                                                    'Agree', 'Disgree', 
                                                    'Strongly Disagree',
                                                    "Unsure/Don't Know"))

# add a column to use in plots
data$count <- 1

### INTEREST IN JOINING CEWIT ###

# raw count by level
p1 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$level)),], 
              aes(level, fill=mailing))
       + ylab('Number of Students')
       + xlab('Enrollment Level')
       + ggtitle('Mailing List Opt-Ins by Enrollment Level')
       + geom_bar()
       + theme_solarized()
       + scale_color_solarized()
       + coord_flip()
       + scale_fill_discrete(name='Opt-In to\nMailing List?'))
ggsave(file="mailing_by_level.pdf")

# share by level
p2 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$level)),],
              aes(x = level, fill = mailing))
       + ylab('Percent of Respondents')
       + xlab('Enrollment Level')
       + ggtitle('Mailing List Opt-Ins by Enrollment Level')
       + geom_bar(aes(y = (..count..)/sum(..count..))) 
       + theme_solarized()
       + scale_color_solarized()
       + coord_flip()
       + scale_fill_discrete(name='Opt-In to\nMailingList?')
       + scale_y_continuous(labels=percent))
ggsave(file="mailing_by_level_pct.pdf")

# raw count by school
p3 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$school)),], 
              aes(x = reorder(school, table(school)[school]), fill = mailing))
       + ylab('Number of Students')
       + xlab('Enrollment Level')
       + ggtitle('Mailing List Opt-Ins by School')
       + geom_bar()
       + theme_solarized()
       + scale_color_solarized()
       + coord_flip()
       + scale_fill_discrete(name='Opt-In to\nMailing List?'))
ggsave(file="mailing_by_school.pdf")

# another way to do p3
data$school <- factor(data$school, levels = names(sort(table(data$school))))
p3.1 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$school)),], 
                aes(x = school, fill = mailing))
         + ylab('Number of Students')
         + xlab('Enrollment Level')
         + ggtitle('Mailing List Opt-Ins by School')
         + geom_bar()
         + theme_solarized()
         + scale_color_solarized()
         + coord_flip()
         + scale_fill_discrete(name='Opt-In to\nMailing List?'))

# share by school
p4 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$school)),], 
              aes(x = school, fill = mailing))
       + ylab('Proportion of Respondents')
       + xlab('Enrollment Level')
       + ggtitle('Mailing List Opt-Ins by School')
       + geom_bar(position="fill")
       + theme_solarized()
       + scale_color_solarized()
       + coord_flip()
       + scale_fill_discrete(name='Opt-In to\nMailing List?'))

# need yes-only by school with fill by grad/undergrad
yes_mailing <- data[data$mailing == 'Yes',]
yes_count <- nrow(yes_mailing)
sorted_levels = names(sort(table(yes_mailing$school)))
data$school <- factor(data$school, levels = sorted_levels)
p4 <- (ggplot(yes_mailing[!is.na(yes_mailing$school),], aes(school, fill=level))
       + geom_bar()
       + theme_solarized()
       + coord_flip())

# by category
p5 <- (ggplot(data[!is.na(data$category),], aes(category, fill=mailing)) 
          + geom_bar()
          + theme_solarized()
          + scale_color_solarized()
          + coord_flip())


### INTEREST IN TECH CAREER ###


### INTEREST IN MENTORING ###


### INTEREST IN SPECIFIC TECHNOLOGY ###

