# Motor Insurance Data Description

## Source

The two CSV files ([freMTPL2freq.csv](https://www.kaggle.com/datasets/floser/french-motor-claims-datasets-fremtpl2freq), [freMTPL2sev.csv](https://www.kaggle.com/datasets/floser/fremtpl2sev)) were downloaded from Kaggle on **25 November 2026**. Field definitions are based on the [CASdatasets reference](https://dutangc.github.io/CASdatasets/reference/freMTPL.html).

| File | Reported rows | Columns | Intended row grain |
| --- | ---: | ---: | --- |
| `freMTPL2freq.csv` | 678,013 | 12 | One policy exposure record |
| `freMTPL2sev.csv` | 26,639 | 2 | One claim amount record |

## Frequency table

### Column definitions

| Column | Description |
| --- | --- |
| `IDpol` | Policy identifier. |
| `ClaimNb` | Number of claims during the policy exposure period. |
| `Exposure` | Length of the exposure period in years. |
| `Area` | Ordered area code based on population density, from A (rural) to F (urban). |
| `VehPower` | Ordered vehicle power code. |
| `VehAge` | Vehicle age in years. |
| `DrivAge` | Driver age in years. |
| `BonusMalus` | French bonus–malus rating. Values below 100 indicate a bonus, 100 is neutral, and values above 100 indicate a malus. The documented range is 50–350. |
| `VehBrand` | Vehicle brand category code. |
| `VehGas` | Vehicle fuel category. |
| `Density` | Population density in the driver's municipality, measured in inhabitants per square kilometre. |
| `Region` | French region code based on the 1970–2015 classification. |

This dataset is seen to have 0 null entries for IDpol. In fact, there are 0 null entries everywhere. All IDpol entries are unique. ClaimNb is non-negative, and Exposure is strictly positive.

## Severity table

### Column definitions

| Column | Description |
| --- | --- |
| `IDpol` | Policy identifier. |
| `ClaimAmount` | Recorded cost of the claim. Currency to be confirmed. |

This table also has 0 null entries everywhere. ClaimAmount is positive everywhere.

## Table relationship

A policy can have multiple severity records, so `IDpol` can repeat in the severity table. A policy with no claims is expected to have no severity record.

## Issues

- There are 195 rows in the severity table with no corresponding IDpol in the frequency table. These comes from 6 unique IDs.
- The frequency table records claims with 0 payout (such as when the policyholder was not at fault), whereas the severity table records claims with strictly positive payouts. I found that 9117 policyholders have less appearances in the severity table than reported in ClaimNb. 668896 policyholders have the same number of appearances in the severity table as they do claims in the frequency table. 0 policyholders have more appearances in the severity table than reported in ClaimNb.
- Of the 9117 policyholders with less appearances in severity than claims in frequency, 9116 of these do not appear in severity at all.

## Decision

I will keep all frequency policies, and exclude the 195 severity rows without a matching policy record. Policies without a severity match contribute zero recorded cost.