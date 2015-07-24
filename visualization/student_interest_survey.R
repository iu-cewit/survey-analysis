library(ggplot2)
library(ggthemes)

### DATA ###
data = read.csv("/Users/nbrodnax/Indiana/CEWIT/iu-cewit/working/data.csv", 
                header=FALSE)
#convert missing to null values
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
for (col in c(10,13:31)) {
  data[,col] <- as.numeric(as.character(data[,col]))
  }
for (col in c(8:9)) {
  data[,col] <- factor(data[,col])
}
data$mailing <- factor(data$mailing, levels = c('Yes', 'No'))
data$level <- factor(data$level, levels = c('Freshman', 'Sophomore', 'Junior',
                                            'Senior', 'Master', 'PhD', 'JD',
                                            'Other'))
data$mentor <- factor(data$mentor, levels = c('peer', 'faculty', 'staff',
                                              'serve'))

### AFFILIATE BACKGROUND ###

# by level
plot1 <- (ggplot(data[!is.na(data$mailing),], aes(level, fill=mailing)) 
       + geom_bar()
       + theme_solarized()
       + scale_color_solarized())

# by career interest
plot2 <- (ggplot(data[!is.na(data$it_career),], aes(level, fill=it_career)) 
          + geom_bar()
          + theme_solarized()
          + scale_color_solarized())

# by school


# by field category


### INTERESTS ###

# skills


# technologies


# mentoring by type