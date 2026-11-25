# SPDX-License-Identifier: MIT

#' Select measurement columns
#' @param samples A base data frame.
#' @param columns Character column names.
#' @return A data frame with the selected columns.
#' @export
select_measurements <- function(samples, columns) {
  # Select the columns
  samples[, columns] # nolint
}
