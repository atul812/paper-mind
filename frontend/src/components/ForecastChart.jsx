import React from 'react'

export default function ForecastChart({ forecast }) {
  const rows = Array.isArray(forecast) && forecast.length ? forecast.slice(0, 7) : []
  const safeRows = rows.filter((item) => item?.topic_id != null && item?.predicted_score != null)
  const values = safeRows.map((item) => Number(item.predicted_score) || 0)
  const maxValue = values.length ? Math.max(...values, 1) : 1

  return (
    <div className="glass-card chart-card forecast-card">
      <div className="chart-header">
        <h2 className="chart-title">12-Month Forecast</h2>
        <span className="material-symbols-outlined">insights</span>
      </div>
      <div className="forecast-bars">
        {safeRows.length ? (
          safeRows.map((item) => {
            const score = Number(item.predicted_score) || 0
            const barHeight = (score / maxValue) * 100
            return (
              <div
                key={item.topic_id}
                className={`forecast-bar ${item.predicted_trend === '↑' ? 'growth' : ''}`}
                style={{ height: `${Math.max(30, barHeight)}%` }}
                title={`Topic ${item.topic_id} predicted ${score.toFixed(2)}`}
              />
            )
          })
        ) : (
          <div className="empty-state">Forecast results will appear after analysis.</div>
        )}
      </div>
      <div className="forecast-legend">
        <span>Current</span>
        <span className="text-tertiary">Forecasted</span>
        <span>+12M</span>
      </div>
    </div>
  )
}
