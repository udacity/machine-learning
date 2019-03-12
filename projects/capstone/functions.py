def calculateMACD(data):
    emaslow = data.ewm(span=10, min_periods=10).mean()
    emafast = data.ewm(span=7, min_periods=7).mean()
    dif = emafast - emaslow
    MACD = dif.ewm(span=9, min_periods=9).mean()
    return dif, MACD

def calculateRSI(data, windows=10):
    delta = data.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    rUp = up.ewm(com=windows,adjust=False).mean()
    rDown = down.ewm(com=windows, adjust=False).mean().abs()
    rsi = 100 - 100 / (1 + rUp / rDown)
    return rsi

def calculateSMA(df, windows=15):
    SMA = df.rolling(window=windows, min_periods=windows, center=False).mean()
    return SMA

def calculateBB(df, windows=15):
    STD = df.rolling(window=windows,min_periods=windows, center=False).std()
    SMA = calculateSMA(df)
    upper_band = SMA + (2 * STD)
    lower_band = SMA - (2 * STD)
    return lower_band,upper_band 

def getDataForTicker(ticker):
    data = fullData[fullData['symbol'] == ticker]
    data = data.drop('symbol', 1)
    data = data.set_index('date')
    closePrices = data['close']
    data['DOF'], data['MACD'] = calculateMACD(closePrices)
    data['RSI'] = calculateRSI(closePrices)
    data['SMA'] = calculateSMA(closePrices)
    data['BBLW'],data['BBUP']  = calculateBB(closePrices)
    #fill nulls
    data = data.fillna(method="ffill") 
    data = data.fillna(method="bfill")
    data =data[17:]
    #normalize
    from sklearn import preprocessing
    x = data.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    xScaled = min_max_scaler.fit_transform(x)
    features = pd.DataFrame(columns=data.columns, data=xScaled, index=data.index)
    
    target = data['close'].shift(-1)
    target = target.fillna(method="ffill")
    x = target.values #returns a numpy array
    x = x.reshape(-1, 1)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    target = pd.DataFrame(columns=['nxtClose'], data=x_scaled, index=target.index)
    direction = 0>target['nxtClose']-features['open']
    direction = direction.values

    validation_y = target[-120:-1]
    target = target[:-120]
    validation_X = features[-120:-1]
    features = features[:-120]

    f1_validation_y=direction[-120:-1]

    return features,target,validation_X,validation_y,f1_validation_y

#FRAMEWORK FOR TRAINING AND VALIDATING MODELS
def trainAndValidateClf(clf, model_name):
    clf = trainClf(clf,timeseriesCv,model_name)
    validateResult(clf, model_name)

def trainClf(model, ts_split,model_name):
    clf = model
    
    for train_index, test_index in ts_split.split(features):
        X_train, X_test = features[:len(train_index)], features[len(train_index): (len(train_index)+len(test_index))]
        y_train, y_test = target[:len(train_index)].values.ravel(), target[len(train_index): (len(train_index)+len(test_index))].values.ravel()
        start = time.time()
        clf.fit(X_train, y_train)
        end = time.time()
        timeToFit=end-start
        global results
        results.at[model_name,'timeToFit'] = timeToFit
    return clf

def validateResult(model, model_name):
    predicted = model.predict(validation_X)
    rsmeScore = np.sqrt(mean_squared_error(validation_y, predicted))
    print('RMSE: ', rsmeScore)
    
    r2Score = r2_score(validation_y, predicted)
    print('R2 score: ', r2Score)
    
    predDirection=(predicted>validation_y['nxtClose']).values
    f1Score = f1_score(f1_validation_y, predDirection)
    print('F1 score: ', f1Score)
    
    global results
    results.at[model_name,['rmse','r2','f1']] = [rsmeScore,r2Score,f1Score]
        
    plt.figure(figsize=(21,7))
    plt.plot(validation_y.index, predicted,'B', label='Predicted Value')
    plt.plot(validation_y.index, validation_y,'R', label='Real Value')
    plt.ylabel('% Price Change')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.title(model_name + ' Predict vs Real')
    plt.legend(loc='lower right')
    plt.show()
    