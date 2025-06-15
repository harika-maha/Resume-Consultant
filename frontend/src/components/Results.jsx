const Results = ({ analysis }) => {
  if (!analysis) return null

  const getMatchColor = (percentage) => {
    if (percentage >= 80) return '#4CAF50'
    if (percentage >= 60) return '#FF9800'
    return '#F44336'
  }

  const getMatchLabel = (percentage) => {
    if (percentage >= 80) return 'Excellent Match'
    if (percentage >= 60) return 'Good Match'
    return 'Needs Improvement'
  }

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>📊 Analysis Results</h2>
      </div>

      {/* Match Score Circle */}
      <div className="match-score-section">
        <div 
          className="match-circle"
          style={{ borderColor: getMatchColor(analysis.matchPercentage || 60) }}
        >
          <div className="match-percentage">
            {analysis.matchPercentage || 60}%
          </div>
          <div className="match-label">
            {getMatchLabel(analysis.matchPercentage || 60)}
          </div>
        </div>
      </div>

      {/* Summary */}
      {analysis.summary && (
        <div className="summary-section">
          <h3>📝 Summary</h3>
          <p className="summary-text">{analysis.summary}</p>
        </div>
      )}

      {/* AI Analysis - if it's the full text response */}
      {analysis.aiAnalysis && (
        <div className="ai-analysis-section">
          <h3>🤖 AI Analysis</h3>
          <div className="ai-analysis-text">
            {analysis.aiAnalysis.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>
      )}

      {/* Structured Results Grid */}
      <div className="results-grid">
        {/* Strengths */}
        {analysis.strengths && analysis.strengths.length > 0 && (
          <div className="result-card strengths">
            <h3>✅ Your Strengths</h3>
            <ul>
              {analysis.strengths.map((strength, index) => (
                <li key={index}>{strength}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Missing Skills */}
        {analysis.missingSkills && analysis.missingSkills.length > 0 && (
          <div className="result-card missing-skills">
            <h3>🎯 Missing Skills</h3>
            <ul>
              {analysis.missingSkills.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Improvements */}
        {analysis.improvements && analysis.improvements.length > 0 && (
          <div className="result-card improvements">
            <h3>💡 Improvements</h3>
            <ul>
              {analysis.improvements.map((improvement, index) => (
                <li key={index}>{improvement}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button className="btn-secondary" onClick={() => window.print()}>
          📄 Print Report
        </button>
        <button className="btn-primary" onClick={() => window.location.reload()}>
          🔄 Analyze Another Resume
        </button>
      </div>
    </div>
  )
}

export default Results