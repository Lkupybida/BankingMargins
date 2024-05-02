import math
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm
import statsmodels.formula.api as smf


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def run_rand_effects_on_flattened(
    file_path: str,
    X_var_names=["PR", "CDR", "LAS", "CR", "NIA", "OE", "RA", "ROA", "SCTA", "SIZE"],
    show_all=False,
):
    """
    Runs random effects model on flattened(panaled) .csv file
    Under the hoods runs pooled OLS and fixed effects,
    their results can be seen if show_all = True

    #### Args:
        file_path (str): path to .csv table
        X_var_names (list, optional): Name of variables to include in the model. Defaults to ["PR", "CDR", "LAS", "CR", "NIA", "OE", "RA", "ROA", "SCTA", "SIZE"].
        show_all (bool, optional): Show or not seps result of pooled OLS and FE. Defaults to False.

    #### Returns:
        RegressionResultsWrapper: results of fitring RE model
    """

    # Set inputs
    bank_names = [
        "Credit_Agricole",
        "FUIB",
        "Kredobank",
        "OTP",
        "Oschadbank",
        "Pivdennyi",
        "Privat_Bank",
        "Raiffeisen",
        "Sense",
        "Ukrsibbank",
        "Universal",
    ]
    bank_names.sort()
    bank_col_name = "Bank"
    y_var_name = "NIM"

    df_panel = pd.read_csv(
        file_path,
        header=0,
        index_col=0,
    )
    df_panel = df_panel.dropna()
    columns_to_drop = [col for col in df_panel.columns if col.startswith("is")]
    df_panel.drop(columns=columns_to_drop, inplace=True)

    # get some constant vars
    n = len(bank_names)
    T = df_panel.shape[0] / n
    N = n * T
    k = len(X_var_names)

    ######## Pooled OLS #########
    pooled_y = df_panel[y_var_name]
    pooled_X = df_panel[X_var_names]
    pooled_X = sm.add_constant(pooled_X)
    pooled_olsr_model = sm.OLS(endog=pooled_y, exog=pooled_X)
    pooled_olsr_model_results = pooled_olsr_model.fit()

    if show_all:
        print(
            "==============================================================================="
        )
        print(
            "============================== Pooled OLSR model =============================="
        )
        print(pooled_olsr_model_results.summary())
    # print("residuals of the 'Pooled OLSR' model:")
    # print(pooled_olsr_model_results.resid)

    ######### Dummies #########
    df_dummies = pd.get_dummies(df_panel[bank_col_name])
    df_panel_with_dummies = df_panel.join(df_dummies)

    lsdv_expr = y_var_name + " ~ "
    i = 0
    for X_var_name in X_var_names:
        if i > 0:
            lsdv_expr = lsdv_expr + " + " + X_var_name
        else:
            lsdv_expr = lsdv_expr + X_var_name
        i = i + 1
    for dummy_name in bank_names[:-1]:
        lsdv_expr = lsdv_expr + " + " + dummy_name

    ######### Fixed Effects #########
    lsdv_model = smf.ols(formula=lsdv_expr, data=df_panel_with_dummies)
    lsdv_model_results = lsdv_model.fit()

    if show_all:
        print(
            "==============================================================================="
        )
        print(
            "============================== OLSR With Dummies =============================="
        )
        print(lsdv_model_results.summary())

    # Calculate sigma-square-epsilon
    sigma2_epsilon = lsdv_model_results.ssr / (n * T - (n + k + 1))
    sigma2_pooled = pooled_olsr_model_results.ssr / (n * T - (k + 1))
    sigma2_u = sigma2_pooled - sigma2_epsilon
    theta = 1 - math.sqrt(sigma2_epsilon / (sigma2_epsilon + T * sigma2_u))
    if show_all:
        print("sigma2_epsilon = " + str(sigma2_epsilon))
        print("sigma2_pooled = " + str(sigma2_pooled))
        print("sigma2_u = " + str(sigma2_u))
        print("theta = " + str(theta))

    ######### Calculating means #########
    df_panel_group_means = df_panel.groupby(bank_col_name).mean(numeric_only=True)
    df_panel_group_means["const"] = 1.0

    unit_col_name = bank_col_name
    # Prepare the data set for mean centering the y and X columns:
    pooled_y_with_unit_name = pd.concat([df_panel[unit_col_name], pooled_y], axis=1)
    pooled_X_with_unit_name = pd.concat([df_panel[unit_col_name], pooled_X], axis=1)

    # Center each X value using the θ-scaled group-specific mean:
    unit_name = ""
    for row_index, row in pooled_X_with_unit_name.iterrows():
        for column_name, cell_value in row.items():
            if column_name == unit_col_name:
                unit_name = pooled_X_with_unit_name.at[row_index, column_name]
            else:
                pooled_X_group_mean = df_panel_group_means.loc[unit_name][column_name]
                pooled_X_with_unit_name.at[row_index, column_name] = (
                    pooled_X_with_unit_name.at[row_index, column_name]
                    - theta * pooled_X_group_mean
                )

    # Center each y value using the θ-scaled group-specific mean:
    for row_index, row in pooled_y_with_unit_name.iterrows():
        for column_name, cell_value in row.items():
            if column_name == unit_col_name:
                unit_name = pooled_y_with_unit_name.at[row_index, column_name]
            else:
                pooled_y_group_mean = df_panel_group_means.loc[unit_name][column_name]
                pooled_y_with_unit_name.at[row_index, column_name] = (
                    pooled_y_with_unit_name.at[row_index, column_name]
                    - theta * pooled_y_group_mean
                )

    ######### Final step #########
    # Carve out the y and X matrices:
    re_y = pooled_y_with_unit_name[list(pooled_y_with_unit_name.columns[1:])]
    re_X = pooled_X_with_unit_name[list(pooled_X_with_unit_name.columns[1:])]

    # Build and train the model
    re_model = sm.OLS(endog=re_y, exog=re_X)
    re_model_results = re_model.fit()

    print(
        bcolors.WARNING
        + "==============================================================================="
        + bcolors.ENDC
    )
    print(
        bcolors.WARNING
        + "================================== RE Model ==================================="
        + bcolors.ENDC
    )
    print(re_model_results.summary())

    return re_model_results


# # Calculate the LM statistic to test for the significance of the Random Effect
# df_pooled_olsr_resid_with_unitnames = pd.concat(
#     [df_panel[unit_col_name], pooled_olsr_model_results.resid], axis=1
# )
# df_pooled_olsr_resid_group_means = df_pooled_olsr_resid_with_unitnames.groupby(
#     unit_col_name
# ).mean()
# ssr_grouped_means = (df_pooled_olsr_resid_group_means[0] ** 2).sum()
# ssr_pooled_olsr = pooled_olsr_model_results.ssr

# LM_statistic = (
#     (n * T)
#     / (2 * (T - 1))
#     * math.pow(((T * T * ssr_grouped_means) / ssr_pooled_olsr - 1), 2)
# )
# print("LM Statistic=" + str(LM_statistic))

# alpha = 0.05
# chi2_critical_value = st.chi2.ppf(q=(1.0 - alpha), df=1)
# print("chi2_critical_value=" + str(chi2_critical_value))
