#' Mean of each sample row
#'
#' @param samples Numeric matrix, one row per sample.
#' @return Numeric vector with one mean per row. A row with a missing
#'   measurement has an unknown (NA) mean. Zero rows give numeric(0).
summarise_samples <- function(samples) {
  result <- numeric(nrow(samples))
  for (i in 1:nrow(samples)) {
    result[i] <- mean(samples[i, ], na.rm = TRUE)
  }
  result
}
