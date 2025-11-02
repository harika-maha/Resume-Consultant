import { useState } from 'react'
import FileUpload from './components/FileUpload'
import JobInput from './components/JobInput'
import Results from './components/Results'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)

  const API_URL = import.meta.env.VITE_API_URL

  const handleAnalyze = async () => {
    console.log('Analyze button clicked!')
    if (!file || !jobDescription) {
      console.log('Missing file or job description')
      return
    }
    
    setLoading(true)
    const formData = new FormData()
    formData.append('resume', file)
    formData.append('jd', jobDescription)

    try {
      const response = await fetch(`${API_URL}/match_resume`, {
        method: 'POST',
        body: formData
      })
      console.log('Response status:', response.status)
      const result = await response.json()
      console.log('API result:', result)
      setAnalysis(result.analysis)
    } catch (error) {
      console.error('Error:', error)
    }
    setLoading(false)
  }

  const testClick = () => {
  console.log('Button clicked!')
  alert('Button works!')
}

  return (
    <div className="App">
      <div className="header-section">
        <h1>Resume Consultant</h1>
        <p className="subtitle">AI-powered resume analysis and job matching</p>
      </div>
      <FileUpload onFileSelect={setFile} />
      <JobInput value={jobDescription} onChange={setJobDescription} />
      <button onClick={handleAnalyze} disabled={loading || !file || !jobDescription}>
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </button>
      {analysis && <Results analysis={analysis} />}
    </div>
  )
}

export default App