library(foreign)
library(mice)
library(tidyverse)

setwd("C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit")

dataset <- read.spss("Brexit_preprocessed.sav", to.data.frame=TRUE)
data <- dataset %>% select(-c(Genecon)) %>% drop_na()

head(data)
dim(data)

md.pattern(data, rotate.names = TRUE)

names(data)

head(data)
num_data <- sapply(data, as.numeric)
head(num_data)

empty_run <- ampute(data, run = FALSE)
mypat <- empty_run$patterns[1,]
mypat[1,1] <- 1
mypat[1,12] <- 0

myweights <- empty_run$weights[1,]
myweights[1,] <- 0
myweights[1,12] <- 1 # MNAR
myweights[1,13] <- 1 # MAR high cor 0.6.0.7
myweights[1,2] <- 1 # MAR low cor 0.2

new_name <- paste0('C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit/MissingDataExperiments/Brexit_', eval(var), '_', eval(type), '.sav')

new_name

props <- c(0.05, 0.1, 0.2, 0.4)
mechs <- c('MCAR', 'MARh', 'MARl', 'MNAR')

nsims <- length(props) * length(mechs)

write_csv(data, path = new_name)

?write.csv

for(i in 1:length(props)){
  for(j in 1:length(mechs)){
    # ampute
    # save
  }
}
  
incomp <- ampute(data)$amp

new_name <- paste0('C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit/MissingDataExperiments/Brexit_', eval(var), '_', eval('emp'), '.sav')
write_csv(incomp, path = new_name)
