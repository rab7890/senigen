import glob
import os


#Chromosome, Complete_Genome, Contig, Scaffold


#Down Summary#
import sys
from pathlib import Path

from dbcontroller import DBController

full_path = os.path.realpath(__file__)
current = os.path.dirname(full_path)
current = str(Path(current).resolve().parent)
MEDIAPATH = current + '/media'
DOWNPATH = current + '/media/Down'

def Summary_down(dbc):
    dbc.set_status_log("start download summary file.")
    if not os.path.isdir(DOWNPATH):
        os.mkdir(DOWNPATH)
    os.chdir(DOWNPATH)
    systemstr = "wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt"
    os.system(systemstr)
    os.chdir(MEDIAPATH)


#Wget File Generate#
def Down_file_gen(Level, dbc):
    os.chdir(DOWNPATH)

    ck = open(DOWNPATH + "/assembly_summary.txt", 'r')
    total = len(ck.readlines()) - 2
    ck.close()

    fin = open(DOWNPATH + "/assembly_summary.txt", 'r')
    Header = fin.readline()
    Header = fin.readline()
    fout = open(DOWNPATH + "/genomic_file", 'w')
    dbc.set_status_log('start Down_file_gen.')
    cnt = 0
    for line in fin:
        linetemp = line.strip().split("\t")
        if linetemp[19].startswith("ftp") and linetemp[20] == "" and linetemp[13] == "Full":
            if Level == "Contig":
                address = linetemp[19] + "/" + linetemp[19].split("/")[-1] + "_genomic.fna.gz"
                if linetemp[4] == "representative genome" or linetemp[4] == "reference genome":
                    fout.write(address + "\t" + linetemp[7].replace(" ", "_") + "\n")
                else:
                    fout.write(address + "\n")
            if Level == "Scaffold":
                if linetemp[11] == "Contig":
                    continue
                else:
                    address = linetemp[19] + "/" + linetemp[19].split("/")[-1] + "_genomic.fna.gz"
                    if linetemp[4] == "representative genome" or linetemp[4] == "reference genome":
                        fout.write(address + "\t" + linetemp[7].replace(" ", "_") + "\n")
                    else:
                        fout.write(address + "\n")
            if Level == "Chromosome":
                if linetemp[11] == "Contig" or linetemp[11] == "Scaffold":
                    continue
                else:
                    address = linetemp[19] + "/" + linetemp[19].split("/")[-1] + "_genomic.fna.gz"
                    if linetemp[4] == "representative genome" or linetemp[4] == "reference genome":
                        fout.write(address + "\t" + linetemp[7].replace(" ", "_") + "\n")
                    else:
                        fout.write(address + "\n")
            if Level == "Complete_Genome":
                if linetemp[11] == "Complete Genome":
                    address = linetemp[19] + "/" + linetemp[19].split("/")[-1] + "_genomic.fna.gz"
                    if linetemp[4] == "representative genome" or linetemp[4] == "reference genome":
                        fout.write(address + "\t" + linetemp[7].replace(" ", "_") + "\n")
                    else:
                        fout.write(address + "\n")
        dbc.set_status_log("Down_file_gen {}/{} 진행 중 ".format(cnt, total))
        cnt += 1
        #print("Level - {}".format(Level))
        dbc.set_process(cnt, total)
    dbc.set_status_log('finish Down_file_gen.')
    systemstr = "rm assembly_summary.txt"
    os.system(systemstr)
    fout.close()
    fin.close()
    os.chdir("../")


#Wget File#
def Wget(dbc):
    os.chdir(DOWNPATH)

    ck = open(DOWNPATH + "/genomic_file", 'r')
    total = len(ck.readlines())
    ck.close()

    fin = open(DOWNPATH + "/genomic_file", 'r')
    fout = open(DOWNPATH + "/down_history", 'w')
    if not os.path.isdir("./Downloaded"):
        os.mkdir("./Downloaded")
    if not os.path.isdir("./Representative"):
        os.mkdir("./Representative")
    os.chdir("./Downloaded")
    dbc.set_status_log('start web get genomic_file.')
    cnt = 0
    for line in fin:
        linetemp = line.strip().split("\t")
        file_name = linetemp[0].split("/")[-1]
        while not os.path.isfile("./" + file_name.replace(".gz", "")):
            systemstr = "wget " + linetemp[0]
            os.system(systemstr)
            systemstr = "gzip -d " + file_name
            os.system(systemstr)
            if os.path.isfile("./" + file_name):
                systemstr = "rm " + file_name
                os.system(systemstr)
        fout.write(line)
        fout.flush()
        if len(linetemp) == 2:
            systemstr = "cp " + file_name.replace(".gz", "") + " ../Representative/" + linetemp[1] + ".fna"
            os.system(systemstr)
        cnt += 1
        dbc.set_status_log("Wget {}/{} 진행 중 ".format(cnt, total))
        dbc.set_process(cnt, total)
    dbc.set_status_log('finish web get genomic_file.')
    os.chdir(MEDIAPATH)


#Representative BWA-MEM2 Indexing
def BWA_MEM2_Indexing (dbc):
    dbc.set_status_log('start BWA_MEM2_Indexing')
    os.chdir(MEDIAPATH + "/Down/Representative")
    file_list = glob.glob("./*.fna")
    for file_name in file_list:
        systemstr = "bwa-mem2 index -p "+os.path.basename(file_name).replace(".fna", "") + " " + file_name
        os.system(systemstr)
    os.system(systemstr)
    dbc.set_status_log('finish BWA_MEM2_Indexing')


#Compare_list#
def Compare(dbc):
    os.chdir(DOWNPATH)
    old_list = []
    fin = open(DOWNPATH + "/down_history", 'r')
    dbc.set_status_log('start compare.')
    for line in fin:
        linetemp = line.strip()
        old_list.append(linetemp)
    Old = set(old_list)
    fin.close()
    new_list = []
    fin = open(DOWNPATH + "/genomic_file", 'r')
    for line in fin:
        linetemp = line.strip()
        new_list.append(linetemp)
    New = set(new_list)
    Update = New-Old
    fin.close()
    fout = open("update_file", 'w')
    for line in Update:
        fout.write(line+"\n")
        fout.flush()
    fout.close()
    dbc.set_status_log('finish compare.')
    os.chdir("../")

#Updated_list Download#
def Wget_update (dbc) :
    os.chdir(DOWNPATH)

    ck = open(DOWNPATH + "/update_file", 'r')
    total = len(ck.readlines())
    ck.close()

    fin = open(DOWNPATH + "/update_file", 'r')
    fout = open(DOWNPATH + "/down_history", 'a')
    if not os.path.isdir("./Update"):
        os.mkdir("./Update")
    os.chdir("./Update")
    dbc.set_status_log('start web get update.')
    cnt = 0
    for line in fin:
        linetemp = line.strip()
        file_name = linetemp.split("/")[-1]
        while not os.path.isfile("./"+file_name.replace(".gz", "")):
            systemstr = "wget "+linetemp
            os.system(systemstr)
            systemstr = "gzip -d "+file_name
            os.system(systemstr)
            if os.path.isfile("./"+file_name):
                systemstr = "rm "+file_name
                os.system(systemstr)
        fout.write(line)
        fout.flush()
        cnt += 1
        dbc.set_status_log("Wget_update {}/{} 진행 중 ".format(cnt, total))
        dbc.set_process(cnt, total)
    dbc.set_status_log('finish web get update.')
    os.chdir(MEDIAPATH)



if __name__ == '__main__':
    try:
        ########## MAIN #############
        Level = sys.argv[1]
        full_path = os.path.realpath(__file__)
        current = os.path.dirname(full_path)
        current = str(Path(current).resolve().parent)
        dbc = DBController(current + '/db.sqlite3', 'GENOME')
        dbc.set_running()
        if not os.path.isfile(DOWNPATH + "/down_history"):
            Summary_down(dbc)
            Down_file_gen(Level, dbc)
            Wget(dbc)
            BWA_MEM2_Indexing(dbc)
        else:
            Summary_down(dbc)
            Down_file_gen(Level, dbc)
            Compare(dbc)
            Wget_update(dbc)

        dbc.set_idle()
    except Exception as e:
        #dbc.set_genome_status_log('error : {}'.format(str(e)))
        dbc.set_main_error(str(e))
        dbc.set_idle()