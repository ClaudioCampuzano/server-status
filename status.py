import GPUtil as gputil
import psutil
import requests
import argparse

def sendSlackMsg(message):
    payload = '{"text":"%s"}' % message
    res = requests.post('API_URL',data=payload)
    if res.status_code == 200:
        print('Ok')
    else:
        print('Error')
        
def getInfoDs(filename, analyticalType):
    Ds_process='`'+analyticalType+' Ds:`\n'
    gatillo = False
    try:
        for line in reversed(list(open(filename))):
            if gatillo:
                Ds_process += '\n'+line.rstrip()
                break
            if line.split(" ")[0].rstrip() == '**PERF:':
                Ds_process += line.rstrip()
                gatillo = True
        stringList = Ds_process.split('\n')
        return stringList[0]+'\n ```'+stringList[2]+'\n'+stringList[1]+'``` \n'
    except:
        print('Problemas al abrir el archivo '+analyticalType+' Ds Log')
        return Ds_process

def getInfoFaust(filename, analyticalType):
    Faust_process = '`'+analyticalType+' Faust:`\n ```'
    try:
        for index, line in enumerate(reversed(list(open(filename)))):
            if index < 3:
                Faust_process += line.rstrip() + '\n'
            else:
                break
    except:
        print('Problemas al abrir el archivo '+analyticalType+' Faust Log')
        Faust_process += ''
    return Faust_process+'```'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program that reports metrics from the computer to Slack')
    parser.add_argument('-n', '--mallName', type=str, required=True, help='name of the mall to report')
    parser.add_argument('-a', '--logFlujoFaust', type=str, required=True, help='Absolute address of the flujo Faust log')
    parser.add_argument('-b', '--logFlujoDs', type=str, required=True, help='Absolute address of the flujo Ds log')
    parser.add_argument('-c', '--logAforoFaust', type=str, required=True, help='Absolute address of the Aforo Faust log')
    parser.add_argument('-d', '--logAforoDs', type=str, required=True, help='Absolute address of the Aforo Ds log')

    args = parser.parse_args()

    gpu = gputil.getGPUs()
    for item in gpu:
        gpu_usage = item.load*100
        gpu_memory = item.memoryUsed
        gpu_temp = item.temperature
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    gpu= f"gpu: {round(gpu_usage)}%"
    gpuMem = f"gpu mem: {round(gpu_memory)}MiB"
    temp = f"temp: {gpu_temp}C"
    ramUsed = f"ram used: {round(ram.used/(1024**3))}GiB"
    diskFree = f"disk free: {round(disk.free/(1024**3))}GiB"
    systemUtils=['```',gpu,gpuMem,temp,ramUsed,diskFree,'```\n']

    mallName = '>*'+args.mallName+'*:'

    flujoFaust = getInfoFaust(args.logFlujoFaust,'#--Flujo--#')
    aforoFaust = getInfoFaust(args.logAforoFaust,'#--Aforo--#')
    flujoDs = getInfoDs(args.logFlujoDs,'#--Flujo--#')
    aforoDs = getInfoDs(args.logAforoDs,'#--Aforo--#')

    sendSlackMsg("\n".join([mallName]+systemUtils+[flujoFaust,flujoDs,aforoFaust,aforoDs]+['*--------------------------------------------------------------------*']))
