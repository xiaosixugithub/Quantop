import numpy as np

from model_stock_data import StockDataSet


class ROICalculator(object):

    def __init__(self, stock_symbols):
        self.stock_symbols = stock_symbols

    def __load_pred(self, stock_symbol):
        return np.loadtxt("data/" + stock_symbol + "_pred.txt", delimiter=',')

    def calculate_roi(self, top_num, with_hedging=True):

        pred_res, truth_res = {}, {}
        stock_data = StockDataSet("^GSPC", input_size=1, num_steps=30, test_ratio=0.05)
        sp500 = stock_data.test_y

        for stock_symbol in self.stock_symbols:
            pred_res[stock_symbol] = self.__load_pred(stock_symbol)

            stock_data = StockDataSet(stock_symbol, input_size=1, num_steps=30, test_ratio=0.05)
            truth_res[stock_symbol] = stock_data.test_y

        roi = 1.0
        for i in range(len(pred_res['AAPL'])):
            d = {}
            for k, v in pred_res.items():
                d[k] = v[i]
            sorted_d = sorted(d.items(), key=lambda item: item[1], reverse=True)
            new_roi = 0.0
            for j in range(top_num):
                key = sorted_d[j][0]
                new_roi += roi / top_num * (1.0 + truth_res[key][j])
            roi = new_roi
            if with_hedging:
                roi -= sp500[i]
            print("echo %d : %f" % (i, roi))
        return roi


if __name__ == '__main__':
    roi_cal = ROICalculator(['AAPL', 'GE', 'GM', 'GOOG', 'JPM', 'KORS', 'MAR', 'MCD', 'MMM', 'TSLA'])
    print(roi_cal.calculate_roi(5))