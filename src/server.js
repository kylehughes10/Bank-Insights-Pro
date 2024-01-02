const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();

// Middlewares
app.use(cors());
app.use(bodyParser.json()); // for parsing application/json

// Handle POST request to '/run-ubpr'
app.post('/run-ubpr', (req, res) => {
  // Extract CERT numbers from the request body
  const certs = req.body.certs;

  // Define the path to your Python script
  const scriptPath = 'C:/Users/kyleh/OneDrive/Documents/YouTube/UBPR/ubpr-report-generator/src/ubpr.py';

  // Check if the file exists
  if (!fs.existsSync(scriptPath)) {
    return res.status(400).json({ message: 'ubpr.py script not found at the provided path' });
  }

  // Spawn a child process to run the Python script
  const pythonProcess = spawn('python', [scriptPath, ...certs]);

  // Collect data from script
  let scriptOutput = '';
  pythonProcess.stdout.on('data', (data) => {
    scriptOutput += data.toString();
  });

  // Collect error from script (if any)
  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  // On script completion
  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ message: 'Failed to run script', error: scriptOutput });
    }
    res.status(200).json({ message: 'Report Generated Successfully', output: scriptOutput });
  });
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});
