import React from 'react'

export default function MomentumChart({ momentum }) {
  const rows = Array.isArray(momentum) && momentum.length ? momentum.slice(0, 5) : []
  const safeRows = rows.filter((item) => item?.topic_id != null)

  const formatTrend = (trend) => {
    if (trend === '↑') return 'Growing'
    if (trend === '↓') return 'Declining'
    return 'Stable'
  }

  return (
    <div className="glass-card chart-card">
      <div className="chart-header">
        <h2 className="chart-title">Momentum Analysis</h2>
        <span className="material-symbols-outlined">bolt</span>
      </div>
      <div className="chart-body momentum-card">
        {safeRows.length ? (
          safeRows.map((item) => {
            const momentumValue = Number(item.momentum ?? 0)
            const score = Math.min(100, Math.abs(momentumValue) * 10 + 10)
            const publicationVelocity = Number(item.publication_velocity ?? 0).toFixed(2)
            const citationVelocity = Number(item.citation_velocity ?? 0).toFixed(2)
            return (
              <div key={item.topic_id} className="progress-item">
                <div className="progress-title">
                  <span>Topic {item.topic_id}</span>
                  <span>{formatTrend(item.momentum_trend)}</span>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${score}%` }} />
                </div>
                <div className="progress-title" style={{ justifyContent: 'space-between' }}>
                  <span>Pub: {publicationVelocity}</span>
                  <span>Cit: {citationVelocity}</span>
                </div>
              </div>
            )
          })
        ) : (
          <div className="empty-state">Analyze data to view momentum breakdown.</div>
        )}
      </div>
    </div>
  )
}
