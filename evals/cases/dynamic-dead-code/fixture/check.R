source("rpackage/R/measurements.R")
x <- structure(2, class = "measurement")
stopifnot(identical(format(x), "2 mg/L"))
stopifnot(identical(format_measurement(3), "3 mg/L"))
