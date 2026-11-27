import pandas as pd
import numpy as np

def data_partition(frequency, severity, split_ratio = 0.8):
    """
    Partition the data into training and testing sets based on the policy IDs.

    Parameters
    ----------
    frequency (pd.DataFrame): DataFrame containing frequency data.\n
    severity (pd.DataFrame): DataFrame containing severity data.\n
    split_ratio (float): Proportion of data to be used for training (default is 0.8).

    Returns
    -------
    train_frequency (pd.DataFrame): Training set for frequency data.\n
    test_frequency (pd.DataFrame): Testing set for frequency data.\n
    train_severity (pd.DataFrame): Training set for severity data.\n
    test_severity (pd.DataFrame): Testing set for severity data.
    """
    ids = frequency['IDpol']

    train_ids = ids.sample(frac=split_ratio, random_state=27).to_numpy()
    test_ids = ids[~ids.isin(train_ids)].to_numpy()

    train_frequency = frequency[frequency['IDpol'].isin(train_ids)]
    test_frequency = frequency[frequency['IDpol'].isin(test_ids)]

    train_severity = severity[severity['IDpol'].isin(train_ids)]
    test_severity = severity[severity['IDpol'].isin(test_ids)]

    return train_frequency, test_frequency, train_severity, test_severity

def audit_partition(train_frequency, test_frequency, train_severity, test_severity):
    """
    Audit the partitioned data to ensure integrity and consistency.

    Parameters
    ----------
    train_frequency (pd.DataFrame): Training set for frequency data.\n
    test_frequency (pd.DataFrame): Testing set for frequency data.\n
    train_severity (pd.DataFrame): Training set for severity data.\n
    test_severity (pd.DataFrame): Testing set for severity data.

    Returns
    -------
    audit_partition (pd.DataFrame): DataFrame containing audit results for both training and testing partitions.
    """
    total_policies = len(train_frequency) + len(test_frequency)
    rows = []
    for partition, freq, sev in [('train', train_frequency, train_severity),
                                 ('test', test_frequency, test_severity)]:
        claim_counts = sev['IDpol'].value_counts()
        rows.append({'partition': partition,
                    'policy_count': len(freq),
                    'share_of_policies': len(freq) / total_policies,
                    'severity_row_count': len(sev),
                    'PaidClaimNb_total': freq['PaidClaimNb'].sum(),
                    'n_policies_with_count_mismatch': (freq['PaidClaimNb'] != freq['IDpol'].map(claim_counts).fillna(0).astype(int)).sum()})
    audit = pd.DataFrame(rows).set_index('partition')
    return audit
