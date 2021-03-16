
# Retrieve the following matlab scripts, store in the working directory
	# CuiXuFindStructure.m
	# ft_hastoolbox.m
	# tal2mni.m

library(label4MRI) # https://github.com/yunshiuan/label4MR
library(matlabr)   # https://cran.r-project.org/web/packages/matlabr/matlabr.pdf
options(matlab.path = "[redacted]/MATLAB/R2020b/bin/matlab.exe") # your MATLAB exe/app path

tal2label <- function(x, y, z){
  date<-format(Sys.Date(), format="%m%d")     # Uses date in a temporary txt file
  code<-paste0("x=",x,";y=",y,";z=",z)        # Write matlab code, Set X Y Z
  code<-paste0(code,"; a=tal2mni([x,y,z]);",  # Add code Run tal2mni coordinates, save as txt file
            "save('_temp_",date,".txt', 'a', '-ascii')")
  run_matlab_code(code)                       # Run matlab code
  temp<-read.delim(paste0("_temp_",date,".txt"), header = FALSE, sep = " ")[1,] 
  temp<-temp[!is.na(temp)]                    # retrieve results, remove spaces, which loaded as NA
  return(mni_to_region_name(temp[1],temp[2],temp[3])$aal.label) # Get label
	# see label4MRI documentation for other options (e.g., BA label)
}

tal2label(-46,31,-10)
