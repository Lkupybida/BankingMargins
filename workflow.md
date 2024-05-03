# Workflow

### 1. Extract pre-variables from raw excels
**Extract**
Aggregation
- L = loans
- D = deposits
- LA = liquid assets
- TA = total assets
- AE = administartive expenses
- C = cash
- NI = not interest income
- TI = total income
- NII = net interest income

KVED
- NPL = non performingloans
- CL = consumer loans

Other
- PR = policy rate -> *note: take avarage for each month*
- INF = inflation

**Transpose all pre-variables to format:**<br>
```{csv}
year, bank_1, bank_2, ....
```
<br>

**Keep only chosen 11 banks**
Banks to keep:
```{json}
"cb privatbank"
"credit agricole bank"
"fuib"
"kredobank"
"oschadbank"
"otp bank"
"pivdennyi bank"
"raiffeisen bank"
"sense bank"
"ukrsibbank"
"universal bank"
```


### 2. Differentiate to remove rolling sum
Differantiate these pre-variables:
- AE
- NI
- NII
- TI

To remove the rolling sum we subtract previous month from current month<br>
$month_t = month_t - month_{t-1}$, if $t \ne 2$
Note : if $t=1$, then $t-1=12$, but for previous year

### 3. Shift pre-variables one month back
Most of the data is for the first day of the month and corresponds to financial activity for previous month. Take into account this by shifting every variable except for INF and PR by one month back:<br>
2019-06-01 **->** 2019-05

### 4. Remove month with lacking or invalid data
These month have either negative data values or lack data for some pre-variables, so we will remove them from all data:
```{json}
"2018-12",
"2019-01",
"2019-03",
"2021-01", # have no CR
"2021-06",
"2020-08",
"2021-12",
"2022-04", # have no CR
"2022-05", # have no CR
"2023-09",
"2023-11",
"2023-12",
"2024-03",
"2024-04"
```
<span style="color:red">**!!!SUBJECT TO CHANGE!!!**</span>

### 5. Create composite time series
Create a time series that comprises of the sum of time series of corresponding banks for a given pre-variable.
Note: INF and PR do not need to be summed

### 6. Create variables from given pre-variables and composite pre-variables
Use these formulas to create variables from pre-variables:
- $NIM=\frac{NII}{TA}$
- $PR=PR$
- $SIZE=\log(TA)$ - note, that TA needs to be adj. for $INF$
- $CR=\frac{NPL}{CL}$
- $ROA=\frac{TI}{TA}$
- $NIA=\frac{NI}{TI}$
- $SCTA=\frac{C}{TA}$
- $OE=\frac{AE}{TA}$
- $LAS=\frac{LA}{TA}$
- $CDR=\frac{L}{D}$
- $RA=\frac{TE}{TA}$

### 7. Remove trends & seasonality
Plot all variables, check for trends and seasonality, remove them if present.

### 8. Correlation matrix + other diagnostic tests

### 9. Run OLS on composite data

### 10. Stack indivudual bank data into one .csv & create dummies for each bank

### 11. Run OLS on fixed effects data
