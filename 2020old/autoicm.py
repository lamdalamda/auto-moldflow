import itertools


class extractcsv(object):#extract information from csv

    def __init__(self,filename="1200hf.csv"):

        self.lines=open(filename,"r").readlines()

        self.attributes=self.lines[0].split(",")

        self.attributes[-1]=self.attributes[-1].replace("\n","")

        self.datalines=self.lines[1:]

        self.listdata=[]

        self.attrdata={}

        self.columns=len(self.attributes) #列数，即attribute数量
       

        for i in self.attributes:

            self.attrdata[i]=[]

        for i in self.datalines:

            thisline=[]

            ii=i.split(",")

            for j in range(0,len(ii)):

                thisline.append(ii[j].replace("\n",""))

                self.attrdata[self.attributes[j]].append(ii[j])

            self.listdata.append(thisline)

        self.rows=len(self.listdata)#抛去第一行的行数


    def debug(self):

        print(self.attrdata)

        print(self.listdata)

        input("debug")
   
    def createdummy(self,dummyname="dummy",value="0"):
        self.attrdata[dummyname]=[]
        for i in range (0,self.rows):
            self.attrdata[dummyname].append(value)


        #debug pass 20201027

    def generate_dicts(self,subtractlist=["melt_temp","mold_temp","flow_rate_r","dummy","pack_press","pack_time","pack_press","cool_time"],totheattrlist=["melt_temperature","mold_temperature","flow_rate","pack_start","pack_initial_pressure","pack_stop","pack_end_pressure","cool_time"]):#build the dictionary list from csv. 由subtractlist产生toheattrlist
       
        self.generatedDicts=[]
        for i in range (0,len(self.attrdata[subtractlist[0]])):
            l={}
            for j in range(0,len(subtractlist)):
                l[totheattrlist[j]]=self.attrdata[subtractlist[j]][i].replace("\n","")
            self.generatedDicts.append(l)
       
        #print(generatedDicts)#debug pass

example_replace_dictionary_IM={"melt_temperature":1,"mold_temperature":2,"flow_rate":3,"pack_start":4,"pack_initial_pressure":5,"pack_stop":6,"pack_end_pressure":7,"cool_time":8}

class changexml(object):

    def __init__(self,filenamepre="1",filename="IMxml.xml",studyname="IMxml.xml",replace_dict=example_replace_dictionary_IM):

        self.lines=open(filename,"r").readlines()
        self.newxml=open(str(filenamepre)+studyname,"w+")
        for i in self.lines:

            for j in replace_dict:

                if j in i:

                    i=i.replace(j,str(replace_dict[j]))
                    print(i)
            self.newxml.write(i)



def alphatest(filename="1200hf.csv"): #alphatest for 1200hf.csv Pass   
    #alphatest workflow       
    k=extractcsv(filename)
    k.createdummy()
    subtractlist=["melt_temp","mold_temp","flow_rate_r","dummy","pack_press","pack_time","pack_press","cool_time"]
    totheattrlist=["melt_temperature","mold_temperature","flow_rate","pack_start","pack_initial_pressure","pack_stop","pack_end_pressure","cool_time"]

    k.generate_dicts(subtractlist,totheattrlist)

    kxmllist=[]

    for i in range (0,len(k.generatedDicts)):
        h=changexml(i,"IMxml.xml",filename+".xml",k.generatedDicts[i])
        kxmllist.append(str(i)+filename+".xml")
    m=studymod(kxmllist)
    studys=m.generatebat()

    r=runstudy(studys)
    r.generatebat()
    g=studyrlt(studys)
    g.generatecommands()
    g.generatebat()

def betatest(filename="2kicmsetting.csv",subtractlist=["melt_temp","mold_temp","flow_rate_r","dummy","pack_press","pack_time","pack_press","cool_time"],totheattrlist=["melt_temperature","mold_temperature","flow_rate","pack_start","pack_initial_pressure","pack_stop","pack_end_pressure","cool_time"],xmlfilename="2kicm.xml"): #betatest for 2kicmsetting   
    #alphatest workflow       
    k=extractcsv(filename)

    k.generate_dicts(subtractlist,totheattrlist)

    kxmllist=[]

    for i in range (0,len(k.generatedDicts)):
        h=changexml(i,xmlfilename,filename+".xml",k.generatedDicts[i])
        kxmllist.append(str(i)+filename+".xml")
    m=studymod(kxmllist,"2kicm.sdy")
    studys=m.generatebat()

    r=runstudy(studys)
    r.generatebat()
    g=studyrlt(studys)
    g.generatecommands()
    g.generatebat()



class studymod(object):
    def __init__(self,xmlstudy=[],studyfile="crims.sdy",moldflowpath=r"C:\Program Files\Autodesk\Moldflow Synergy 2019\bin"):
        #xmlstudy=kxmlstudy     for alphatest
        super().__init__()
        self.xmls=xmlstudy
        self.studyfile=studyfile
        self.studymodpath='"'+moldflowpath+'\\studymod"'
    def generatebat(self):
        self.studymodbat=open("studymod.bat","w+")
        self.newstudys=[]
        for i in range(0,len(self.xmls)):
            self.studymodbat.write(self.studymodpath+" "+self.studyfile+" "+self.xmls[i].replace(".","")+".sdy "+self.xmls[i]+"\n")
            self.newstudys.append(self.xmls[i].replace(".","")+".sdy")
        self.studymodbat.close()

        return self.newstudys#所有产生的studyfile 的名字，列表格式
    
class runstudy(object):
    def __init__(self,studys=[],command=" -temp temp -keeptmp ",moldflowpath=r"C:\Program Files\Autodesk\Moldflow Insight 2019\bin"):
        #studys=studymod.newstudys  for alphatest
        super().__init__()
        self.studys=studys
        self.commands=command
        self.runstudypath='"'+moldflowpath+'\\runstudy"'
    def generatebat(self):
        self.runstudybat=open("runstudy.bat","w+")
        #self.newstudys=[]
        for i in range(0,len(self.studys)):
            self.runstudybat.write(self.runstudypath+self.commands+self.studys[i]+"\n")
            #self.newstudys.append(self.xmls[i]+".sdy")
        self.runstudybat.close()

        #return self.newstudys#所有产生的studyfile 的名字，列表格式
    

class resultcommands(object):
    def __init__(self,commanddict={" -result ":["6260"]," -node ":["128","124","27","23","126","79","74"]," -component ":["1","2"], " -unit metric":[" "]}):
        self.cdict={}
        for i in commanddict:
            self.cdict[i]=[]
            for j in commanddict[i]:
                self.cdict[i].append(i+j)
        self.clist=[]
        for i in self.cdict:
            self.clist.append(self.cdict[i])
        self.commands=list(itertools.product(*tuple(self.clist)))
        self.strcommands=[]
        for i in self.commands:
            self.strcommands.append("".join(i))
        


class studyrlt(object):#under construct

    def __init__(self,studys=[],commanddict={" -result ":["6260"]," -node ":["128","124","27","23","126","79","74"]," -component ":["1","2"], " -unit metric":[" "]},moldflowpath=r"C:\Program Files\Autodesk\Moldflow Insight 2019\bin"):
        #studys=studymod.newstudys  for alphatest
        super().__init__()
        self.studys=studys
        #self.commands=command
        self.studyrltpath='"'+moldflowpath+'\\studyrlt" '
        self.commanddict=commanddict
    def generatecommands(self):
        self.cdict={}
        for i in self.commanddict:
            self.cdict[i]=[]
            for j in self.commanddict[i]:
                self.cdict[i].append(i+j)
        self.clist=[]
        for i in self.cdict:
            self.clist.append(self.cdict[i])
        self.commands=list(itertools.product(*tuple(self.clist)))
        self.strcommands=[]
        for i in self.commands:
            self.strcommands.append("".join(i))
        return self.strcommands
    
    def generatebat(self):
        self.studyrltbat=open("studyrlt.bat","w+")
        #self.newstudys=[]
        for i in range(0,len(self.strcommands)):
            for j in self.studys:
                self.studyrltbat.write(self.studyrltpath+j+self.strcommands[i]+"\nrename "+j[:-3]+'val '+j+self.strcommands[i].replace(" ","")+'.val\n')

            #self.newstudys.append(self.xmls[i]+".sdy")
        self.studyrltbat.close()
#    with open



icmdict=["icm_mold_temp","icm_melt_temp","icm_injection_time","icm_vp_switchover","icm_pack_start","icm_pack_initial_pressure","icm_pack_stop","icm_pack_end_pressure","icm_cool_time","im_mold_temp","im_melt_temp","im_injection_time","im_vp_switchover","im_pack_start","im_pack_initial_pressure","im_pack_stop","im_pack_end_pressure","im_cool_time","press_open","compression_start","compression_time","speed_cap","one_compression_distance","one_compression_speed","two_compression_distance","two_compression_speed","force_cap"]

def workflow():
    a=betatest("2kicmsetting.csv",icmdict,icmdict,"2kicm.xml")
if __name__=='__main__':

    workflow()


#input the combination of process settings in the 2kicmsetting.csv and run this program to generate bat file and sdy file
#dont need to run the studyrlt.bat