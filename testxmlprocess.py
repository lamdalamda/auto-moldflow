from xmlprocess import *

#alphatest("1300.csv")

#a="C:\Program Files\Autodesk\Moldflow Synergy 2019\\bin"
#print(a)
#a=resultcommands()
#print(tuple(a.clist))
#print(list(itertools.product(*a.clist)))
#print(a.cdict)
#print(a.strcommands)

icmdict=["icm_mold_temp","icm_melt_temp","icm_injection_time","icm_vp_switchover","icm_pack_start","icm_pack_initial_pressure","icm_pack_stop","icm_pack_end_pressure","icm_cool_time","im_mold_temp","im_melt_temp","im_injection_time","im_vp_switchover","im_pack_start","im_pack_initial_pressure","im_pack_stop","im_pack_end_pressure","im_cool_time","press_open","compression_start","compression_time","speed_cap","one_compression_distance","one_compression_speed","two_compression_distance","two_compression_speed","force_cap"]

def workflow():
    a=betatest("2kicmsetting.csv",icmdict,icmdict)