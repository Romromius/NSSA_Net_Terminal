import subprocess

args = [
    "mimic3",
    "\"Hello World\"",
    "--output-dir", "OUTPUT/DIR"]
try:
    subprocess.check_call(args)
except subprocess.CalledProcessError as e:
    # Handle error
    pass