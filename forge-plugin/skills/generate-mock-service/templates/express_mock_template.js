// Express.js Mock Server Template
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || {{PORT}};

// Middleware
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Simulated delay middleware
const delay = (ms) => (req, res, next) => {
  setTimeout(next, ms);
};

app.use(delay(process.env.MOCK_DELAY_MS || 100));

// In-memory data store
const dataStore = {
  // {{DATA_STORE}}
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    service: '{{SERVICE_NAME}}',
    timestamp: new Date().toISOString()
  });
});

// {{ENDPOINT_NAME}} - GET
app.get('/{{ENDPOINT_PATH}}', (req, res) => {
  // Query parameters
  const { page = 1, limit = 10 } = req.query;
  
  // Simulate different scenarios based on query params
  const scenario = req.query.scenario || req.headers['x-mock-scenario'];
  
  if (scenario === 'error') {
    return res.status(500).json({
      error: 'internal_server_error',
      message: 'Simulated server error'
    });
  }
  
  // Success response
  res.json({
    data: [], // {{RESPONSE_DATA}}
    page: parseInt(page),
    limit: parseInt(limit),
    total: 0
  });
});

// {{ENDPOINT_NAME}} - GET by ID
app.get('/{{ENDPOINT_PATH}}/:id', (req, res) => {
  const { id } = req.params;
  
  // Check if item exists
  const item = dataStore[id];
  
  if (!item) {
    return res.status(404).json({
      error: 'not_found',
      message: `Item ${id} not found`
    });
  }
  
  res.json(item);
});

// {{ENDPOINT_NAME}} - POST
app.post('/{{ENDPOINT_PATH}}', (req, res) => {
  const data = req.body;
  
  // Validation
  if (!data || Object.keys(data).length === 0) {
    return res.status(400).json({
      error: 'validation_error',
      message: 'Request body is required'
    });
  }
  
  // Simulate specific error scenarios
  if (data.trigger_error) {
    return res.status(422).json({
      error: 'unprocessable_entity',
      message: 'Unable to process request',
      details: data.trigger_error
    });
  }
  
  // Create new item
  const id = `id_${Date.now()}`;
  const newItem = {
    id,
    ...data,
    created_at: new Date().toISOString()
  };
  
  dataStore[id] = newItem;
  
  res.status(201).json(newItem);
});

// {{ENDPOINT_NAME}} - PUT
app.put('/{{ENDPOINT_PATH}}/:id', (req, res) => {
  const { id } = req.params;
  const data = req.body;
  
  if (!dataStore[id]) {
    return res.status(404).json({
      error: 'not_found',
      message: `Item ${id} not found`
    });
  }
  
  const updatedItem = {
    ...dataStore[id],
    ...data,
    updated_at: new Date().toISOString()
  };
  
  dataStore[id] = updatedItem;
  
  res.json(updatedItem);
});

// {{ENDPOINT_NAME}} - DELETE
app.delete('/{{ENDPOINT_PATH}}/:id', (req, res) => {
  const { id } = req.params;
  
  if (!dataStore[id]) {
    return res.status(404).json({
      error: 'not_found',
      message: `Item ${id} not found`
    });
  }
  
  delete dataStore[id];
  
  res.status(204).send();
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'internal_server_error',
    message: err.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'not_found',
    message: `Endpoint ${req.method} ${req.path} not found`
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🎭 Mock Service: {{SERVICE_NAME}}`);
  console.log(`📍 Running on port: ${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`\nAvailable endpoints:`);
  console.log(`  GET    http://localhost:${PORT}/{{ENDPOINT_PATH}}`);
  console.log(`  GET    http://localhost:${PORT}/{{ENDPOINT_PATH}}/:id`);
  console.log(`  POST   http://localhost:${PORT}/{{ENDPOINT_PATH}}`);
  console.log(`  PUT    http://localhost:${PORT}/{{ENDPOINT_PATH}}/:id`);
  console.log(`  DELETE http://localhost:${PORT}/{{ENDPOINT_PATH}}/:id`);
  console.log(`\nMock delay: ${process.env.MOCK_DELAY_MS || 100}ms`);
});

module.exports = app;
