import subprocess
from io import StringIO
import pandas as pd


def admix(in_file, model):
    res = StringIO(subprocess.check_output(f"admix -f {in_file} -m {model}", shell=True, text=True))
    df = pd.read_csv(res, skiprows=5)
    ser = df.iloc[:, -1].str.split(": ", expand=True)[1]
    admix_scores = ",".join(a.strip('%') for a in ser)
    return admix_scores
