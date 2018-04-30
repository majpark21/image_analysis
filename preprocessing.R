# 1) Select only full trajectories
# 2) Impute missing data
# 3) Save one table for each condition with a random subset of trajectories

library(data.table)
library(imputeTS)

#dt_whole <- fread("../data/paolo/objNuclei_clean_tracks.csv")
#dt_whole[, uniqID := paste(Image_Metadata_Well, Image_Metadata_Site, track_id, sep="_")]
# Vector with complete tracks ID
#v.tracks <- dt_whole[,.N, by=uniqID][N==max(N), uniqID]
#write.csv(x = dt_whole[uniqID %in% v.tracks], file = "../data/paolo/complete_objNuclei_clean_tracks.csv",  quote = F, row.names = F)

# Impute missing values
dt_whole <- fread("../data/paolo/complete_objNuclei_clean_tracks.csv")
for(col in colnames(dt_whole)[6:13]){
  set(dt_whole, j=col, value = na.interpolation(dt_whole[[col]]))
}

# Save a table for each condition with 40 random trajectories
i <- 1
for(cond in unique(dt_whole$condAll)){
  select_random_save(in.file = dt_whole[condAll==cond], ntraj = 40, col.uniqID = "uniqID", col.time = "Image_Metadata_T", col.whatokeep = colnames(dt_whole)[-c(3,14)], out.file = paste0("../data/paolo/sub40/condition", i, ".csv"))
  i <- i+1
}
rm(i, cond)

#c1 <- fread("sub100/condition1.csv")
