import os, subprocess, errno, re, random, datetime, json
from shutil import copyfile, rmtree

def main():
    print("\n\n\tHades Does Assignment Opensource Project by AIM\n\tCopyleft @ GPL-3.0\n\tABTZ, Inc.\n\n\t'Tis I, Hades, the ruler of the underworld!\n\tYour one last wish of completing your assignment wil be fulfilled!\n\tBut first, I need some details before we proceed!\n\n")

    mainfolder = os.getcwd()
    configfile = os.path.join(mainfolder,'config.json')
    modelsimdir = os.path.abspath(os.path.join(os.sep, 'opt', 'intelFPGA_pro','19.2'))
    settingsfile = os.path.join(modelsimdir, 'modelsim_ase', 'modelsim.ini')
    vsim = os.path.join(modelsimdir, 'modelsim_ase', 'linuxaloem', 'vsim')
    libraryfile = os.path.join(mainfolder, 'stuff', 'library.v')
    scaffoldfolder = os.path.join(mainfolder, 'stuff', 'scaffolds')
    craftfolder = os.path.join(mainfolder,'stuff','crafts')
    furnacefolder = os.path.join(mainfolder,'stuff', 'furnace')
    typocount = 0
    while True:
        if os.path.isfile(configfile):
            with open(configfile, 'r') as configjson:
                config = json.loads(configjson.read()) 
                firstname = config['firstname'].upper()
                rollno = config['rollno'].upper()
                assgno = config['assgno']
                print('Your Firstname: ' + firstname)
                print('Your Rollno: ' + rollno)
                print('Your Assignment no. : ' + assgno)
                correctdetails = input('\nAre these details correct? ').lower()
                if (correctdetails == 'yes' or correctdetails == 'y'):
                    break
                else:
                    print("\n\nPlease edit the config file and correct the errors...\n\nCall me when you're done correcting the errors...\n\nBye!\n")
                exit()
        else:
            firstname,rollno,assgno,correctdetails = inputdetails()
            if (correctdetails == 'yes' or correctdetails == 'y'):
                break
            elif typocount<1:
                print("\nTry typing them again...\n")
                typocount += 1
            elif typocount<2:
                print("\nArggh... There you've done it again...\n")
                typocount +=1
                exitchoice = input("Why don't you take a break a come back later? [Exit(yes/no)] : ").lower()
                if(exitchoice == 'yes' or exitchoice == 'y'):
                    exit()
                else:
                    print("\nI see you don't give up, do you? I'll give you one more chance...\n")
            else:
                print("\nArghhhhh...You've done it the third time... I'd suggest you to take rest and come back later...\n")
                exit()
    
    filestart = '_'.join([firstname, 'A'+str(assgno), 'P'])
    foldername = '_'.join([firstname, rollno,'ALL'])
    savefolder = os.path.join(craftfolder, foldername)
    catchphrase = r'@[a-zA-Z0-9\-]+'

    cleanfolder(craftfolder)
    cleanfolder(furnacefolder)

    with open(libraryfile, 'r') as library:
        bundle = library.read()
        scaffolds = os.listdir(scaffoldfolder)
        scaffolds.sort()
        for raw in scaffolds:
            filenameparts = re.findall(r'(\d+?)([a-z])(\.v)', raw)[0]
            with open(os.path.join(scaffoldfolder,raw), 'r') as mould:
                scaffold = setscaffold(scaffold,mould,catchphrase)
                deferror = 0
                for slot in slots:
                    checkpatch = re.search(slot+r'\n([\s\S]+?)(?:\n@|$)',bundle)
                    if checkpatch:
                        patch = checkpatch.group(1).strip()+'\n'
                        scaffold = scaffold.replace(slot+'\n', patch+'\n')
                    else:
                        deferror += 1
                        if(deferror==1):
                            print('\n'+filenameparts[0]+') ERROR!!! I found a few errors in the your code , please check it...\n')
                        print('** Hades: Error! Definition for '+slot+' not found!')
                if(deferror>0):
                    print('\nPlease correct the errors before I can complete the automation task...\n')
                    cleanchoice = input('\nClean up the furnace?(yes/no): ').lower()
                    if(cleanchoice == 'yes' or cleanchoice == 'y'):
                        cleanfolder(furnacefolder)
                    print("\n\nCall me when you're done correcting the errors...\n\nBye!\n")
                    exit()
                
                scaffold = scaffold.strip()

                buildfolder = os.path.join(furnacefolder,filestart+filenameparts[0])
                makefolder(buildfolder)
                os.chdir(buildfolder)
                projectname = filestart+filenameparts[0]
                if(filenameparts[1] == 'm'):
                    with open(projectname+filenameparts[2], 'w') as craft:
                        craft.write(scaffold)
                elif(filenameparts[1]=='s'):
                    with open(projectname+'_TB'+filenameparts[2],'w') as craft:
                        craft.write(scaffold)
                    output = subprocess.getoutput(" ".join([vsim, '-c', '-do', '"project new',re.sub(' ', r'\ ', buildfolder), projectname, 'work', settingsfile,';project open', os.path.join(re.sub(' ', r'\ ', buildfolder), projectname),';project addfile', projectname+filenameparts[2],';project addfile',projectname+'_TB'+filenameparts[2],';project compileall;vsim work.simulate; add wave -r /*; run; quit -sim; quit"']))
                    if('Error:' in output):
                        print(filenameparts[0]+') ERROR!!! I found a few errors in the your code , please check it...\n')
                        for line in output.splitlines():
                            if('Error:' in line):
                                print(line)
                        print('\nPlease correct the errors before I can complete the automation task...\n')
                        cleanchoice = input('\nClean up the furnace?(yes/no): ').lower()
                        if(cleanchoice == 'yes' or cleanchoice == 'y'):
                            cleanfolder(furnacefolder)
                        print("\n\nCall me when you're done correcting the errors...\n\nBye!\n")
                        exit()
                    else:
                        modulefile = os.path.join(buildfolder,projectname+filenameparts[2])
                        newmodulefile = os.path.join(savefolder, projectname+filenameparts[2])
                        simfile = os.path.join(buildfolder,projectname+'_TB'+filenameparts[2])
                        newsimfile = os.path.join(savefolder,projectname+'_TB'+filenameparts[2])
                        transcriptfile = os.path.join(buildfolder,'transcript')
                        with open(transcriptfile, 'r') as transcriptmod:
                            transcripttext = transcriptmod.read()
                            transcripttext = settranscripttext(transcripttext,filestart,filenameparts)
                            monitorcapture = re.search(r'run\n([\s\S]*)\nquit \-sim',transcripttext)
                            if monitorcapture:
                                monitorsting = monitorcapture.group(1)
                                print('\n\n'+filenameparts[0]+') Output from code '+':\n\n' + monitorsting)
                            else:
                                print('\n\n'+filenameparts[0]+') WARNING!!! No output recieved from code.''\n')
                        with open(transcriptfile, 'w') as transcriptmod:
                            transcriptmod.write(transcripttext)
                        newtranscriptfile = os.path.join(savefolder,'TRANSCRIPT_'+projectname)
                        os.chdir(mainfolder)
                        makefolder(savefolder)
                        copyfile(modulefile, newmodulefile)
                        copyfile(simfile, newsimfile)
                        copyfile(transcriptfile, newtranscriptfile)
    print("\nCHEERS! Your assignment has been completed successfully! :)\n\nPlease do check the output carefully to see if you've made any mistakes in the code!\n\nPeace Out!\n")
    cleanfolder(furnacefolder)

def inputdetails():
    firstname = input('Your Firstname : ').upper()
    rollno = input('Your Rollno : ').upper()
    assgno = input('Current Assignment no. : ')
    correctdetails = input('\nAre these details correct? ').lower()
    return firstname,rollno,assgno,correctdetails

def settranscripttext(transcripttext,filestart,filenameparts):
    transcripttext = re.sub(r'#\s+Loading project([\s\S]+?)\n','', transcripttext)
    transcripttext = re.sub(r'#\s+project new([\s\S]+?)\n','', transcripttext)
    transcripttext = re.sub(r'#\s+project open([\s\S]+?)\n','', transcripttext)
    transcripttext = re.sub(r'#\s+project add([\s\S]+?)\n','', transcripttext)
    transcripttext = re.sub(r'#\s+project compileall([\s\S]+?)#\s+simulate\n',' '.join(['# Compile of',filestart+filenameparts[0]+filenameparts[2],'was successful.\n'])+' '.join(['# Compile of',filestart+filenameparts[0]+'_TB'+filenameparts[2],'was successful.\n']), transcripttext)
    transcripttext = re.sub(r'#\s+add','add', transcripttext)
    transcripttext = re.sub(r'#\s+\*\*\s+Warning:(.)*\n','', transcripttext)
    transcripttext = re.subn(r'#\s+vsim','vsim', transcripttext,1)[0]
    starttime = datetime.datetime.strptime(re.search(r'Start time: (\d+\:\d+\:\d+)', transcripttext).group(1), '%H:%M:%S')
    deltatime = random.randint(60,120)
    endtime = starttime + datetime.timedelta(seconds=deltatime)
    elapsedtime = datetime.datetime.strptime('0:00:00', '%H:%M:%S') + datetime.timedelta(seconds=deltatime)
    transcripttext = re.sub(r'End time: (\d+\:\d+\:\d+)', 'End time: '+endtime.strftime('%H:%M:%S'), transcripttext)
    transcripttext = re.sub(r'(?:Elapsed time\: 0\:00\:)(\d+)', 'Elapsed time: '+ elapsedtime.strftime('%H:%M:%S'), transcripttext)
    transcripttext = re.sub(r'#\s+run','run', transcripttext)
    transcripttext = re.sub(r'#\s+quit \-sim','quit -sim', transcripttext)
    transcripttext = re.sub(r'\n#\s+quit\n','', transcripttext)

def setscaffold(scaffold,mould,catchphrase):
    scaffold = mould.read().strip()
    scaffold = scaffold + '\n'
    scaffold = re.sub(r'//.*(\n|$)?', '\n', scaffold)
    scaffold = re.sub(r'\n[^\S\r\n]+?\n', '\n', scaffold)
    slots = re.findall(catchphrase, scaffold)
    return scaffold

def makefolder(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def removefolder(directory):
    try:
        rmtree(directory)
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise

def cleanfolder(directory):
    removefolder(directory)
    makefolder(directory)

if __name__=='__main__':
    main()
