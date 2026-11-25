format_measurement <- function(x) {
  paste(x, "mg/L")
}

format.measurement <- function(x, ...) {
  format_measurement(unclass(x))
}

.legacy_start <- function() {
  .legacy_end()
}

.legacy_end <- function() {
  "obsolete"
}
