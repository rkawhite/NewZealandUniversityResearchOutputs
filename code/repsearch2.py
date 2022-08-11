#Open Access API Project
import requests
import re
import datetime
import time
import csv
import os
import codecs
import json

inf=input('Enter the name of the input file: ')
infilestring=str(inf)
print(infilestring)

if '.csv' not in infilestring.lower():
    infilestring=infilestring+'.csv'

#Locate the input file and quit if it is not found

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = "input/"+infilestring
abs_file_path = os.path.join(script_dir, rel_path)

doi_list=abs_file_path
print(doi_list)

try:
    filetest=open(doi_list)

except:
    print("File not found")
    
    quit()

repstring=input('Repository address, eg.g researchcommons.waikato.ac.nz: ')
#repstring='researchspace.auckland.ac.nz'

nowstart=datetime.datetime.now()
now1=str(nowstart)
now1=now1.replace(':','-')
now1=now1.replace(' ','-')
now1=now1[:16]


ofile=str(inf+'_'+now1+'.csv')

#Create path to output file in output folder

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
newdir="output/"+inf+'_'+now1
os.makedirs(newdir)

rel_path=newdir+"/"+ofile




abs_file_path3 = os.path.join(script_dir, rel_path)


of1=abs_file_path3


print(of1)


with open(of1, 'w', newline='',encoding='utf-8-sig') as outputfile:
    headings=['DOI','Full text in repository','Repository full record','Version','Link to full text']
    writer = csv.writer(outputfile)
    writer.writerow(headings)
    

    records=csv.DictReader(open(doi_list))

    for line in records:

        doi=line['DOI']
        print(doi)


        dspacefulltext='No'
        linkhandle=''
        citation=''
        version=''
        outlist=[]
        handleout=''




        searchstring='https://'+repstring+'/discover?query='+doi
        
        
        print(searchstring)
        findrep=requests.get(searchstring)
        


        repsearch1=findrep.content
        
        
        
        repsearch=str(repsearch1,encoding='utf-8')
        
            
            
        if 'href="/handle/' in repsearch:
            
            starthandle=repsearch.find('href="/handle/')+14
            
            endhandle=repsearch.find('"',starthandle)
            
            handle=repsearch[starthandle:endhandle]
            print(handle)

            
            
            
            gethandle='https://'+repstring+'/handle/'+handle+'?show=full'

            print(gethandle)

            

            findhandle=requests.get(gethandle)
            findhandle=findhandle.content
            
            
            
            handlesearch=str(findhandle,encoding='utf-8')
            
            
            
            
            
            
            
                    
                    
            if doi in handlesearch and '/bitstream/' in handlesearch and 'Full text for this item is not available' not in handlesearch:
                dspacefulltext='Yes'
                print(dspacefulltext)
                handleout=gethandle
                
                #if '/bitstream/handle/' in handlesearch or '/bitstream/'+handle in handlesearch:
                if '/bitstream/handle/' in handlesearch:
                    startcitation=handlesearch.find('/bitstream/handle/')
                    endcitation=handlesearch.find('"',startcitation)
                    citation='https://'+repstring+handlesearch[startcitation:endcitation]
                    print(citation)
                    
                    
                    
                    
                    print('/bitstream/handle/ in handlesearch')
                    
                    
                elif '/bitstream/' in handlesearch:
                    startcitation=handlesearch.find('/bitstream/')
                    endcitation=handlesearch.find('"',startcitation)
                    citation='https://'+repstring+handlesearch[startcitation:endcitation]
                    print(citation)  
                     
                    print('/bitstream/ in handlesearch')  
                        
                        
                        
                    


                if '>Description:<'in handlesearch:
                    descriptionposition=handlesearch.find('>Description:<')
                    startversion=handlesearch.find('" title="',descriptionposition)+9                   
                    endversion=handlesearch.find('"',startversion)
                    version=handlesearch[startversion:endversion]
                    
                else:
                    version='Not determined'

                print(version)
            else:
                dspacefulltext='No'
                print(dspacefulltext)
                version=''

        else:
            dspacefulltext='No'
            print(dspacefulltext)
            version=''

        outlist.append(doi);outlist.append(dspacefulltext);outlist.append(handleout);outlist.append(version);outlist.append(citation)
        print(outlist)
        writer.writerow(outlist)

        print()

                        

print('Finished!')