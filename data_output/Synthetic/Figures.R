library(ggplot2)
library(readxl)
library(tidyverse)
library(RColorBrewer)
library(mice)
library(xtable)

setwd("C:/Users/20200059/Documents/Github/EMM_RCS/data_output/Synthetic/")

#### Simulation results ####
dataa <- read_excel("Experiment_['y', [1, 2, 3], [1, 2, 3], 10000, 10, 0.5, [1, 2, 3, 4], 10]a.xlsx")
datab <- read_excel("Experiment_['y', [1, 2, 3], [1, 2, 3], 10000, 10, 0.5, [1, 2, 3, 4], 10]b.xlsx")
data <- rbind(dataa,datab[,0:8])

class(data$quality_value)

sum <- data %>%
  mutate(qv_yes = ifelse(quality_value != 0, 1, 0)) %>%
  #filter(quality_value != 0) %>%
  group_by(distance, sd, d, qv_yes) %>% 
  summarize(n = n(),
            medq = median(quality_value),
            medr = median(rank),
            minq = min(quality_value),
            maxq = max(quality_value)) 

data %>% 
  filter(quality_value == 0) %>%
  group_by(distance, sd, d) %>% 
  summarize(c = n())

data %>%
  filter(distance == 1) %>%
  filter(sd == 1) %>%
  filter(d == 2) %>%
  summarise(med = median(quality_value))

plot <- data %>% 
  #filter(quality_value != 0) %>%
  filter(d != 1) %>%
  filter(distance != 2) %>%
  mutate(quality_value = ifelse(quality_value == 0, NA, quality_value)) %>%
  mutate(group = as.character(interaction(distance,sd,d, sep="."))) %>%
  arrange(desc(group)) %>%
  mutate(group = fct_reorder(as.factor(group), desc(group))) %>%
  ggplot(aes(y=quality_value, x=as.factor(group), fill=as.factor(d))) + 
  geom_boxplot(outlier.color=NA,size=0.1)+ 
  #geom_violin(trim=TRUE,color = NA) + 
  coord_flip() +
  theme_bw(base_size=7) + 
  #ylab("") +
  ylab("quality value of the true subgroup") +
  #ggtitle("Quality value of subgroup for varying distance, sd and size") +
  scale_y_continuous(breaks=seq(0,45,by=5))+
  theme(axis.title.y=element_blank(),
        #axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        axis.text.x=element_text(size=7),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        #panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        #panel.border = element_blank(),
        panel.background = element_blank()) + 
  guides(fill=FALSE) + 
  geom_hline(yintercept=13.6)

plot
name <- paste('./syntheticplot.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 6, units = "cm")


