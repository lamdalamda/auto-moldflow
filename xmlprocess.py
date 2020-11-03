from xml.dom.minidom import parse
import csv
import itertools

class csv(object):#extract information from csv

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
        for i in range (0,len(self.attrdata["melt_temp"])):
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
    k=csv(filename)
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
    
'''
class tcode(object):#trail on building xml from initial.  Abandoned

    def __init__(self,father_node=0,codeid=10707,codevalue=[0,18900000,14,18900000],codename=None):

        tcode_node=domTree.createElement("TCode")

        id_node=domTree.createElement("ID")

        id_codeid=domTree.createTextNode(codeid)

        id_node.appendChild(id_codeid)

        tcode_node.appendChild(id_node)

        for i in codevalue:

            value_node=domTree.createElement("Value")

            Value_value=domTree.createElement(i)

            value_node.appendChild(Value_value)

            tcode_node.appendChild(value_node)

        father_node.appendChild(tcode_node)

    

    tcode reference

                <TCode>

                    <ID>10707</ID>

                    <Value>0</Value>

                    <Value>18900000</Value>

                    <Value>14</Value>

                    <Value>18900000</Value>

    '''   

class studymod(object):
    def __init__(self,xmlstudy=[],studyfile="crims.sdy",moldflowpath="C:\Program Files\Autodesk\Moldflow Insight 2019\\bin"):
        #xmlstudy=kxmlstudy     for alphatest
        super().__init__()
        self.xmls=xmlstudy
        self.studyfile=studyfile
        self.studymodpath='"'+moldflowpath+'\\studymod"'
    def generatebat(self):
        self.studymodbat=open("studymod.bat","w+")
        self.newstudys=[]
        for i in range(0,len(self.xmls)):
            self.studymodbat.write(self.studymodpath+" "+self.studyfile+" "+self.xmls[i]+".sdy "+self.xmls[i]+"\n")
            self.newstudys.append(self.xmls[i]+".sdy")
        self.studymodbat.close()

        return self.newstudys#所有产生的studyfile 的名字，列表格式
    
class runstudy(object):
    def __init__(self,studys=[],command=" -temp temp -keeptmp ",moldflowpath="C:\Program Files\Autodesk\Moldflow Insight 2019\\bin"):
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

    def __init__(self,studys=[],commanddict={" -result ":["6260"]," -node ":["128","124","27","23","126","79","74"]," -component ":["1","2"], " -unit metric":[" "]},moldflowpath="C:\Program Files\Autodesk\Moldflow Insight 2019\\bin"):
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
