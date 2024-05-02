from statsmodels.tools.eval_measures import rmse, mse, meanabs
from sklearn.metrics import mean_absolute_percentage_error as mape


class ManyModels:
    def __init__(self, path, df, X, y, res) -> None:
        self.path = path
        self.df = df
        self.X = X
        self.y = y
        self.res = res

    def get_estimators(self, silence=False):
        ypred = self.res.predict(self.X)
        rmse_results = round(rmse(self.y, ypred), 8)
        mse_results = round(mse(self.y, ypred), 8)
        mae_results = round(meanabs(self.y, ypred), 8)
        mape_res = round(mape(self.y, ypred), 8)
        if not silence:
            print("=================== HOW GOOD? ==================")
            print(f"Mean absolute error(MAE):               {mae_results}")
            print(f"Mean-absolute percentage error(MAPE):   {mape_res}")
            print(f"Mean-squred error(MSE):                 {mse_results}")
            print(f"Root mean-squred error(RMSE):           {rmse_results}")
        return {
            "MAE": mae_results,
            "MAPE": mape_res,
            "MSE": mse_results,
            "RMSE": rmse_results,
        }
