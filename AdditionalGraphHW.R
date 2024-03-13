#### This is an addition of one graph to the work already provided by Ho Woo ####

#### Load libraries ####

library(tidyverse)
library(ggstats)
library(EnvStats) # for adding sample size

#### Load data ####

# Import data from Python csv output
df_schools <- read_csv('df_schools.csv')

# Convert character columns to factors
# This doesn't seem to work, so I have converted manually when plotting
df_schools <- df_schools %>%
  mutate(across(where(is.character), as.factor)) %>%
  mutate(Q36_Cleansed = factor(Q36_Cleansed, levels = c("Yes", "No", "Depends"))) %>%
  mutate(Q37_Bins = factor(Q37_Bins, levels = c(1, 2, 3, "4+"))) %>%
  mutate(Ethnicity_2 = factor(Ethnicity_2, levels = c("White", "Ethnic Minority"))) %>%
  mutate(Stakeholder = factor(Stakeholder, levels = c("Parent/Carer", "Staff - Teaching", "Staff - Other")))


#### Plots for Q36: Do meat-free days sound like a good idea? ####


# Proportions by Packed Lunch Response
# Get sample size
n <- df_schools %>%
  group_by(Q18) %>%
  summarise(n = sum(!is.na(Q36_Cleansed))) %>%
  mutate(label = paste(Q18, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(Q18)) %>%
  ggplot(aes(x = Q18,
             y = after_stat(prop),
             by = Q18,
             fill = Q36_Cleansed)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q36: Do meat-free days sound like a good idea?
       \nProportion of responses by response of bringing packed-lunch",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q36_packedlunch.png")