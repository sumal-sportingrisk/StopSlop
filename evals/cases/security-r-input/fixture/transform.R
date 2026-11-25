apply_transform <- function(samples, expression) {
  eval(parse(text = expression), envir = list(samples = samples))
}
