import os

#Run GTDBTK for First Download
from pathlib import Path

from dbcontroller import DBController

full_path = os.path.realpath(__file__)
current = os.path.dirname(full_path)
current = str(Path(current).resolve().parent)
GTDBTKPATH = current + '/media/GTDBTK'
MEDIAPATH = current + '/media'


def GTDBTK(dbc):
    if not os.path.isdir(GTDBTKPATH):
        os.mkdir(GTDBTKPATH)
        os.mkdir(GTDBTKPATH + '/identify')
        os.mkdir(GTDBTKPATH + '/align')
        os.mkdir(GTDBTKPATH + '/classify')

    os.chdir(GTDBTKPATH)
    dbc.set_status_log("start GTDBTK")
    systemstr = "gtdbtk identify --genome_dir {0}/Down/Downloaded --out_dir {1}/identify --extension fna --cpus 16".format(MEDIAPATH, GTDBTKPATH)
    print(systemstr)
    dbc.set_status_log("do {}".format(systemstr))
    os.system(systemstr)
    systemstr = "gtdbtk align --identify_dir {0}/identify --out_dir {0}/align --cpus 16".format(GTDBTKPATH)
    print(systemstr)
    dbc.set_status_log("do {}".format(systemstr))
    os.system(systemstr)
    systemstr = "gtdbtk classify --genome_dir {0}/Down/Downloaded --align_dir {1}/align --out_dir {1}/classify -x fna --cpus 16".format(MEDIAPATH, GTDBTKPATH)
    print(systemstr)
    dbc.set_status_log("do {}".format(systemstr))
    os.system(systemstr)
    os.chdir(GTDBTKPATH)
    dbc.set_status_log("finish GTDBTK")


#Assign classifed
def Reassign(dbc):
    os.chdir(GTDBTKPATH)
    if not os.path.isdir("{}/reassigned".format(GTDBTKPATH)):
        os.mkdir("{}/reassigned".format(GTDBTKPATH))
    dbc.set_status_log("start Reassign")
    assign_file = GTDBTKPATH + "/classify/gtdbtk.bac120.summary.tsv"
    fna_folder = MEDIAPATH + "/Down/Downloaded/"

    ck = open(assign_file, 'r')
    total = len(ck.readlines()) - 1
    ck.close()

    fin = open(assign_file, 'r')
    header = fin.readline()
    cnt = 0
    for line in fin:
        linetemp = line.strip().split("\t")
        file_name = linetemp[0] + ".fna"
        g_name = linetemp[1].split(";g__")[1].split(";s__")[0]
        s_name = linetemp[1].split(";s__")[1].replace(" ", "_")
        if s_name == "":
            continue
        elif s_name.count("_") > 1:
            continue
        elif "sp0" in s_name:
            continue
        else:
            if not os.path.isdir("{}/reassigned/" + g_name.format(GTDBTKPATH)):
                os.mkdir("{}/reassigned/" + g_name.format(GTDBTKPATH))
            if not os.path.isdir("{}/reassigned/" + g_name + "/" + s_name.format(GTDBTKPATH)):
                os.mkdir("{}/reassigned/" + g_name + "/" + s_name.format(GTDBTKPATH))
            systemstr = "cp " + fna_folder + file_name + " " + "{}/reassigned/" + g_name + "/" + s_name.format(GTDBTKPATH)
            os.system(systemstr)
        dbc.set_status_log("Reassign {}/{} 진행 중 ".format(cnt, total))
        cnt += 1
        dbc.set_process(cnt, total)
    os.chdir("../")
    dbc.set_status_log("finish Reassign")


#GTDB Folder Remove"
def Remove(dbc):
    dbc.set_status_log("start Remove")
    os.chdir(GTDBTKPATH)
    systemstr = "rm -r {}/identify".format(GTDBTKPATH)
    dbc.set_status_log("do {}".format(systemstr))
    os.system(systemstr)
    systemstr = "rm -r {}/align".format(GTDBTKPATH)
    dbc.set_status_log("do {}".format(systemstr))
    os.system(systemstr)
    systemstr = "rm -r {}/classify".format(GTDBTKPATH)
    dbc.set_status_log("do {}".format(systemstr))
    os.system(systemstr)
    os.chdir("../")
    dbc.set_status_log("finish Remove")


#GTDB for update genome
def GTDBTK_update(dbc):
    os.chdir(GTDBTKPATH)
    dbc.set_status_log("start GTDBTK_update")
    systemstr = "gtdbtk identify --genome_dir {0}/Down/Update --out_dir {1}/identify --extension fna --cpus 16".format(MEDIAPATH, GTDBTKPATH)
    os.system(systemstr)
    systemstr = "gtdbtk align --identify_dir {}/identify --out_dir ./align --cpus 16".format(GTDBTKPATH)
    os.system(systemstr)
    systemstr = "gtdbtk classify --genome_dir {0}/Down/Update --align_dir {1}/align --out_dir {1}/classify -x fna --cpus 16".format(MEDIAPATH, GTDBTKPATH)
    os.system(systemstr)
    os.chdir("../")
    dbc.set_status_log("finish GTDBTK_update")


#Assign update classifed
def Reassign_update(dbc):
    os.chdir(GTDBTKPATH)
    if not os.path.isdir("{}/reassigned".format(GTDBTKPATH)):
        os.mkdir("{}/reassigned".format(GTDBTKPATH))
    dbc.set_status_log("start Reassign_update")
    assign_file = GTDBTKPATH + "/classify/gtdbtk.bac120.summary.tsv"
    fna_folder = MEDIAPATH + "/Down/Update/"

    ck = open(assign_file, 'r')
    total = len(ck.readlines()) - 1
    ck.close()

    fin = open(assign_file, 'r')
    header = fin.readline()
    cnt = 0
    for line in fin:
        linetemp = line.strip().split("\t")
        file_name = linetemp[0]+".fna"
        g_name = linetemp[1].split(";g__")[1].split(";s__")[0]
        s_name = linetemp[1].split(";s__")[1].replace(" ", "_")

        if s_name == "":
            continue
        elif s_name.count("_") > 1:
            continue
        elif "sp0" in s_name:
            continue
        else:
            if not os.path.isdir("{}/reassigned/"+g_name.format(GTDBTKPATH)):
                os.mkdir("{}/reassigned/"+g_name.format(GTDBTKPATH))
            if not os.path.isdir("{}/reassigned/"+g_name+"/"+s_name.format(GTDBTKPATH)):
                os.mkdir("{}/reassigned/"+g_name+"/"+s_name.format(GTDBTKPATH))
            systemstr = "cp "+fna_folder+file_name+" "+"{}/reassigned/"+g_name+"/"+s_name.format(GTDBTKPATH)
            os.system(systemstr)
        dbc.set_status_log("Reassign_update {}/{} 진행 중 ".format(cnt, total))
        cnt += 1
        dbc.set_process(cnt, total)
    os.chdir("../")
    systemstr = "mv {}/Down/Update/* {}/Down/Downloaded".format(MEDIAPATH)
    os.system(systemstr)
    dbc.set_status_log("finish Reassign_update")


if __name__ == '__main__':
    try:
        ######## MAIN ########
        full_path = os.path.realpath(__file__)
        current = os.path.dirname(full_path)
        current = str(Path(current).resolve().parent)
        dbc = DBController(current + '/db.sqlite3', 'GTDBTK')
        dbc.set_running()
        if not os.path.isdir(GTDBTKPATH):
            GTDBTK(dbc)
            Reassign(dbc)
            Remove(dbc)

        if os.path.isdir(GTDBTKPATH):
            if os.path.isdir(MEDIAPATH + "/Down/Update/") and len(os.listdir(MEDIAPATH + "/Down/Update/")) != 0:
                GTDBTK_update(dbc)
                Reassign_update(dbc)
                Remove(dbc)
    except Exception as e:
        dbc.set_main_error(str(e))
        dbc.set_idle()
