import pandas as pd
import numpy as np
import urllib.request
from pathlib import Path
import logging
from dotenv import load_dotenv
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()   

DATASETS_DIR = os.getenv("DATASETS_PATH")
DATASETS_DIR = Path(DATASETS_DIR)   
NSL_KDD_URLS = {
    'train': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt',
    'test': 'https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt'
}


FEATURE_NAMES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack_type', 'difficulty'
]

ATTACK_TYPES = {
    'normal': 'normal',
    'back': 'attack', 'land': 'attack', 'neptune': 'attack', 'pod': 'attack',
    'smurf': 'attack', 'teardrop': 'attack', 'mailbomb': 'attack', 'apache2': 'attack',
    'processtable': 'attack', 'udpstorm': 'attack', 'satan': 'attack', 'ipsweep': 'attack', 
    'nmap': 'attack', 'portsweep': 'attack', 'mscan': 'attack', 'saint': 'attack',
    'guess_passwd': 'attack', 'ftp_write': 'attack', 'imap': 'attack', 'phf': 'attack',
    'multihop': 'attack', 'warezmaster': 'attack', 'warezclient': 'attack', 'spy': 'attack',
    'xlock': 'attack', 'xsnoop': 'attack', 'snmpread': 'attack', 'snmpwrite': 'attack',
    'httptunnel': 'attack', 'worm': 'attack', 'named': 'attack', 'sendmail': 'attack',
    'xterm': 'attack', 'ps': 'attack', 'sqlattack': 'attack', 'buffer_overflow': 'attack', 
    'loadmodule': 'attack', 'perl': 'attack', 'rootkit': 'attack'
}

def load_nsl_kdd_data(filepath):
    df = pd.read_csv(filepath, header=None, names=FEATURE_NAMES)
    df = df.drop('difficulty', axis=1)
    df['label'] = df['attack_type'].apply(lambda x: 0 if x=="normal" else 1)
    df = df.drop('attack_type', axis=1)

    return df

def main():
    
    train_file = DATASETS_DIR / 'KDDTrain+.txt'
    test_file = DATASETS_DIR / 'KDDTest+.txt'
    if not train_file.exists():
        logger.info("Downloading training data...")
        urllib.request.urlretrieve(NSL_KDD_URLS['train'], str(train_file))
    
    if not test_file.exists():
        logger.info("Downloading test data...")
        urllib.request.urlretrieve(NSL_KDD_URLS['test'], str(test_file))
 
    train_df = load_nsl_kdd_data(str(train_file))
    test_df = load_nsl_kdd_data(str(test_file))
    combined_df = pd.concat([train_df, test_df], ignore_index=True)
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save full dataset
    output_file = DATASETS_DIR / 'nsl_kdd_processed.csv'
    combined_df.to_csv(output_file, index=False)
    
    # # Save full dataset
    # output_file = DATASETS_DIR / 'test_kdd.csv'
    # test_df.to_csv(output_file, index=False)
    # output_file = DATASETS_DIR / 'train_kdd.csv'
    # train_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()