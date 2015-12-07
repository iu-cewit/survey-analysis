library(ggplot2)
library(ggthemes)
library(likert)
library(scales)
library(reshape)

### DATA ###
data = read.csv("/Users/nbrodnax/Indiana/CEWIT/evaluation/surveys/student_interest_14/data/data.csv", 
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
data$mailing <- factor(data$mailing, levels = c('Yes', 'No'))
# data$level <- factor(data$level, levels = c('Freshman', 'Sophomore', 'Junior',
#                                             'Senior', 'Master', 'PhD', 'JD',
#                                             'Other'))
data$level <- factor(data$level, levels = c('Other', 'JD', 'PhD', 'Master',
                                            'Senior', 'Junior', 'Sophomore',
                                            'Freshman'))
# data$mentor <- factor(data$mentor, levels = c('peer', 'faculty', 'staff',
#                                               'serve'))
data$it_career <- factor(data$it_career, levels = c("Strongly Agree",
                                                    "Agree", 
                                                    "Unsure/Don't Know",
                                                    "Disagree", 
                                                    "Strongly Disagree"))
for (col in c(13:31)) {
  data[,col] <- factor(data[,col], levels = c('Completely Uninterested',
                                              'Uninterested', 'Interested',
                                              'Very Interested'))
}

### INTEREST IN JOINING CEWIT ###

# raw count by level (all respondents)
p1 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$level)),], 
              aes(level, fill=mailing))
       + ylab('Number of Students')
       + xlab('Enrollment Level')
       + ggtitle('Affiliation with CEWIT by Level')
       + geom_bar()
       + theme_fivethirtyeight()
       + coord_flip()
       + scale_fill_discrete(name='Opt-In to\nMailing List?')
       + theme(title = element_text(size=24))
       + theme(axis.text = element_text(size=12),
               axis.text.y= element_text(hjust=1, angle=0))
       + theme(legend.position="bottom")
       + theme(legend.text = element_text(size=11), 
               legend.title = element_text(size=11)))
ggsave(file="mailing_by_level.pdf")

# share by level (all respondents)
p2 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$level)),],
              aes(x = level, fill = mailing))
       + ylab('Percent of Respondents')
       + xlab('Enrollment Level')
       + ggtitle('Mailing List Opt-Ins by Enrollment Level')
       + geom_bar(aes(y = (..count..)/sum(..count..))) 
       + theme_fivethirtyeight()
       + coord_flip()
       + scale_fill_discrete(name='Opt-In to\nMailingList?')
       + scale_y_continuous(labels=percent))
ggsave(file="mailing_by_level_pct.jpeg")

# raw count by school (all respondents)
data$school <- factor(data$school, levels = names(sort(table(data$school))))
p3 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$school)),], 
                aes(x = school, fill = mailing))
         + ylab('Number of Students')
         + xlab('Enrollment Level')
         + ggtitle('Affiliation with CEWIT')
         + geom_bar()
         + theme_fivethirtyeight()
         + coord_flip()
         + theme(title = element_text(size=24))
         + theme(axis.text = element_text(size=12),
               axis.text.y= element_text(hjust=1, angle=0))
         + theme(legend.position="bottom")
         + theme(legend.text = element_text(size=11), 
               legend.title = element_text(size=11))
         + scale_fill_discrete(name='Response'))
ggsave(file="mailing_by_school.pdf")

# proportion of school opting in
# may try this with the likert graph approach
p4 <- (ggplot(data[which(!is.na(data$mailing) & !is.na(data$school)),], 
              aes(x = school, fill = mailing))
       + ylab('Proportion of Respondents')
       + xlab('Enrollment Level')
       + ggtitle('Mailing List Opt-Ins by School')
       + geom_bar(position="fill")
       + theme_fivethirtyeight()
       + coord_flip()
       + scale_fill_discrete(name='Opt-In to\nMailing List?'))
ggsave(file="mailing_by_school_pct.pdf")

# likert approach
# need to figure out how to group by school or level
data$mailing <- factor(data$mailing, levels = c('No', 'Yes'))
mailing_school <- data[which(!is.na(data$mailing) & !is.na(data$school)),]
mailing <- data.frame(mailing_school$mailing)
optin <- likert(mailing, grouping = mailing_school$school)
optin_p1 <- (plot(optin) + ggtitle('Affiliation with CEWIT')
             + theme_fivethirtyeight()
             + theme(title = element_text(size=24))
             + theme(axis.text = element_text(size=12),
                     axis.text.y= element_text(hjust=1, angle=0))
             + theme(legend.position="bottom")
             + theme(legend.text = element_text(size=11), 
                     legend.title = element_text(size=11)))
ggsave(file="mailing_by_school_centered.pdf")

mailing_category <- data[which(!is.na(data$mailing) & !is.na(data$category)),]
mailing <- data.frame(mailing_category$mailing)
optin <- likert(mailing, grouping = mailing_category$category)
optin_p2 <- (plot(optin) + ggtitle('Student Opt-In to Mailing List')
             + theme_fivethirtyeight()
             + theme(legend.position="bottom"))
ggsave(file="mailing_by_category_centered.jpeg")

interests <- data[, 13:31, drop = FALSE]
interests <- rename(interests, c(data_analysis = 'Data Analysis', blogging = 
                                   'Blogging', programming = 'Programming',
                                 graphics = 'Graphic Design', humanities = 
                                   'Digital Humanities', social_justice = 
                                   'Equity and Justice', social_good = 
                                   'Social Good', social_media = 'Social Media',
                                 game_dev = 'Game Development', gaming = 
                                   'Gaming', interaction = 'Human-Computer
                                 Interaction', mobile_app = 'Mobile App
                                 Development', web_dev = 'Web Development',
                                 phys_computing = 'Physical Computing', 
                                 project_mgmt = 'Project Management', 
                                 research = 'Research Technology', security = 
                                   'Technology Security', education = 'K-12
                                 Education Technology', higher_ed = 'Higher
                                 Education Technology'))
topics <- likert(interests)
summary(topics)
topic_p1 <- (plot(topics) + ggtitle('Student Interests by Topic')
             + theme_fivethirtyeight()
             + theme(legend.position="bottom")
             + theme(title = element_text(size=24))
             + theme(axis.text = element_text(size=12),
                     axis.text.y= element_text(hjust=1, angle=0))
             + theme(legend.text = element_text(size=11), 
                     legend.title = element_text(size=11)))
ggsave(file="interests_by_topic.pdf")

# need yes-only by school
# need to fill by grad/undergrad (need new variable)
# currently too messy
yes_mailing <- data[data$mailing == 'Yes',]
yes_count <- nrow(yes_mailing)
sorted_levels = names(sort(table(yes_mailing$school)))
data$school <- factor(data$school, levels = sorted_levels)
p5 <- (ggplot(yes_mailing[!is.na(yes_mailing$school),], aes(school, fill=level))
       + geom_bar()
       + theme_solarized()
       + coord_flip())

### INTEREST IN TECH CAREER ###
career_level <- data[which(!is.na(data$it_career) & !is.na(data$level)),]
career <- data.frame(career_level$it_career)
want_career <- likert(career, grouping = career_level$level)
career_p1 <- (plot(want_career) 
              + ggtitle('Student Interest in Tech Career')
              + theme_fivethirtyeight()
              + theme(legend.position="bottom")
              + theme(title = element_text(size=24))
              + theme(axis.text = element_text(size=15))
              + theme(legend.text = element_text(size=12), 
                      legend.title = element_text(size=12)))
ggsave(file="it_career_interest.pdf")

### INTEREST IN MENTORING ###


### INTEREST IN SPECIFIC TECHNOLOGY ###

# Testing script
students <- c('001', '002', '003', '004', '005')
school <- c('kelley', 'spea', 'kelley', 'spea', 'spea')
mailing <- c('yes', 'no', 'yes', 'no', 'yes')
df <- data.frame(students, school, mailing)
