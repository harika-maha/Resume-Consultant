import { useState } from 'react'

const FileUpload = ({ onFileSelect }) => {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file)
      onFileSelect(file)
    } else {
      alert('Please select a PDF file')
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    const file = e.dataTransfer.files[0]
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file)
      onFileSelect(file)
    } else {
      alert('Please select a PDF file')
    }
  }

  return (
    <div className="file-upload-container">
      <div 
        className={`file-upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          accept=".pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <label htmlFor="file-upload" className="file-upload-label">
          <div className="upload-icon">📄</div>
          <div className="upload-text">
            {selectedFile ? (
              <>
                <p><strong>{selectedFile.name}</strong></p>
                <p>Click to change file</p>
              </>
            ) : (
              <>
                <p><strong>Click to upload</strong> or drag and drop</p>
                <p>PDF files only</p>
              </>
            )}
          </div>
        </label>
      </div>
    </div>
  )
}

export default FileUpload