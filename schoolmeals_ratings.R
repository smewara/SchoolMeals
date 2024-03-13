# Load libraries
library(tidyverse)
library(readxl)
library(scales)

# Set path
path = getwd()

# Import data
school_1a <- read_excel(paste(path, "School_1a_2021.xlsx", sep = "/"), "School_Meal_Rating_Q29")
school_1b <- read_excel(paste(path, "School_1b_2021.xlsx", sep = "/"), "School_Meal_Rating_Q29")
school_2 <- read_excel(paste(path, "School_2_2021.xlsx", sep = "/"), "School_Meal_Rating_Q29")

# Add school name
school_1a <- school_1a %>% mutate(school = "1a: St Leonard's")
school_1b <- school_1b %>% mutate(school = "1b: Trinity")
school_2 <- school_2 %>% mutate(school = "2: Doddiscombsleigh")

# Append individual school files and add proportions
df_ratings <- rbind(school_1a, school_1b, school_2) %>%
  mutate(school = as.factor(school)) %>%
  mutate(Phrase = as.numeric(Phrase)) %>%
  filter(!is.na(Phrase)) %>%
  mutate(Phrase = as.factor(Phrase)) %>%
  complete(school, Phrase, fill = list(val = 0)) %>%
  replace(is.na(.), 0) %>%
  group_by(school) %>%
  mutate(proportion = prop.table(Frequency))

# Check proportions total to 1
df_ratings %>%
  group_by(school) %>%
  summarise(total_proportion = sum(proportion))

# Plot school meal rating as heat map
# Get average rating by school
q29_avg <- df_ratings %>%
  group_by(school) %>%
  summarise(rating = weighted.mean(as.numeric(Phrase), Frequency))
# Get sample size
n <- df_ratings %>%
  group_by(school) %>%
  summarise(n = sum(Frequency)) %>%
  mutate(label = paste(school, paste("n =", n), sep = "\n"))
# Plot heat map of rating distributions
  ggplot() +
  geom_tile(data = df_ratings, aes(x = school, y = Phrase, fill = proportion)) +
  scale_fill_gradient(low="white", high="#619CFF", labels=scales::label_percent()) +
  labs(title = "Q29: How healthy would you rate the current school meal provision at school? 1 = Lowest, 10 = Highest
       \n Proportion of responses by school",
       x = "School",
       y = "Rating",
       fill = "Proportion of \nresponses",
       col = "Average rating") +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_text(size = 12),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11),
        panel.background = element_blank()) +
  scale_color_discrete(labels = " ") +
  scale_colour_manual(values = "red") +
  scale_x_discrete(labels = rev(n$label), limits = rev) +
  geom_point(data = q29_avg, aes(x = school, y = rating, col = ""), size = 5) +
  coord_flip()
ggsave("Plots/q29_school.png")