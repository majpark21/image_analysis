library(tcltk)
library(data.table, quietly = TRUE)
library(ggplot2)

# Read Input
dat <- fread(input = "tCoursesSelected.csv")
dat <- dat[, .(Well, Image_Metadata_Site, objNuc_TrackObjects_Label, RealTime, objNuc_Intensity_MeanIntensity_imErkCorrOrig, objCyto_Intensity_MeanIntensity_imErkCorrOrig) ]
setnames(dat, c("Image_Metadata_Site", "objNuc_TrackObjects_Label", "objNuc_Intensity_MeanIntensity_imErkCorrOrig", "objCyto_Intensity_MeanIntensity_imErkCorrOrig"),
              c("Site", "Label", "Nuc_ERK", "Cyto_ERK"))
dat[, Ratio_ERK := Cyto_ERK / Nuc_ERK]





# Window definition
output <- c()

myWindow <- function(){
  win <- tktoplevel()
  tktitle(win) <- "Outlier buster"
  
  butOUT <- ttkbutton(win, text = "Outlier", width = -6,
                      command = function(){output <<- c(output, "Outlier"); tkdestroy(win)})
  butnotOUT<- ttkbutton(win, text = "NOT an Outlier", width = -6,
                        command = function(){output <<- c(output, "NOT Outlier"); tkdestroy(win)})
  butPREV<- ttkbutton(win, text = "Back to previous", width = -6,
                      command = function(){output <<- output[1:(length(output)-1)]; tkdestroy(win)})
  tkgrid(butOUT, butnotOUT, butPREV)
  tkwait.window(win)
}


for(i in 1:3){
  plot(i, main=as.character(i))
  Sys.sleep(1)
  myWindow()
}
