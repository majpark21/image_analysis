#' Select Random
#'
#' Select a random subset of time series from a dataset by using unique ID
#' subset. Optionally, a minimum number of observation for the individual IDs
#' can be provided.
#'
#' @param in.file A character or a variable for the current environment. If a
#'   character, a path to a .csv file is expected.
#' @param ntraj Numeric. How many unique IDs to extract?
#' @param col.uniqID Character. Name of the column with unique IDs.
#' @param col.time Character. Name of the column with time.
#' @param col.whatokeep Optional character. Name of the columns to be returned
#'   in the output. If NULL returns all columns. Columns with uniqID and time
#'   are always returned.
#' @param out.file Optional character. If provided the output is saved as a .csv
#'   file to the path indicated by out.file. Otherwise, the new dataset is
#'   returned.
#' @param min.obs Optional numeric. Minimum number of observations of an ID.
#'
#' @return A data.table with the columns indicated in col.whatokeep.
#' @export
#'
#' @examples
select_random_save <- function(in.file, ntraj, min.obs=NULL, col.uniqID, col.time, col.whatokeep=NULL, out.file=NULL){
  require(data.table)
  if(is.character(in.file)) dt <- fread(in.file)
  else dt <- in.file
  # Remove ID and time to avoid duplicate when whatokeep is null
  if(is.null(col.whatokeep)) col.whatokeep <- setdiff(colnames(dt), c(col.uniqID, col.time))
  # Choose IDs to keep, with=FALSE to use arguments provided as characters in data.table
  if(!is.null(min.obs)){
    candidates <- dt[, .N, by=get(col.uniqID)][N >= min.obs, get]
    trajs <- sample(candidates, size=ntraj, replace=FALSE)
  } else {
    trajs <- sample(unlist(unique(dt[, col.uniqID, with=FALSE])), size=ntraj, replace=FALSE)
  }
  dt <- dt[get(col.uniqID) %in% trajs, c(col.uniqID, col.time, col.whatokeep), with=FALSE]
  if(!is.null(out.file)) write.csv(dt, out.file, quote = FALSE, row.names = FALSE)
  else return(dt)
}
