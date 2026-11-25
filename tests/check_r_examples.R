reference <- readLines("plugin/skills/slopstop-python-r/references/r.md", warn = FALSE)
example_env <- new.env(parent = baseenv())

for (start in which(reference == "```r")) {
  remaining <- seq.int(start + 1L, length(reference))
  closing <- match("```", reference[remaining])
  stopifnot(!is.na(closing))
  code <- reference[remaining[seq_len(closing - 1L)]]
  eval(parse(text = code), envir = example_env)
}

stopifnot(is.na(mean(example_env$measurements)))
stopifnot(identical(mean(example_env$measurements, na.rm = TRUE), 3))
stopifnot(is.nan(mean(numeric(0))))
samples <- data.frame(sample_id = 1:2, value = c(3, 4))
selected <- example_env$select_measurements(samples, "value")
stopifnot(identical(dim(selected), c(2L, 1L)))
empty <- example_env$select_measurements(samples[FALSE, ], "value")
stopifnot(identical(dim(empty), c(0L, 1L)))
cat("PASS: R reference examples and data-shape contracts\n")
