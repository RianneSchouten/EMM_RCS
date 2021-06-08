library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)
library(ggthemes)

setwd("C:/Users/20200059/Documents/Github/EMM_RCS/")

gg_color_hue <- function(n) {
  hues = seq(15, 375, length = n + 1)
  hcl(h = hues, l = 65, c = 100)[1:n]
}

extract_legend <- function(my_ggp) {
  step1 <- ggplot_gtable(ggplot_build(my_ggp))
  step2 <- which(sapply(step1$grobs, function(x) x$name) == "guide-box")
  step3 <- step1$grobs[[step2]]
  return(step3)
}

### import functions through python
source_python("import_subgroup.py")

# euspeed1num, mean, average
nr_subgroups = 24.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

data_name <- 'Eurobarometer'
trend_name <- 'euspeed1num'
file_name <- "20210608_None_[8, 40, 3, 25]_[0.05, 0.5]_[True, 20]_[0.9, 80]_['mean', 'data', None, None, 'average', None, 'max']"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, nrow(general_params))) %>%
  select(-min_size) 
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
T <- c('86','87','', '', '90', '', '92','93','94','95','96','97','', '99','00','01')
data <- rbind(all_params_adapted,general_params_adapted) %>%
  mutate(year = rep(c(1,2,5,7:12,14:16), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(T, length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

#sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,3,14,20,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3","#636363")

trend_plot <- ggplot(sel, aes(x = year, y = mean, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=c(1:16),
                     labels=T) +
  scale_color_manual(values = pal, 
                     labels = c("1", "3", "14", "20", "D"),
                     name = "") +
  guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
  theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        #legend.direction = "vertical",
        #plot.title = element_text(hjust = 0, vjust=-3), 
        legend.box.margin = margin(0,0,-0.2,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        #panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.text  = element_text(size = 7),
        legend.key.width = unit(0.2,"cm"),
        legend.key.size = unit(0.2,"cm"),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
trend_plot

name <- paste('./data_output/Eurobarometer/euspeed1num/euspeed1num_mean_average.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# euspeed1num, mean, max
nr_subgroups = 24.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

data_name <- 'Eurobarometer'
trend_name <- 'euspeed1num'
file_name <- "20210608_None_[8, 40, 3, 25]_[0.05, 0.5]_[True, 20]_[0.9, 80]_['mean', 'data', None, None, 'max', None, 'max']"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, nrow(general_params))) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
T <- c('86','87','', '', '90', '', '92','93','94','95','96','97','', '99','00','01')
data <- rbind(all_params_adapted,general_params_adapted) %>%
  mutate(year = rep(c(1,2,5,7:12,14:16), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

#sel <- data[data$subgroup %in% c(0,1:25), ]
sel <- data[data$subgroup %in% c(1,4,10,18,19,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")

trend_plot <- ggplot(sel, aes(x = year, y = mean, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=c(1:16),
                     labels=T) +
  scale_color_manual(values = pal, 
                     labels = c("1", "4", "10", "18", "19", "D"),
                     name = "") +
  guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
  theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        #legend.direction = "vertical",
        #plot.title = element_text(hjust = 0, vjust=-3), 
        legend.box.margin = margin(0,0,-0.2,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        #panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.text  = element_text(size = 7),
        legend.key.width = unit(0.2,"cm"),
        legend.key.size = unit(0.2,"cm"),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
trend_plot

name <- paste('./data_output/Eurobarometer/euspeed1num/euspeed1num_mean_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# lrsnum, mean, max
nr_subgroups = 24.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'Eurobarometer'
trend_name <- 'lrsnum'
file_name <- "20210605_None_[8, 40, 3, 25]_[0.05, 0.5]_[False, 0]_[0.9, 80]_['mean', 'data', None, None, 'max', None]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, nrow(general_params))) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
T <- c('76', '',' 77','', '78','', '79','', '80','', '81','', '82','', 
       '83','', '84','', '85','', '86','', '87','',
       '88','', '89','', '90','', '91','', '92','', '93','', '94','',
       '95','', '96','', '97','', '98','', '99','', '00','', '01','',
       '02')
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(c(1:53), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,2,4,12,13,19,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

trend_plot <- ggplot(sel, aes(x = year, y = mean, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=1:53,
                     labels=T) +
  scale_color_manual(values = pal, 
                     #labels = c("1", "4", "10", "18", "19", "D"),
                     name = "") +
  guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
  theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        #legend.direction = "vertical",
        #plot.title = element_text(hjust = 0, vjust=-3), 
        legend.box.margin = margin(0,0,-0.2,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        #panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.text  = element_text(size = 7),
        legend.key.width = unit(0.2,"cm"),
        legend.key.size = unit(0.2,"cm"),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
trend_plot

name <- paste('./data_output/Eurobarometer/lrsnum/lrsnum_mean_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# lrsnum, mean, average
nr_subgroups = 24.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

data_name <- 'Eurobarometer'
trend_name <- 'lrsnum'
file_name <- "20210606_None_[8, 40, 3, 25]_[0.05, 0.5]_[False, 20]_[0.9, 80]_['mean', 'data', None, None, 'average', None, 'max']"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, nrow(general_params))) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
T <- c('76', '',' 77','', '78','', '79','', '80','', '81','', '82','', 
       '83','', '84','', '85','', '86','', '87','',
       '88','', '89','', '90','', '91','', '92','', '93','', '94','',
       '95','', '96','', '97','', '98','', '99','', '00','', '01','',
       '02')
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(c(1:53), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,2,4,13,19,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

trend_plot <- ggplot(sel, aes(x = year, y = mean, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=1:53,
                     labels=T) +
  scale_color_manual(values = pal, 
                     #labels = c("1", "2", "4", "13", "19", "D"),
                     name = "") +
  guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
  theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        #legend.direction = "vertical",
        #plot.title = element_text(hjust = 0, vjust=-3), 
        legend.box.margin = margin(0,0,-0.2,0, "line"),
        #axis.title.y = element_text(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        #panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.text  = element_text(size = 7),
        legend.key.width = unit(0.2,"cm"),
        legend.key.size = unit(0.2,"cm"),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
trend_plot

name <- paste('./data_output/Eurobarometer/lrsnum/lrsnum_mean_average.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")
