source("summarise.R")
stopifnot(identical(summarise_samples(matrix(c(2, 4), nrow = 1)), 3))
stopifnot(is.na(summarise_samples(matrix(c(2, NA_real_), nrow = 1))))
stopifnot(identical(summarise_samples(matrix(numeric(0), nrow = 0, ncol = 2)), numeric(0)))
