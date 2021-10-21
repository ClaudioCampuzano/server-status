import GPUtil as gputil
import psutil
import requests

def sendSlackMsg(message):
    payload = '{"text":"%s"}' % message
    res = requests.post('https://hooks.slack.com/services/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',data=payload)
    if res.status_code == 200:
        print('Ok')
    else:
        print('Error')

if __name__ == '__main__':
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
    
    sendSlackMsg("\n".join([gpu,gpuMem,temp,ramUsed,diskFree]))
