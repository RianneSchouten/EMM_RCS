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
data1 <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

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
data2 <- rbind(all_params_adapted, general_params_adapted) %>%
  #filter(meting != 2019) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c(1:8), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

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
data3 <- rbind(all_params_adapted, general_params_adapted) %>%
  #filter(meting != 2019) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), length(subgroup_numbers) + 1)) %>%
  #mutate(year = rep(c(1:8), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

make_figure <- function(sel, pal, labels){
  trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
    geom_point(size=0.8) + 
    geom_line(size=0.7) + 
    ggtitle(label = "Prevalence of alcohol use") + 
    scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
    scale_y_continuous(limits = c(0,1)) + 
    xlab("") + 
    ylab("") + #ylab("Prevalence in alcohol use") + 
    scale_color_manual(values = pal, 
                     labels = labels,
                     name = "") + 
    guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
    theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        #legend.direction = "vertical",
        plot.title = element_text(hjust = 0, vjust=-8), 
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
  return(trend_plot)
}

# only dataset trend
sel <- data1[data1$subgroup %in% c(50), ]
pal <- c("#636363")
labels <- c('D')
trend_plot <- make_figure(sel, pal, labels)
trend_plot
name <- paste('./data_output/HBSC_DNSSSU/figD.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# dataset trend and sg 1, 7
sel <- data1[data1$subgroup %in% c(50,1,7), ]
pal <- c("#fdb462", "#bebada", "#636363")
labels <- c('1', '7', 'D')
trend_plot <- make_figure(sel, pal, labels)
name <- paste('./data_output/HBSC_DNSSSU/figD17.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")

# dataset trend and sg 1, 7 and sg 11
sel <- rbind(sel, data2[data2$subgroup %in% c(11), c('n', 'prev', 'prev_se', 'subgroup', 'meting', 'year')])
pal <- c("#fdb462", "#bebada", "#fb8072", "#636363")
labels <- c('1', '7', '11', 'D')
trend_plot <- make_figure(sel, pal, labels)
name <- paste('./data_output/HBSC_DNSSSU/figD1711.pdf', sep = "", collapse = NULL)
ggsave(name, width = 8, height = 5, units = "cm")


  
  
  
