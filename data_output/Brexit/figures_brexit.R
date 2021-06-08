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

# Leaver, prev, max # with certain attributes
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

data_name <- 'Brexit'
trend_name <- 'Leaver_with'
file_name <- "20210606_None_[8, 20, 3, 20]_[0.1, 0.7]_[True, 100]_[0.9, 40]_['prev', 'data', None, None, 'max', None, 'max']"

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
T <- c(1:10)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(T, length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(1:20,50), ]
sel <- data[data$subgroup %in% c(1,4,11,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#636363")

trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=T) +
  scale_color_manual(values = pal, 
                     labels = c("1", "4", "11", "D"),
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

name <- paste('./data_output/Brexit/Leaver_with/leaver_with_prev_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# Leaver, prev_slope, max
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

data_name <- 'Brexit'
trend_name <- 'Leaver_with'
file_name <- "20210606_None_[8, 20, 3, 20]_[0.1, 0.7]_[True, 100]_[0.9, 40]_['prev_slope', 'value', 0, True, 'max', None, 'max']"

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
T <- c(1:10)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(T, length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(1:20,50), ]
sel <- data[data$subgroup %in% c(1,2,9,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#636363")

trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=T) +
  scale_color_manual(values = pal, 
                     labels = c("1", "2", "9", "D"),
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

name <- paste('./data_output/Brexit/Leaver_with/leaver_with_prev_slope_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# Leaver, prev, max, without certain variable
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

data_name <- 'Brexit'
trend_name <- 'Leaver_without'
file_name <- "20210607_None_[8, 20, 3, 20]_[0.1, 0.7]_[True, 100]_[0.9, 40]_['prev', 'data', None, None, 'max', None, 'max']"
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
T <- c(1:10)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(T, length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(1:20,50), ]
sel <- data[data$subgroup %in% c(1,4,6,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#636363")

trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=T) +
  scale_color_manual(values = pal, 
                     #labels = c("1", "4", "6", "D"),
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

name <- paste('./data_output/Brexit/Leaver_without/leaver_without_prev_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# Leaver, prev_slope, max, without certain variable
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

data_name <- 'Brexit'
trend_name <- 'Leaver_without'
file_name <- "20210607_None_[8, 20, 3, 20]_[0.1, 0.7]_[True, 100]_[0.9, 40]_['prev_slope', 'value', 0, True, 'max', None, 'max']"

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
T <- c(1:10)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(T, length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(1:20,50), ]
sel <- data[data$subgroup %in% c(1,3,10,13,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#636363")

trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=T) +
  scale_color_manual(values = pal, 
                     #labels = c("1", "3", "10", "13", "D"),
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

name <- paste('./data_output/Brexit/Leaver_without/leaver_without_prev_slope_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")
