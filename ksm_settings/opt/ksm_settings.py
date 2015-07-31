import psutil
import os

def get_processlist():
    return [psutil.Process(i).name() for i in psutil.get_pid_list()]

def readfile(path):
    return open(path, 'r+').read()

def writefile(path, value):
	if readfile(path) is not value:
		f = open(path, 'w')
		f.write(value)

def is_qemu_alive():
	return "qemu-system-x86_64" in get_processlist()

def is_ksm_alive():
	return True if readfile(ksm_get_param['run']) ==1 else False

def ksm_get_param(param_name):
	f = {}
	f['run']='/sys/kernel/mm/ksm/run'
	f['pages_to_scan']='/sys/kernel/mm/ksm/pages_to_scan'
	f['sleep_millisecs']='/sys/kernel/mm/ksm/sleep_millisecs'
	return f[param_name] 

def ksm_get():
	run = readfile(ksm_get_param('run'))
	pages_to_scan = readfile(ksm_get_param('pages_to_scan'))
	sleep_millisecs = readfile(ksm_get_param('sleep_millisecs'))

	return run, pages_to_scan, sleep_millisecs
	

run, pages_to_scan, sleep_millisecs = ksm_get()
qemu_alive = is_qemu_alive()

if qemu_alive:
	writefile(ksm_get_param('run'), '1')
	writefile(ksm_get_param('pages_to_scan'), '5000')
	writefile(ksm_get_param('sleep_millisecs'), '1000')
else:
	writefile(ksm_get_param('run'), '0')
	writefile(ksm_get_param('pages_to_scan'), '100')
	writefile(ksm_get_param('sleep_millisecs'), '200')