# sample_id comes from the lab portal's search box.
fetch_sample <- function(connection, sample_id) {
  query <- paste0("SELECT * FROM dbo.samples WHERE id = '", sample_id, "'")
  DBI::dbGetQuery(connection, query)
}
