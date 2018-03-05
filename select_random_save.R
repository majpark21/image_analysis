select_random_save <- function(in.file, ntraj, col.uniqID, col.time, col.whatokeep, out.file=NULL){
  require(data.table)
  dt <- fread(in.file)
  trajs <- sample(unlist(unique(dt[, col.uniqID, with=FALSE])), size=ntraj, replace=FALSE)
  dt <- dt[get(col.uniqID) %in% trajs, c(col.uniqID, col.time, col.whatokeep), with=FALSE]
  if(!is.null(out.file)) write.csv(dt, out.file, quote = FALSE, row.names = FALSE)
  else return(dt)
}