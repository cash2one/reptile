import subprocess


def call(command):
  call = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  out = call.stdout.read()

  return out.strip()
