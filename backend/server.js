const express = require('express')
const cors = require('cors')
const fs = require('fs')
const path = require('path')
const csv = require('csv-parser')

const app = express()
const PORT = 3001

app.use(cors())
app.use(express.json())

app.get('/', (req, res) => {
  res.send('GradeCastify backend is running')
})

app.get('/api/courses', (req, res) => {
  const results = []
  const filePath = path.join(__dirname, 'data', 'courses.csv')

  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (data) => {
      results.push({
        course: data.course,
        current: data.current === '' || data.current == null ? null : Number(data.current),
        attendance: data.attendance === '' || data.attendance == null ? null : Number(data.attendance),
        midterm_score: data.midterm_score === '' || data.midterm_score == null ? null : Number(data.midterm_score),
        assignments_avg: data.assignments_avg === '' || data.assignments_avg == null ? null : Number(data.assignments_avg),
        quizzes_avg: data.quizzes_avg === '' || data.quizzes_avg == null ? null : Number(data.quizzes_avg),
        participation_score: data.participation_score === '' || data.participation_score == null ? null : Number(data.participation_score),
        projects_score: data.projects_score === '' || data.projects_score == null ? null : Number(data.projects_score),
        predicted_grade: data.predicted_grade || ''
      })
    })
    .on('end', () => {
      console.log('[GET] /api/courses ->', results)
      res.json(results)
    })
    .on('error', (err) => {
      console.log('CSV read error:', err)
      res.status(500).json({ error: 'Failed to read courses.csv' })
    })
})

app.post('/api/courses', (req, res) => {
  const filePath = path.join(__dirname, 'data', 'courses.csv')

  console.log('[POST] req.body =', req.body)
  console.log('[POST] filePath =', filePath)

  const {
    course,
    current,
    attendance,
    midterm_score,
    assignments_avg,
    quizzes_avg,
    participation_score,
    projects_score,
    predicted_grade
  } = req.body

  const row = [
    course ?? '',
    current ?? '',
    attendance ?? '',
    midterm_score ?? '',
    assignments_avg ?? '',
    quizzes_avg ?? '',
    participation_score ?? '',
    projects_score ?? '',
    predicted_grade ?? ''
  ].join(',') + '\n'

  console.log('[POST] row =', row)

  fs.appendFile(filePath, row, (err) => {
    if (err) {
      console.log('[POST] CSV write error:', err)
      return res.status(500).json({ error: 'Failed to save courses.csv' })
    }

    console.log('[POST] csv append success')
    res.json({ success: true })
  })
})

app.delete('/api/courses/:id', (req, res) => {
  const filePath = path.join(__dirname, 'data', 'courses.csv')
  const courseId = req.params.id

  fs.readFile(filePath, 'utf8', (err, fileData) => {
    if (err) {
      console.log('[DELETE] CSV read error:', err)
      return res.status(500).json({ error: 'Failed to read courses.csv' })
    }

    const lines = fileData.trim().split('\n')
    const header = lines[0]
    const rows = lines.slice(1)

    const index = Number(courseId.replace('demo-', ''))

    if (Number.isNaN(index) || index < 0 || index >= rows.length) {
      return res.status(400).json({ error: 'Invalid course id' })
    }

    rows.splice(index, 1)

    const updatedCsv = [header, ...rows].join('\n') + '\n'

    fs.writeFile(filePath, updatedCsv, (writeErr) => {
      if (writeErr) {
        console.log('[DELETE] CSV write error:', writeErr)
        return res.status(500).json({ error: 'Failed to update courses.csv' })
      }

      console.log('[DELETE] csv delete success:', courseId)
      res.json({ success: true })
    })
  })
})

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`)
})