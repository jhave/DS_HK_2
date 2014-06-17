setwd('../data/poetryFoundation/txt_60')
files <- list.files(pattern = "[.]txt$")

library(rbenchmark)
benchmark(replications = 10, order = "user.self",
          LAPPLY = {
            read.all <- lapply(files, read.table, header = TRUE)
            data1 <- do.call(rbind, read.all)
          },
          FOREACH = {
            library(doParallel)
            registerDoParallel(cores = 4)
            library(foreach)
            data2 <- foreach(i = files, .combine = rbind) %dopar% read.table(i, header = TRUE)
          }
)

library(compare)
all.equal(data1, data2)