# TODO: check PREVIOUS button, add a quit button

library(tcltk)
suppressMessages(library(data.table))
library(ggplot2)

# Read Input
dt <- fread(input = "tCoursesSelected.csv")
dt <- dt[Well==4, .(Well, Image_Metadata_Site, objNuc_TrackObjects_Label,
                    RealTime, objNuc_Intensity_MeanIntensity_imErkCorrOrig,
                    objCyto_Intensity_MeanIntensity_imErkCorrOrig)]
setnames(dt, c("Image_Metadata_Site", "objNuc_TrackObjects_Label",
               "objNuc_Intensity_MeanIntensity_imErkCorrOrig",
               "objCyto_Intensity_MeanIntensity_imErkCorrOrig"),
             c("Site", "Label", "Nuc_ERK", "Cyto_ERK"))
dt[, uniqID := paste(Well, Site, Label, sep="_")]
dt[, Ratio_ERK := Cyto_ERK / Nuc_ERK]

whole.plot <- ggplot(dt, aes(x=RealTime, y=Ratio_ERK)) +
  geom_line(aes(group=Label)) +
  stat_summary(fun.y=mean, geom="line", colour = "blue", size = 1.5) + 
  theme_bw()

# outlier table
dt.out <- data.table(uniqID=unique(dt$uniqID), is.outlier = ".")


# Window definition
myWindow <- function(){
  win <- tktoplevel()
  tktitle(win) <- "Outlier buster"
  
  i <<- i
  butOUT <- ttkbutton(win, text = "Outlier", width = -6,
                      command = function(){set(dt.out, i, 2L, "yes"); tkdestroy(win)})
  butnotOUT<- ttkbutton(win, text = "NOT an Outlier", width = -6,
                      command = function(){set(dt.out, i, 2L, "no"); tkdestroy(win)})
  butPREV<- ttkbutton(win, text = "Back to previous", width = -6,
                      command = function(){output <<- output[1:(length(output)-1)]; tkdestroy(win)})
  tkgrid(butOUT, butnotOUT, butPREV)
  tkwait.window(win)
}


for(i in 1:nrow(dt.out)){
  plot(whole.plot +
    geom_line(data = dt[uniqID==dt.out[i, uniqID]], aes(x=RealTime, y=Ratio_ERK), col = 'red', size = 2))
  Sys.sleep(1)
  myWindow()
}
