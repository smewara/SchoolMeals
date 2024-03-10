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


# Proportions by school
# Get sample size
n <- df_schools %>%
  group_by(School) %>%
  summarise(n = sum(!is.na(Q36_Cleansed))) %>%
  mutate(label = paste(School, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(School)) %>%
  ggplot(aes(x = School,
             y = after_stat(prop),
             by = School,
             fill = Q36_Cleansed)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q36: Do meat-free days sound like a good idea?
       \nProportion of responses by school",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q36_school.png")


# Proportions by school, parents/carers only
# Get sample size
n <- df_schools %>%
  filter(Stakeholder == "Parent/Carer") %>%
  group_by(School) %>%
  summarise(n = sum(!is.na(Q36_Cleansed))) %>%
  mutate(label = paste(School, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(School)) %>%
  filter(Stakeholder == "Parent/Carer") %>%
  ggplot(aes(x = School,
             y = after_stat(prop),
             by = School,
             fill = Q36_Cleansed)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q36: Do meat-free days sound like a good idea?
       \nProportion of parents/carer responses by school",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q36_school_parents.png")


# Proportions by school, staff only
# Get sample size
n <- df_schools %>%
  filter(Stakeholder != "Parent/Carer") %>%
  group_by(School) %>%
  summarise(n = sum(!is.na(Q36_Cleansed))) %>%
  mutate(label = paste(School, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(School)) %>%
  filter(Stakeholder != "Parent/Carer") %>%
  ggplot(aes(x = School,
             y = after_stat(prop),
             by = School,
             fill = Q36_Cleansed)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q36: Do meat-free days sound like a good idea?
       \nProportion of staff responses by school",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q36_school_staff.png")


# Proportions by stakeholder
# Get sample size
n <- df_schools %>%
  group_by(Stakeholder) %>%
  summarise(n = sum(!is.na(Q36_Cleansed))) %>%
  mutate(label = paste(Stakeholder, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(Stakeholder)) %>%
  ggplot(aes(x = Stakeholder,
             y = after_stat(prop),
             by = Stakeholder,
             fill = Q36_Cleansed)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q36: Do meat-free days sound like a good idea?
       \nProportion of responses by stakeholder",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q36_stakeholder.png")


# Proportions by ethnicity
# Get sample size
n <- df_schools %>%
  group_by(Ethnicity) %>%
  summarise(n = sum(!is.na(Q36_Cleansed))) %>%
  mutate(label = paste(str_wrap(Ethnicity, width = 10), paste("n = ", n, sep = ""), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(Ethnicity)) %>%
  ggplot(aes(x = Ethnicity,
             y = after_stat(prop),
             by = Ethnicity,
             fill = Q36_Cleansed)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q36: Do meat-free days sound like a good idea?
       \nProportion of responses by ethnicity",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 9))
ggsave("Plots/q36_ethnicity.png")


# Proportions by FSM eligibility
# Get sample size
n <- df_schools %>%
  group_by(FSM_Eligibility) %>%
  summarise(n = sum(!is.na(Q36_Cleansed))) %>%
  mutate(label = paste(FSM_Eligibility, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(FSM_Eligibility)) %>%
  ggplot(aes(x = FSM_Eligibility,
             y = after_stat(prop),
             by = FSM_Eligibility,
             fill = Q36_Cleansed)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q36: Do meat-free days sound like a good idea?
       \nProportion of responses by eligibility for free school meals",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q36_fsm.png")



#### Plots for Q37: How many meat-free days per week sound reasonable to you? ####


# Proportions by school
# Get sample size
n <- df_schools %>%
  group_by(School) %>%
  summarise(n = sum(!is.na(Q37_Bins))) %>%
  mutate(label = paste(School, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(School)) %>%
  ggplot(aes(x = School,
             y = after_stat(prop),
             by = School,
             fill = Q37_Bins)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q37: How many meat-free days per week sound reasonable?
       \nProportion of responses by school",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("1" = "#f8766d", "2" = "#00BA38", "3" = "#619CFF", "4+" = "#C77CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q37_school.png")



# Proportions by school, parents/carers only
# Get sample size
n <- df_schools %>%
  filter(Stakeholder == "Parent/Carer") %>%
  group_by(School) %>%
  summarise(n = sum(!is.na(Q37_Bins))) %>%
  mutate(label = paste(School, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(School)) %>%
  filter(Stakeholder == "Parent/Carer") %>%
  ggplot(aes(x = School,
             y = after_stat(prop),
             by = School,
             fill = Q37_Bins)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q37: How many meat-free days per week sound reasonable?
       \nProportion of parent/carer responses by school",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("1" = "#f8766d", "2" = "#00BA38", "3" = "#619CFF", "4+" = "#C77CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q37_school_parents.png")


# Proportions by school, staff only
# Get sample size
n <- df_schools %>%
  filter(Stakeholder != "Parent/Carer") %>%
  group_by(School) %>%
  summarise(n = sum(!is.na(Q37_Bins))) %>%
  mutate(label = paste(School, paste("n =", n), sep = "\n"))
# Plot
df_schools %>%
  filter(!is.na(School)) %>%
  filter(Stakeholder != "Parent/Carer") %>%
  ggplot(aes(x = School,
             y = after_stat(prop),
             by = School,
             fill = Q37_Bins)) +
  geom_bar(stat = "prop", position = position_dodge(preserve = "single")) +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Q37: How many meat-free days per week sound reasonable?
       \nProportion of staff responses by school",
       y = "Proportion of responses",
       fill = "Response") +
  scale_fill_manual(values = c("1" = "#f8766d", "2" = "#00BA38", "3" = "#619CFF", "4+" = "#C77CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11))
ggsave("Plots/q37_school_staff.png")


#### Plots for Q35: How much would you be willing to pay for healthy and sustainable school meals?


# Price willing to pay
df_schools %>%
  filter(!is.na(Q36_Cleansed)) %>%
  ggplot(aes(x = Q36_Cleansed,
             y = Q35_Cleansed,
             fill = Q36_Cleansed)) +
  geom_point(position = "jitter") +
  labs(title = "Q35: How much would you be willing to pay for health and sustainable school meals?
       \nComparison by school and eligibility",
       y = "Amount willing to pay",
       fill = "Response") +
  scale_fill_manual(values = c("Yes" = "#00BA38", "No" = "#f8766d", "Depends" = "#619CFF")) +
  scale_x_discrete(labels = n$label) +
  theme(plot.title = element_text(hjust = 0.5, size = 13, lineheight = 0.5),
        axis.title.x = element_blank(),
        axis.title.y = element_text(size = 12),
        axis.text = element_text(size = 11)) +
  facet_wrap(~School)
ggsave("Plots/q36_fsm.png")