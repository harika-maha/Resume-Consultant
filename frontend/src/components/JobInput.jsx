const JobInput = ({ value, onChange }) => {
  return (
    <div className="job-input-container">
      <label htmlFor="job-description" className="job-input-label">
        <span>📋 Job Description</span>
      </label>
      <textarea
        id="job-description"
        className="job-input-textarea"
        placeholder="Paste the job description here...

Example:
- 3+ years of React development experience
- Strong knowledge of JavaScript, HTML, CSS
- Experience with Node.js and MongoDB
- Familiarity with AWS cloud services
- Bachelor's degree in Computer Science"
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
