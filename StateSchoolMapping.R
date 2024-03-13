#### Mapping State/Independent School proportions by Region ####

library(tidyverse)
library(Rmisc)
library(GGally)
library(dplyr)
library(sf)
library(ggplot2)

#Importing lookup and shapefiles for regional mapping.
ltla <- st_read("LAD_Boundaries_UK.shp")
ltla
lookup <- read_csv("LAD_to_Region_Lookup.csv")
lookup

#Importing all school related data.
schooldata <- read_csv("spc_ees_school_characteristics.csv")
meal_data1 <- read_csv("D://MTHM604_Data//03_Sustainable_food//Doctoral_study_data_for_Devon_schools//Survey_data//School_1a_2021.csv")
meal_data2 <- read_csv("D://MTHM604_Data//03_Sustainable_food//Doctoral_study_data_for_Devon_schools//Survey_data//School_1b_2021.csv")
#Duplicate heading removal.
meal_data1 <- meal_data1[-1]
meal_data2 <- meal_data2[-1]
main_meal <- rbind.fill(meal_data1, meal_data2)

#Creating long/lat dataframe.
latdf <- subset(main_meal,!(is.na("LocationLatitude") | is.na("LocationLongitude")))

#Creating id vector for mapping from district admin codes from school data.
lad19cd <- schooldata["district_administrative_code"]

#Creating main dataframe for mapping.
maindata <- schooldata[,c("district_administrative_code", "phase_type_grouping")]
names(maindata)[names(maindata)=="district_administrative_code"] <- "LAD19CD"
maindata[["phase_type_grouping"]][grepl("State-funded", maindata[["phase_type_grouping"]])] <- "State-funded"
maindata$phase_type_grouping <- as.numeric(factor(maindata$phase_type_grouping))
maindata$"phase_type_grouping" <- as.numeric(maindata$"phase_type_grouping")
new_df <- aggregate(maindata[2], by = list(maindata$LAD19CD), FUN=mean)

#New lookup for mapping the country and the southwest independently.
new_lookup <- inner_join(ltla, new_df, by= c("lad19cd" = "Group.1"))
lookup <- filter(lookup, RGN19NM == "South West")
sw_new_lookup <- inner_join(new_lookup, lookup, by= c("lad19cd" = "LAD19CD"))

#UK wide plotting for State School Proportions.
funding_type_map <- ggplot(new_lookup) + 
  geom_sf(aes(fill = phase_type_grouping))+
  scale_fill_gradient2(low = "white", mid = "blue", high = "darkblue", midpoint = median(new_lookup$phase_type_grouping))

#South West wide plotting for State School Proportions.
sw_funding_type_map <- ggplot(sw_new_lookup) + 
  geom_sf(aes(fill = phase_type_grouping))+
  scale_fill_gradient2(low = "white", mid = "blue", high = "darkblue", midpoint = median(sw_new_lookup$phase_type_grouping))

print(sw_funding_type_map)
print(funding_type_map)
#Plotting first 30 coordinates (incomplete as not used).
lat30 <- top_n(latdf, 30)
xy <- latdf[,c("LocationLongitude", "LocationLatitude")]
plot2 <- ggplot(lat30) +
  geom_point(aes(x = LocationLatitude, y = LocationLongitude))
plot2

