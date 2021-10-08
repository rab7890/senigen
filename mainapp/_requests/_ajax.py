import mimetypes
import os
import subprocess
import signal
import sys
import time
from wsgiref.util import FileWrapper

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from commands.dbcontroller import Process
from mainapp.models import DownloadGenomeInfo, GTDBTKInfo, MainInfo, RegionInfo
from senigenprimer.settings import MEDIA_ROOT


def check_status(request):
    data = {}
    main_obj = MainInfo.objects.get(id=1)
    genome_obj = DownloadGenomeInfo.objects.get(id=1)
    gtdbtk_obj = GTDBTKInfo.objects.get(id=1)
    region_obj = RegionInfo.objects.get(id=1)

    # read uniq_filtered.fa content
    the_file = MEDIA_ROOT + '/Specific/Uniq_filtered.fa'
    if os.stat(the_file).st_size != 0:
        with open(the_file, 'r') as fh:
            txt = fh.readlines()
            res = ''
            for v in txt[:15]:
                res += v
            res = res.strip('\n') + '...................'
            data['uniq_filtered'] = res

    # GENOME
    if genome_obj.status_log:
        data['GENOME_status_log'] = genome_obj.status_log
    else:
        data['GENOME_status_log'] = ''
    if genome_obj.last_run_date:
        data['GENOME_last_updated'] = 'Last DB updated : ' + genome_obj.last_run_date.strftime("%Y-%m-%d %H:%M")
    else:
        data['GENOME_last_updated'] = 'No Data'

    # GTDBTK
    if gtdbtk_obj.status_log:
        data['GTDBTK_status_log'] = gtdbtk_obj.status_log
    else:
        data['GTDBTK_status_log'] = ''
    if gtdbtk_obj.last_run_date:
        data['GTDBTK_last_updated'] = 'Last Classification Run : ' + gtdbtk_obj.last_run_date.strftime("%Y-%m-%d %H:%M")
    else:
        data['GTDBTK_last_updated'] = 'No Data'

    # Region
    if region_obj.status_log:
        data['REGION_status_log'] = region_obj.status_log
    else:
        data['REGION_status_log'] = ''
    if region_obj.last_run_date:
        data['REGION_last_updated'] = region_obj.last_run_date.strftime("%Y-%m-%d %H:%M")
    else:
        data['REGION_last_updated'] = 'No Data'



    if main_obj.is_error:
        data['state'] = 'error'
        data['error_type'] = main_obj.error_type
        data['msg'] = main_obj.error_msg
        return JsonResponse(data)

    if genome_obj.status == 'IDLE' and gtdbtk_obj.status == 'IDLE' and region_obj.status == 'IDLE':
        data['state'] = 'IDLE'
        return JsonResponse(data)

    elif genome_obj.status == "RUNNING" and gtdbtk_obj.status == "RUNNING" or \
            genome_obj.status == "RUNNING" and region_obj.status == "RUNNING" or \
            gtdbtk_obj.status == "RUNNING" and region_obj.status == "RUNNING" or \
        genome_obj.status == "RUNNING" and gtdbtk_obj.status == "RUNNING" and region_obj.status == "RUNNING":
        data['state'] = 'fail'
        data['msg'] = '두 가지 이상이 RUNNING 입니다. 데이테베이스 및 PID를 확인 해 주세요. 그리고 페이지를 새로고침 해 주세요.'
        return JsonResponse(data)

    else:
        data['state'] = 'RUNNING'
        if genome_obj.status == "RUNNING":
            data['status'] = "GENOME"
            data['process_total'] = genome_obj.progress_total_value
            data['process_current'] = genome_obj.progress_current_value
        elif gtdbtk_obj.status == "RUNNING":
            data['status'] = "GTDBTK"
            data['process_total'] = gtdbtk_obj.progress_total_value
            data['process_current'] = gtdbtk_obj.progress_current_value
        elif region_obj.status == "RUNNING":
            data['status'] = "REGION"
            data['process_total'] = region_obj.progress_total_value
            data['process_current'] = region_obj.progress_current_value

    return JsonResponse(data)

def load_Species_path(request):
    genus = request.GET.get("genus")
    data = {}
    try:
        if sys.platform == "win32":
            dirs = os.listdir(MEDIA_ROOT + '\\GTDBTK\\reassigned\\' + genus)
        else:
            dirs = os.listdir(MEDIA_ROOT + '/GTDBTK/reassigned/' + genus)
        dirs.sort()
        data['species_select'] = dirs
    except:
        data['species_select'] = []
        pass

    data['status'] = 'success'
    return JsonResponse(data)

def load_genus_path(request):
    # Region 폴더 -> select
    data = {}
    try:
        if sys.platform == "win32":
            dirs = os.listdir(MEDIA_ROOT + '\\GTDBTK\\reassigned')
        else:
            dirs = os.listdir(MEDIA_ROOT + '/GTDBTK/reassigned')
        dirs.sort()
        data['genus_select'] = dirs
    except:
        data['genus_select'] = []
        pass
    data['status'] = 'success'
    return JsonResponse(data)

@csrf_protect
def genome_run(request):
    current_path = os.getcwd()
    arg = request.POST.get('parameter')
    rel = '/commands/download.py'
    #proc = subprocess.Popen(["python3", current_path + rel, arg], preexec_fn=os.setsid)
    proc = subprocess.Popen("python3 " + current_path + rel + " " + arg, shell=True, preexec_fn=os.setsid)
    # stdout=subprocess.PIPE, stderr=subprocess.PIPE
    Process.process = proc
    DownloadGenomeInfo.objects.filter(id=1).update(pid=proc.pid, last_run_date=timezone.now())
    MainInfo.objects.filter(id=1).update(last_type='GENOME', last_pid=proc.pid, error_type='', error_msg='', is_error=False)
    #p = subprocess.check_output(['ps -aux'])
    return JsonResponse({'status': 'success'})


def execute_stop(request):
    try:
        type = request.GET.get('type')
        if type == "GENOME":
            obj = DownloadGenomeInfo.objects.get(id=1)
        elif type == "GTDBTK":
            obj = GTDBTKInfo.objects.get(id=1)
        elif type == "REGION":
            obj = RegionInfo.objects.get(id=1)
        pid = obj.pid
        obj.status = "IDLE"
        obj.progress_current_value = "0"
        obj.save()
        #os.system('kill -9 {}'.format(pid))
        #os.kill(int(pid), signal.SIGTERM)
        os.killpg(os.getpgid(int(pid)), signal.SIGKILL)
        #Process.process.communicate()
        #Process.process.terminate()
        #Process.process.kill()
        time.sleep(1)
        #os.kill(int(pid) + 1, signal.SIGTERM)
        obj.status = "IDLE"
        obj.progress_current_value = "0"
        obj.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'fail', 'msg': str(e)})


@csrf_protect
def upload_file(request):
    files = request.FILES.getlist('files[]')
    fs = FileSystemStorage(location=MEDIA_ROOT + '/Downloaded')
    for f in files:
        fs.save(f.name, f)
    return JsonResponse({'status': 'success'})

def gtdbtk_run(request):
    current_path = os.getcwd()
    rel = '/commands/gtdbtk.py'
    proc = subprocess.Popen("python3 " + current_path + rel, shell=True, preexec_fn=os.setsid)
    Process.process = proc
    GTDBTKInfo.objects.filter(id=1).update(pid=proc.pid, last_run_date=timezone.now())
    MainInfo.objects.filter(id=1).update(last_type='GTDBTK', last_pid=proc.pid, error_type='', error_msg='', is_error=False)
    return JsonResponse({'status': 'success'})

@csrf_protect
def region_run(request):
    current_path = os.getcwd()
    rel = '/commands/specific_region.py'
    genus = request.POST.get('region_genus')
    species = request.POST.get('region_species')
    k_length = request.POST.get('region_K_mer_length')
    GC_ratio_min = request.POST.get('region_GC_min')
    GC_ratio_max = request.POST.get('region_GC_max')

    proc = subprocess.Popen("python3 " + current_path + rel + " {} {} {} {} {}".format(genus,
                                                                                       species, k_length, GC_ratio_min,
                                                                                       GC_ratio_max),
                            shell=True, preexec_fn=os.setsid)
    Process.process = proc
    #proc = subprocess.Popen(["python3", current_path + rel, genus, species, k_length, GC_ratio_min, GC_ratio_max])
    RegionInfo.objects.filter(id=1).update(pid=proc.pid, last_run_date=timezone.now())
    MainInfo.objects.filter(id=1).update(last_type='REGION', last_pid=proc.pid, error_type='', error_msg='', is_error=False)
    return JsonResponse({'status': 'success'})
class FixedFileWrapper(FileWrapper):
    def __iter__(self):
        self.filelike.seek(0)
        return self

def download(request):
    if os.path.exists(MEDIA_ROOT + '/Specific/Uniq_filtered.fa'):
        the_file = MEDIA_ROOT + '/Specific/Uniq_filtered.fa'
        with open(the_file, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename=' + 'Specific_region.fa'
            return response
        """
        with open(the_file, 'rb') as fsock:
            
            response = HttpResponse()
            response['content_type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=download.txt'
            response.write(fsock.read())
            
            chunk_size = 8192
            response = StreamingHttpResponse(FixedFileWrapper(open(the_file, 'rb'), chunk_size),
                                             content_type=mimetypes.guess_type(the_file)[0])
            response['Content-Length'] = os.path.getsize(the_file)
            response['Content-Disposition'] = "attachment; filename=%s" % 'download.txt'
           
            return response
        """
    else:
        messages.add_message(request, messages.INFO, 'no Uniq.txt')
        return redirect('home')


