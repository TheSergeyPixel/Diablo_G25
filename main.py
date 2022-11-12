import pandas as pd
import gzip
import argparse
import os
from time import time
from numpy import ceil
from src import admix

parser = argparse.ArgumentParser(description='Diablo_G25')

parser.add_argument('-i', '--input', required=True, help='Input as vcf.gz file', type=str)
parser.add_argument('-o', '--output', required=True, help='Output in txt file', type=str)
parser.add_argument('-m', '--model', required=False, help='model to use in admix', type=str)

args = parser.parse_args()


def read_vcf():
    with gzip.open(os.path.abspath(args.input), "rt") as f:
        for i, n in enumerate(f.readlines()):
            if n.startswith('#CHROM'):
                index_df = i
                sample = n.split()[-1]

    df_vcf = pd.read_csv(os.path.abspath(args.input), skiprows=index_df, compression="gzip", sep='\t',
                         usecols=['#CHROM', 'POS', 'REF', 'ALT', 'ID', sample])
    return df_vcf, sample


def read_snp():
    snp_df = pd.read_csv("db/23andmevars.tsv", sep='\t')
    snp_df = snp_df[snp_df['REF'].str.len() == 1]
    return snp_df


def generate_required_lists(snp_df):
    var_dict = {}
    for var, ref in zip(snp_df['ID'], snp_df['REF']):
        var_dict[var] = ref
    temp_list = list(var_dict.keys())

    return temp_list, var_dict


def process_snp_df(df, temp_list, sample_name, snp_dict, snp_df):
    result = pd.DataFrame(columns=['# rsid', 'chromosome', 'position', 'genotype'])
    df_filt = df[df.ID.isin(temp_list)]

    rsid = []
    chrom = []
    pos = []
    gt = []

    for r, c, p, g, ref, a in zip(df_filt["ID"], df_filt['#CHROM'], df_filt["POS"],
                                  df_filt[sample_name], df_filt["REF"], df_filt["ALT"]):

        rsid.append(r)
        chrom.append(int(c.strip("chr")))
        pos.append(p)
        temp_gt = g.split(":")[0]
        if temp_gt == "0|1" or temp_gt == "0/1":
            gt.append(ref + a)
        elif temp_gt == "1|1" or temp_gt == "1/1":
            gt.append(a + a)
        else:
            gt.append(snp_dict[r] + snp_dict[r])

    snp_list = set(rsid)

    for c, p, rs, ref in zip(snp_df["CHROM"], snp_df["POS"], snp_df["ID"], snp_df["REF"]):
        if rs not in snp_list:
            chrom.append(int(c.replace('chr', '')))
            pos.append(int(p))
            rsid.append(rs)
            gt.append(ref + ref)

    result["# rsid"] = rsid
    result['chromosome'] = chrom
    result['position'] = pos
    result['genotype'] = gt

    return result


def generate_output(processed_snp_df):
    final_df = processed_snp_df.sort_values(by=['chromosome', 'position'], ascending=[True, True], ignore_index=True)
    return final_df


def main():
    start_time = time()

    df, sample_name = read_vcf()
    snp_df = read_snp()
    var_list, snp_dict = generate_required_lists(snp_df)
    result = process_snp_df(df, var_list, sample_name, snp_dict, snp_df)
    final_df = generate_output(result)

    final_df.to_csv(os.path.abspath(args.output), index=False, sep='\t')

    mod_scores = admix(os.path.abspath(args.output), args.model)

    with open(os.path.join(os.path.split(args.output)[0],
                           f"{''.join(os.path.split(args.output)[1].split('.')[:-1])}_G25.txt"), 'w') as g_scores:
        g_scores.write(f"{''.join(os.path.split(args.output)[1].split('.')[:-1])},{mod_scores}")

    stop_time = time()

    print("Completed successfully!")

    return print(f'Finished in {str(ceil(stop_time - start_time))} seconds')


if __name__ == '__main__':
    main()
