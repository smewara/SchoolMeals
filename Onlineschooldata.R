library(tidyverse)
library(Rmisc)
library(GGally)
library(dplyr)
library(ggplot2)
#Prior to importing, replaced ofsted string labels to corresponding numerical 
#ratings.
#Outstanding - 4, Good - 3, Requires improvement - 2. 
#Importing Data and relabelling schools.
data <- read_csv("school_data.csv")
data["school"] <- data$school <- sub("_", " ", data$school)
data["school"] <- str_to_title(data$school)

#Ratings by School, and Income Per Pupil. 
ratings <- ggplot(data, aes(x=school, y=ofsted_rating, fill=total_income_per_pupil))+
  geom_bar(stat="identity")+
  xlab("Schools")+
  ylab("Ofsted Rating")
ratings <-  ratings+ guides(fill=guide_legend(title="Income Per Pupil (£)"))
ratings

#Creating sub-dataframe for filtering n/a from column and inserting two new 
#columns with predicted pupil numbers based on Locrating data.
meal_df <- data[,c("school", "percentage_eligibility_for_free_meals", "total_pupils")]
meal_df <- data%>%filter(percentage_eligibility_for_free_meals!="n/a")
meal_df <- meal_df%>%
  mutate(mealpupils = c(67,1,75))%>%
  mutate(expectedmealpupils = c(109, 7, 44))

#Simple Meals Plot
meals <- ggplot(meal_df,aes(x= school, y= total_pupils, fill=as.numeric(percentage_eligibility_for_free_meals)))+
  geom_bar(stat="identity")+
  xlab("Schools")+
  ylab("Total Pupils")
meals <-  meals +guides(fill=guide_legend(title="Eligibility for Free School Meals (%)"))
meals

#Total pupils per school plotted with respective percentages of free school meals.
#Horizontal line indicators of expected per region for each school. 
meals <- ggplot(meal_df,aes(x= school))+
  geom_bar(aes(y=total_pupils), stat="identity", position="identity", alpha = 1, fill = "grey")+
  geom_bar(aes(y=mealpupils),stat="identity", position="identity", alpha = 0.5, fill = "darkgreen")+
  geom_hline(aes(yintercept=109, colour = "St Leonards"))+
  geom_hline(aes(yintercept=7, colour = "Doddiscombsleigh"))+
  geom_hline(aes(yintercept=44, colour = "Totnes"))+
  scale_colour_manual(name = "Expected", values = c("Doddiscombsleigh" = "dodgerblue2", "St Leonards" = "red", "Totnes" = "green4"))+
  xlab("Schools")+
  ylab("Total Pupils")+
  ggtitle("Total Pupils and Percentage of Free School Meals")

meals  

#Bar plot of Ethnicity Percentages
ethn <- ggplot(data, aes(x = school))+
  geom_bar(aes(y=white_british),stat="identity",position = "identity",alpha = 0.5, fill = "dodgerblue2")+
  geom_bar(aes(y=white_other),stat="identity", position="identity",alpha = 0.5, fill = "red")+
  geom_bar(aes(y=other),stat="identity", position="identity",alpha = 0.5, fill = "green4")+
  geom_bar(aes(y=chinese),stat="identity", position="identity",alpha = 0.5, fill = "orange")+
  geom_bar(aes(y=mixed_other),stat="identity", position="identity",alpha = 0.5, fill = "black")+
  geom_bar(aes(y=white_and_asian),stat="identity", position="identity",alpha = 0.5, fill = "gold1")+
  geom_bar(aes(y=indian),stat="identity", position="identity",alpha = 0.5, fill = "skyblue")+
  geom_bar(aes(y=white_and_black),stat="identity", position="identity",alpha = 0.5, fill = "palegreen2")+
  geom_bar(aes(y=bangladeshi),stat="identity", position="identity",alpha = 0.5, fill = "purple")+
  xlab("Schools")+
  ylab("Ethnicities")+
  ggtitle("Ethnicities by Percentage for each School")

ethn

