from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_topics(tfidf_matrix,horizon_months=12):
    forecasts=[]
    for topic in tfidf_matrix.topic_id.unique():

        df=tfidf_matrix[tfidf_matrix.topic_id==topic].sort_values("window")
        y=df["score"].values

        if len(y)<2:
            continue

        x=np.arange(len(y)).reshape(-1,1)

        model=LinearRegression()
        model.fit(x,y)
        future=np.array([
            [len(y)+(horizon_months//6)]
        ])
        pred=model.predict(future)[0]

        if pred>y[-1]:
            predicted_trend="↑"

        elif pred<y[-1]:
            predicted_trend="↓"

        else:
            predicted_trend="→"

        forecasts.append({
            "topic_id":topic,
            "current_score":float(y[-1]),
            "predicted_score":float(pred),
            "predicted_trend":predicted_trend
        })
    return forecasts