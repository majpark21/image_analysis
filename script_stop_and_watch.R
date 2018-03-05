#rm(list=ls())
# Path to file to read
filetoread = "mod_tCoursesSelected.csv"
col.uniqID = "myID"
col.time = "RealTime"
col.whatoplot = c("objNuc_Intensity_MeanIntensity_imNucCorrBg", "objCell_AreaShape_Area", "objCell_AreaShape_EulerNumber")

# At which trajectory to start, useul if you stopped in the middle of a dataset and want to 
# come back to it
i <- 1L
# Increase if GUI appears before the plot
sleep.time <- 0.75
# Number of trajectories to plot (selected at random, lower to speed up plotting)
in.ntraj <- 20


# ----------------------------

library(tcltk)
suppressMessages(library(data.table))
library(ggplot2)
# Read Input
dt <- fread(input = filetoread)
# Chop unuse columns for memor efficiency and melt on features to plot
col.tokeep <- c(col.uniqID, col.time, col.whatoplot)
dt <- dt[, col.tokeep, with=FALSE]
dt <- melt(dt, measure.vars = col.whatoplot)

# Select some random trajectories to always plot
traj.to.plot <- sample(unlist(unique(dt[, col.uniqID, with=FALSE])), in.ntraj, FALSE)
whole.plot <- ggplot(dt[get(col.uniqID) %in% traj.to.plot], aes(x=get(col.time), y=value)) +
  geom_line(aes_string(group=col.uniqID)) +
  stat_summary(fun.y=mean, geom="line", colour = "blue", size = 1.5) + 
  facet_wrap(~variable, scales = "free") +
  theme_bw()

# outlier table
dt.out <- data.table(unique(dt[, col.uniqID, with=FALSE]), is.outlier = ".")


# Window definition
myWindow <- function(){
  win <- tktoplevel()
  tktitle(win) <- "Outlier buster"
  
  i <<- i
  butOUT <- ttkbutton(win, text = "Outlier", width = -6,
                      command = function(){set(dt.out, i, 2L, "yes"); tkdestroy(win)})
  butnotOUT<- ttkbutton(win, text = "NOT an Outlier", width = -6,
                        command = function(){set(dt.out, i, 2L, "no"); tkdestroy(win)})
  # -2 since the while loop is -1
  butPREV<- ttkbutton(win, text = "Back to previous", width = -6,
                      command = function(){i <<- i-2L ; tkdestroy(win)})
  butSAVEQUIT <- ttkbutton(win, text = "Save and quit", width = -6,
                           command = function(){
                             filename <- tclvalue(tkgetSaveFile())
                             if (!nchar(filename)) {
                               tkmessageBox(message = "No file was selected!")
                             } else {
                               tkmessageBox(message = paste("The file selected was", filename))
                             }
                             write.csv(x = dt.out, file = paste0(filename, ".csv"), quote = FALSE)
                             tkdestroy(win)
                             stoploop <<- TRUE
                           })
  tkgrid(butOUT, butnotOUT, butPREV, butSAVEQUIT)
  tkwait.window(win)
}

endWindow <- function(){
  win <- tktoplevel()
  tktitle(win) <- "You have reached the end of the file, now save your data by pressing the button."
  butSAVEQUIT <- ttkbutton(win, text = "Save and quit", width = -24,
                           command = function(){
                             filename <- tclvalue(tkgetSaveFile())
                             if (!nchar(filename)) {
                               tkmessageBox(message = "No file was selected!")
                             } else {
                               tkmessageBox(message = paste("The file selected was", filename))
                             }
                             write.csv(x = dt.out, file = paste0(filename, ".csv"), quote = FALSE)
                             tkdestroy(win)
                           })
  tkgrid(butSAVEQUIT)
  tkwait.window(win)
}


stoploop <- FALSE
#while(i <= nrow(dt.out)){
while(i <= 3L){
  print(i)
  plot(whole.plot +
         geom_line(data = dt[get(col.uniqID)==dt.out[i, get(col.uniqID)]], aes(x=get(col.time), y=value), col = 'red', size = 2))
  Sys.sleep(sleep.time)
  myWindow()
  if(stoploop) break
  i <- i + 1L
}

# if script didn't stop because of pressing "save and quit"
if(!stoploop){
  endWindow()
}
