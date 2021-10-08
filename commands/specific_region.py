import sys, glob, os
import traceback

from pathlib import Path
from Bio import SeqIO
from Bio.SeqUtils import GC

#Code Argument
from dbcontroller import DBController

full_path = os.path.realpath(__file__)
current = os.path.dirname(full_path)
current = str(Path(current).resolve().parent)
GTDBTKPATH = current + '/media/GTDBTK'
MEDIAPATH = current + '/media'
SPECIFICPATH = current + '/media/Specific'



#Identify specific kmer in Genus
def Specific_in_genus(dbc):
    dbc.set_status_log("start species_file_list")
    if not os.path.isdir(SPECIFICPATH):
        os.mkdir(SPECIFICPATH)
    os.chdir(SPECIFICPATH)

    species_file_list = glob.glob(GTDBTKPATH + "/reassigned/"+Genus+"/"+Species+"/*.fna")
    print("species_file_list")
    print(species_file_list)
    total = len(species_file_list)
    in_genus = os.listdir(GTDBTKPATH + "/reassigned/" + Genus)
    genus_target_folder = set(in_genus) - set([Species])
    except_list = []
    for target_folder in genus_target_folder:
        except_list += glob.glob(GTDBTKPATH + "/reassigned/"+Genus+"/"+target_folder+"/*.fna")
    print("except_list")
    print(except_list)
    fout = open(SPECIFICPATH + "/Uniq.txt", 'w')
    #fout2=open("log.txt",'w')

    sub_1 = []
    sub_2 = []
    other = []
    FLAG = 1
    CNT_uniq = 1

    cnt = 0
    for file_name in species_file_list:
        if FLAG == 1:
            FLAG += 1
            fin = open(file_name, 'r')
            for sequence in SeqIO.parse(fin, 'fasta'):
                num_kmers = len(str(sequence.seq)) - int(k_length) + 1
                forward = str(sequence.seq)
                reverse = str(sequence.seq.reverse_complement())
                for i in range(num_kmers):
                    kmer = forward[i:i + int(k_length)]
                    sub_1.append(kmer)
                    kmer_r = reverse[i:i + int(k_length)]
                    sub_1.append(kmer_r)
            sub_1 = list(set(sub_1))
            #fout2.write(str(len(sub_1))+"\n")
            #fout2.flush()
            print(file_name+":"+str(len(sub_1)))
            fin.close()
        else:
            fin = open(file_name, 'r')
            for sequence in SeqIO.parse(fin, 'fasta'):
                num_kmers=len(str(sequence.seq)) - int(k_length) + 1
                forward = str(sequence.seq)
                reverse = str(sequence.seq.reverse_complement())
                for i in range(num_kmers):
                    kmer = forward[i:i + int(k_length)]
                    sub_2.append(kmer)
                    kmer_r = reverse[i:i + int(k_length)]
                    sub_2.append(kmer_r)
            sub_2 = list(set(sub_2))
            sub_1 = set(sub_1) & set(sub_2)
            #fout2.write(str(len(sub_1))+"\n")
            #fout2.flush()
            sub_2 = []
            print(file_name+":"+str(len(sub_1)))
            fin.close()
        dbc.set_status_log("Specific_in_genus {}/{} 진행 중 ".format(cnt, total))
        cnt += 1
        dbc.set_process(cnt, total)
    Common = sub_1
    dbc.set_status_log("start except_list")
    total = len(except_list)
    cnt = 0
    for file_name in except_list:
        #fout2.write(file_name+"\n")
        #fout2.flush()
        fin = open(file_name, 'r')
        for sequence in SeqIO.parse(fin, 'fasta'):
            num_kmers = len(str(sequence.seq)) - int(k_length) + 1
            forward = str(sequence.seq)
            reverse = str(sequence.seq.reverse_complement())
            for i in range(num_kmers):
                kmer = forward[i:i + int(k_length)]
                other.append(kmer)
                kmer_r = reverse[i:i + int(k_length)]
                other.append(kmer_r)
        fin.close()
        Common = set(Common)-set(other)
        print(len(Common))
        #fout2.write(str(len(Unique))+"\n")
        #fout2.flush()
        other = []
        dbc.set_status_log("Specific_in_genus except_list {}/{} 진행 중 ".format(cnt, total))
        cnt += 1
        dbc.set_process(cnt, total)

    dbc.set_status_log("start write kmer")
    cnt = 0
    #print("Common")
    #print(Common)
    total = len(Common)
    for kmer in Common:
        fout.write(">"+Species+"_"+str(CNT_uniq)+"\n")
        CNT_uniq += 1
        fout.write(kmer+"\n")
        #dbc.set_status_log("Specific_in_genus kmer {}/{} 진행 중 ".format(cnt, total))
        cnt += 1
        #dbc.set_process(cnt, total)
    fout.close()
    dbc.set_status_log("finish write kmer")


# Specificity test to all
def Mapping(dbc):
    dbc.set_status_log("start mapping")
    os.chdir(SPECIFICPATH)

    rep_list = glob.glob(MEDIAPATH + "/Down/Representative/*.fna")
    total = len(rep_list)
    cnt = 0
    for rep_name in rep_list:
        if Genus in rep_name:
            continue
        else:
            systemstr = "bwa-mem2 mem -t 16 "+rep_name.replace(".fna", "")+" Uniq.txt | samtools sort -o aln.bam -"
            os.system(systemstr)
            systemstr = "samtools view -bf 0x04 aln.bam > unmapped.bam"
            os.system(systemstr)
            systemstr = "samtools bam2fq unmapped.bam > Uniq.txt"
            os.system(systemstr)
            systemstr = "seqtk seq -A Uniq.txt > temp.fa"
            os.system(systemstr)
            systemstr = "mv temp.fa Uniq.txt"
            os.system(systemstr)
        dbc.set_status_log("Mapping {}/{} 진행 중 ".format(cnt, total))
        cnt += 1
        dbc.set_process(cnt, total)
    dbc.set_status_log("finish mapping")
    systemstr = "rm aln.bam"
    os.system(systemstr)
    systemstr = "rm unmapped.bam"
    os.system(systemstr)

#GC Filtering
def GC_Filter(dbc):
    dbc.set_status_log("start GC_Filter")
    os.chdir(SPECIFICPATH)
    fin = open("Uniq.txt", 'r')
    fout = open("Uniq_filtered.fa", 'w')
    for line in SeqIO.parse(fin, 'fasta'):
        if int(GC_ratio_min) < int(GC(line.seq)) < int(GC_ratio_max):
            SeqIO.write(line, fout, 'fasta')
    fin.close()
    fout.close()
    dbc.set_status_log("end GC_Filter")

if __name__ == '__main__':
    try:
        ##### MAIN #####
        full_path = os.path.realpath(__file__)
        current = os.path.dirname(full_path)
        current = str(Path(current).resolve().parent)
        dbc = DBController(current + '/db.sqlite3', 'REGION')
        Genus = sys.argv[1]
        Species = sys.argv[2]
        k_length = sys.argv[3]
        GC_ratio_min = sys.argv[4]
        GC_ratio_max = sys.argv[5]
        print("command args genus : {} / species : {} / k_length : {} / GC_ratio_min : {} / GC_ratio_max : {}".format(Genus, Species,
                                                                                                         k_length
                                                                                                         , GC_ratio_min,
                                                                                                         GC_ratio_max))
        dbc.set_running()
        Specific_in_genus(dbc)
        os.chdir(SPECIFICPATH)
        if os.stat("Uniq.txt").st_size != 0:
            Mapping(dbc)
            GC_Filter(dbc)
        dbc.set_idle()
    except Exception as e:
        print(traceback.format_exc())
        dbc.set_main_error(str(e))
        dbc.set_idle()
