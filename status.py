import GPUtil as gputil
import psutil
import requests
import argparse

def sendSlackMsg(message):
    payload = '{"text":"%s"}' % message
    res = requests.post('https://hooks.slack.com/services/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',data=payload)
    if res.status_code == 200:
        print('Ok')
    else:
        print('Error')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program that reports metrics from the computer to Slack')
    parser.add_argument('-n', '--mallName', type=str, required=True, help='name of the mall to report')
    parser.add_argument('-f', '--logFaust', type=str, required=True, help='Absolute address of the Faust log')
    parser.add_argument('-d', '--logDs', type=str, required=True, help='Absolute address of the Faust log')
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
    mallName = args.mallName+':'

    for line in reversed(list(open(args.logDs))):
        if line.split(" ")[0].rstrip() == '**PERF:':
            Ds_process = 'Ds: '+line.rstrip()
            break
    Faust_process = 'Faust: '
    for index, line in enumerate(reversed(list(open(args.logFaust)))):
        if index < 5:
            Faust_process += line.rstrip() + '\n'
        else:
            break
    sendSlackMsg("\n".join([mallName,gpu,gpuMem,temp,ramUsed,diskFree,Ds_process, Faust_process]))
