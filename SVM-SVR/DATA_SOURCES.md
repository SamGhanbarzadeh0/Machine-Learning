# Data sources

## UCI Dermatology

Güvenir, H. A., Demiröz, G., and İlter, N. Dermatology [Dataset]. UCI Machine Learning Repository, dataset 33. [Dataset page](https://archive.ics.uci.edu/dataset/33/dermatology); [DOI: 10.24432/C5FK5P](https://doi.org/10.24432/C5FK5P). License: CC BY 4.0. The file contains 366 rows, 34 predictors and six classes.

## NHANES

National Center for Health Statistics, CDC. [National Health and Nutrition Examination Survey](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx), 2017–March 2020 pre-pandemic cycle. The two development CSVs come from the [Multidimensional-Data repository](https://github.com/sudeepkumarhs/Multidimensional-Data). Their Git blob SHA-1 values are:

| File | Git blob SHA-1 |
|---|---|
| Female measurements | `83adef2fdcbcb4dd484851ca6db7f477f9383135` |
| Male measurements | `d820fa76bc3ba31cf13bf3d9648464720208fe27` |

These derived CSVs omit participant identifiers and survey weights. They are available from the linked source and are not included here because its redistribution terms were unspecified. Use copies for which you have permission.

Temporal validation uses the official [BMX_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.htm) and [DEMO_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm) files from August 2021–August 2023. Eligible records have age at least 18 years, complete positive measurements, known sex and positive exam weight. The reader follows the [SAS XPORT V5 format](https://support.sas.com/content/dam/SAS/support/en/technical-papers/record-layout-of-a-sas-version-5-or-6-data-set-in-sas-transport-xport-format.pdf).

The [NCHS data user agreement](https://www.cdc.gov/nchs/policy/data-user-agreement.html) sets the conditions for use of the public-use files, including restrictions on re-identification. The [NHANES citation guidance](https://wwwn.cdc.gov/nchs/nhanes/NhanesCitation.aspx) gives the recommended attribution.
