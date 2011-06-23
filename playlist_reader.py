# playlist_reader.py
# Processes .pls file and outputs a list
# Copyright (C) 2011 Rajat Saxena
#
# rajat.saxena.work@gmail.com
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class reader:
    def __init__(self,filename):
        with open(filename,"r") as f:
            line=f.readline().strip()
            #print(line)
            if line!="[playlist]":
                print("Not a valid playlist file")
            else:
                print("Processing file...")
                tempdict={}
                self.mediafiles=[]
                line=f.readline().strip()
                tempdata=line.split("=")
                tempdict[tempdata[0]]=tempdata[1]
                print(tempdict)
                print("Adding Media Files...")
                count=0
                print(str(int(tempdict['NumberOfEntries'])))
                for line in f:
                    line=line.strip()
                    print(line)
                    if line[:4]!="File":
                        pass
                    else:
                        tempdata=line.split("=")
                        self.mediafiles.append(tempdata[1])
                        count=count+1

    def returner(self):
        return self.mediafiles

if __name__=="__main__":
    a=reader("/home/rajat/test.pls")
    listy=a.returner()
    print("Number of entries: "+str(len(listy)))
    print(listy)
                


