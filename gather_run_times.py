import os
import csv
import pandas as pd


from customer import Customer
import secret

EXTRACT_PATH = secret.EXTRACT_PATH
ROOT_PATH = secret.ROOT_PATH

def main():
    CUSTOMER_FOLDERS = pd.read_csv(EXTRACT_PATH, delimiter = '\t', encoding = 'latin1')
    community = {}
    with open("run_times.tab", "a") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        #TODO: use apply or pipe rather than iterating over the dataframe
        for idx, row in CUSTOMER_FOLDERS.iterrows():
            community[row['GPID']] = Customer(row['GPID'], row['CustomerFolder'], ROOT_PATH+row['CustomerFolder']+'\\')
            community[row['GPID']].init_review_history()
            writer.writerows(community[row['GPID']].log)
            
    

if __name__ == "__main__":
    main()
        


