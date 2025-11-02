const JobInput = ({ value, onChange }) => {
  return (
    <div className="job-input-container">
      <label htmlFor="job-description" className="job-input-label">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
          <polyline points="10 9 9 9 8 9" />
        </svg>
        <span>Job Description</span>
      </label>
      <textarea
        id="job-description"
        className="job-input-textarea"
        placeholder="Paste the job description here...

Example:
• 3+ years of React development experience
• Strong knowledge of JavaScript, HTML, CSS
• Experience with Node.js and MongoDB
• Familiarity with AWS cloud services
• Bachelor's degree in Computer Science"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={8}
      />
      <div className="char-count">
        {value.length} characters
      </div>
    </div>
  )
}

export default JobInput
