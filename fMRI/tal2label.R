
# Retrieve the following matlab scrips, store in this directory
	# CuiXuFindStructure.m
	# ft_hastoolbox.m
	# tal2mni.m

library(label4MRI)
library(matlabr)
options(matlab.path = "[redacted]/MATLAB/R2020b/bin/matlab.exe")

tal2label <- function(x, y, z){
  date<-format(Sys.Date(), format="%m%d")
  code<-paste0("x=",x,";y=",y,";z=",z)
  code<-paste0(code,"; a=tal2mni([x,y,z]);",
            "save('_temp_",date,".txt', 'a', '-ascii')")
  run_matlab_code(code)
  temp<-read.delim(paste0("_temp_",date,".txt"), header = FALSE, sep = " ")[1,]
  temp<-temp[!is.na(temp)]
  return(mni_to_region_name(temp[1],temp[2],temp[3])$aal.label)
}

tal2label(-46,31,-10)
