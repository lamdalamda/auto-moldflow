import autoicm
import crims



pathdict={"moldflow":r"C:\Program files\Autodesk\Moldflow Insight 2019\bin\studymod","crimscsv":"LS2.csv","crimsxml":"IMxml.xml","icmxml":"2kicm.xml","icmcsv":"2kicmsetting.csv","crimssdy":"crims.sdy","2kicmsdy":"2kicm.sdy"}
#this is the relative path file
crims_files=["moldflow","crimscsv","crimsxml","crimssdy"]
k2icm_files=["moldflow","icmxml","2kicmsdy","icmcsv"]



class checktools(object):
    def __init__(self,pathdict,crims_files,k2icm_files) -> None:
        super().__init__()
        self.pathdict=pathdict
        self.files=[]
        self.exist_file=[]
        self.noexist_file=[]
        self.crims_files=crims_files
        self.k2icm_files=k2icm_files
        for i in self.pathdict:
            self.files.append(i)
    def checklist(self):
        #generate two lists:
        #existing and not existing
        #files: a list, containing files to check
        #example:["moldflow","crimscsv",""]
        self.exist_file=[]
        self.noexist_file=[]
        for i in self.files:
            if self.fileexist(self.pathdict[i]):
                self.exist_file.append(i)
            else:
                self.noexist_file.append(i)


    def fileexist(self,filepath):
        try:
            open(filepath,"r")
        except FileNotFoundError:
            return False
        else:
            return True

    def crims_ok(self):
        self.checklist()
        for i in self.crims_files:
            if i not in self.exist_file:
                return False
        return True
    def k2icm_ok(self):
        self.checklist()
        for i in self.k2icm_files:
            if i not in self.exist_file:
                return False
        return True

    def userchangepath(self,fileindex):
        self.pathdict[self.files[fileindex]]=input("please enter new path: ")


    def generate_ouput(self):
        print("\nnum# | file | filepath | exist?")
        for i in range(0,len(self.files)):
            print(i,self.files[i],self.pathdict[self.files[i]],self.fileexist(self.pathdict[self.files[i]]))
        if self.crims_ok():
            print("crims ready for analysis")
        if self.k2icm_ok():
            print("2kicm ready for auto-generate")
        user_input=input("input the number to change the path\ninput crims to generate IM studys\n input 2kicm to generate 2kicm parallel studys\ninput q to quit: ")
        #not finish yet
        #input 2kicm to do the 2kicm.py
        #input crims to do the crims.py
        if user_input=="2kicm":
            icmdict=autoicm.icmdict
            autoicm.betatest(self.pathdict["icmcsv"],icmdict,icmdict,self.pathdict["icmxml"])
            return False
        elif user_input=="crims":
            crims.alphatest(self.pathdict["crimscsv"],self.pathdict["crimsxml"])

            
            
            return False
        elif user_input=="q":
            return False
        else:
            self.userchangepath(int(user_input))
    def loop(self):
        continueloop=True
        while continueloop!=False:
            continueloop=self.generate_ouput()
        
        input("sequence: studymod.bat-->runstudy.bat-->studyrlt.bat\npress enter to exit")    
    



def alphatest():
    a=checktools(pathdict,crims_files,k2icm_files)
    a.loop()
if __name__=='__main__':

    alphatest()
