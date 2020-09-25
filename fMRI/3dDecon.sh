# @Author: christopherbrozdowski
# @Date:   2016-10-04 15:42:38
# @Last Modified by:   christopherbrozdowski
# @Last Modified time: 2016-10-11 16:23:29

#NOTE: polort now 1

set SchNum = $argv[1]
#set SchNum = '01'
 
3dDeconvolve                              				 \
-nodata 720 1                                            \
-polort 1                                              \
-num_stimts 4                                            \
-stim_times 1 stimes_8sResp_sched-0${SchNum}_Proj.1D GAM \
-stim_label 1 Proj                                       \
-stim_times 2 stimes_8sResp_sched-0${SchNum}_Topo.1D GAM \
-stim_label 2 Topo                                       \
-stim_times 3 stimes_8sResp_sched-0${SchNum}_Ctrl.1D GAM \
-stim_label 3 Ctrl                                       \
-stim_times 4 stimes_8sResp_sched-0${SchNum}_Resp.1D GAM \
-stim_label 4 Resp                                       \
-x1D Sched-0${SchNum}                                    \
> 3dDecon_Output_Sched-0${SchNum}
