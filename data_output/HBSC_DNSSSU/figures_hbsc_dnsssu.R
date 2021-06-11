library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)

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

# prevalence, max
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210605_None_[8, 40, 3, 20]_[0.05, 1.0]_[True, 100]_[0.9, 80]_['prev', 'data', None, None, 'max', None]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(0,1:25), ]
#sel <- data[data$subgroup %in% c(1,3,7,18,19,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")
#pal <- c("#636363", gg_color_hue(nr_subgroups+1))
trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("") + 
  ylab("") + #ylab("Prevalence") + 
  scale_color_manual(values = pal, 
                     labels = c("1", "3", "7", "18", "19", "D"),
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

name <- paste('./data_output/HBSC_DNSSSU/MPALC/mpalc_prev_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# mov avg prevalence slope, max
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210605_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'data', None, None, 'max', None]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  filter(meting != 2019) %>%
  #mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), length(subgroup_numbers) + 1)) %>%
  mutate(year = rep(c(1:8), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

#sel <- data[data$subgroup %in% c(0,1:25), ]
sel <- data[data$subgroup %in% c(1,6,11,18,50), ]
pal = c("#fdb462", "#bebada", "#b3de69", "#fccde5", "#636363")
#pal <- c("#636363", gg_color_hue(nr_subgroups+1))
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=c(1:8),
                     labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) +
  scale_color_manual(values = pal, 
                     labels = c("1", "6", "11", "18", "D"),
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

name <- paste('./data_output/HBSC_DNSSSU/MPALC/mpalc_mov_avg_slope_max.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# mov avg prevalence slope, count
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210605_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'value', 0.0, False, 'count', 0.01]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  filter(meting != 2019) %>%
  #mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), length(subgroup_numbers) + 1)) %>%
  mutate(year = rep(c(1:8), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

#sel <- data[data$subgroup %in% c(0,1:25), ]
sel <- data[data$subgroup %in% c(3,13,15,18,50), ]
pal = c("#fdb462", "#80b1d3", "#b3de69", "#fccde5", "#636363")
#pal <- c("#636363", gg_color_hue(nr_subgroups+1))
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=c(1:8),
                     labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) +
  scale_color_manual(values = pal, 
                     #labels = c("1", "13", "15", "18", "D"),
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

name <- paste('./data_output/HBSC_DNSSSU/MPALC/mpalc_mov_avg_slope_count.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

### combined sg 11 from mov avg slope max and 3,13,15,18 from mov avg slope count
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210605_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'data', None, None, 'max', None]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data1 <- rbind(all_params_adapted, general_params_adapted) %>%
  filter(meting != 2019) %>%
  #mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), length(subgroup_numbers) + 1)) %>%
  mutate(year = rep(c(1:8), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210605_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'value', 0.0, False, 'count', 0.01]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data2 <- rbind(all_params_adapted, general_params_adapted) %>%
  filter(meting != 2019) %>%
  #mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), length(subgroup_numbers) + 1)) %>%
  mutate(year = rep(c(1:8), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- rbind(data2[data2$subgroup %in% c(3,13,15,18,50), ],
             data1[data1$subgroup %in% c(11), ]) %>%
  mutate(type = c(rep(1, 40), rep(2, 8))) %>%
  mutate(subgroup = ifelse(subgroup == 11, 51, subgroup))
sel$int <- as.numeric(paste(sel$subgroup, sel$type, sep="."))

pal = c("#fdb462", "#fb8072", "#b3de69", "#fccde5", "#636363", "#80b1d3")
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, 
                              color = as.factor(int), 
                              linetype = as.factor(int))) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + 
  xlab("") + 
  ylab("") +  
  scale_x_continuous(breaks=c(1:8),
                     labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) +
  #scale_color_manual(values = pal, 
  #                   labels = c("3", "13", "15", "18", "D", "11"),
  #                   name = "") +
  #scale_color_discrete(values = pal) +
  scale_color_manual(name ="", values = pal, labels = c("3", "13", "15", "18", "Psi", "11")) + 
  scale_linetype_manual(name = "", values=c(1,1,1,1,1,2), labels = c("3", "13", "15", "18", "Psi", "11")) +
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

name <- paste('./data_output/HBSC_DNSSSU/MPALC/mpalc_mov_avg_slope_count_combi.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# mov avg prev slope, multiply, count
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210606_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'value', 0.0, 'multiply', 'count', 1, 'max']"
file_name <- "20210606_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'value', 0.0, 'multiply', 'count', 0.5, 'max']"
 
out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  filter(meting != 2019) %>%
  mutate(year = rep(c(1:8), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

sel <- data[data$subgroup %in% c(1:25,50), ]
#sel <- data[data$subgroup %in% c(1,3,7,18,19,50), ]
#pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  scale_x_continuous(breaks=c(1:8),
                     labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) +
  xlab("") + 
  ylab("") + #ylab("Prevalence") + 
  scale_color_manual(values = pal, 
                     #labels = c("1", "3", "7", "18", "19", "D"),
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

name <- paste('./data_output/HBSC_DNSSSU/MPALC/mpalc_prev_slope_count_multiply.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")
