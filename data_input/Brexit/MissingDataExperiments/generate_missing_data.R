library(foreign)
library(mice)
library(tidyverse)

setwd("C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit")

dataset <- read.spss("Brexit_preprocessed.sav", to.data.frame=TRUE)
data <- dataset %>% select(-c(Genecon)) %>% drop_na()

# write short dataset, run emm-rcs and work from there
new_name <- paste0('C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit/MissingDataExperiments/Brexit_short.sav')
write_csv(data, path = new_name)

sum(data$Hindsight == 'Wrong')/nrow(data)

# MNAR
props <- c(0.1, 0.3, 0.5, 0.7, 0.9)
mech = 'MNAR'
for(i in 1:length(props)){
  inc_data <- data
  myprop <- props[i]
  w <- as.numeric(inc_data$Hindsight == 'Wrong')
  r <- rbinom(n=sum(w), size=1, prob=myprop)
  R <- rep(0, length(w))
  counter = 0
  for(j in 1:length(R)){
    if(w[j] == 1){
      counter = counter + 1
      if(r[counter] == 1){
        R[j] <- 1
      }
    }
  }
  print(sum(R)/length(w))
  inc_data[R == 1, 'Hindsight'] <- NA
  new_name <- paste0('C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit/MissingDataExperiments/Brexit_', eval(myprop), '_', eval(mech), '.sav')
  write_csv(inc_data, path = new_name)
}

# MAR
props <- c(0.1, 0.3, 0.5, 0.7, 0.9)
mech <- 'MAR'
for(i in 1:length(props)){
  inc_data <- data
  myprop <- props[i]
  w <- as.numeric(inc_data$EURef2016 == 'Remain')
  r <- rbinom(n=sum(w), size=1, prob=myprop)
  R <- rep(0, length(w))
  counter = 0
  for(j in 1:length(R)){
    if(w[j] == 1){
      counter = counter + 1
      if(r[counter] == 1){
        R[j] <- 1
      }
    }
  }
  print(sum(R)/length(w))
  inc_data[R == 1, 'Hindsight'] <- NA
  new_name <- paste0('C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit/MissingDataExperiments/Brexit_', eval(myprop), '_', eval(mech), '.sav')
  write_csv(inc_data, path = new_name)
}

# MCAR
props <- 0.51*c(0.1, 0.3, 0.5, 0.7, 0.9)
mech <- 'MCAR'
for(i in 1:length(props)){
  inc_data <- data
  myprop <- props[i]
  w <- rep(1, length(inc_data))
  r <- rbinom(n=sum(w), size=1, prob=myprop)
  R <- rep(0, length(w))
  counter = 0
  for(j in 1:length(R)){
    if(w[j] == 1){
      counter = counter + 1
      if(r[counter] == 1){
        R[j] <- 1
      }
    }
  }
  print(sum(R)/length(w))
  inc_data[R == 1, 'Hindsight'] <- NA
  new_name <- paste0('C:/Users/20200059/Documents/Github/EMM_RCS/data_input/Brexit/MissingDataExperiments/Brexit_', eval(myprop), '_', eval(mech), '.sav')
  write_csv(inc_data, path = new_name)
}





