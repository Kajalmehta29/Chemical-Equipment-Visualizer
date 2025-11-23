import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import './App.css';

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => { fetchHistory(); }, []);

  const fetchHistory = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/history/');
      setHistory(res.data);
    } catch (err) { console.error(err); }
  };
const loadHistoryItem = async (id) => {
    if (!username || !password) {
      alert("Please login to view history details.");
      return;
    }
    
    try {
      const res = await axios.get(`http://127.0.0.1:8000/api/history/${id}/`, {
        auth: { username, password }
      });
      setStats(res.data);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      console.error(err);
      alert("Failed to load history data.");
    }
  };
  const onUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }
    if (!username || !password) {
      alert("Please enter a username and password.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
        auth: {
          username: username,
          password: password 
        }
      });
      
      setStats(res.data);
      fetchHistory();
      alert("Upload Successful!"); 
    } catch (err) { 
      console.error(err);
      if (err.response && err.response.status === 401) {
        alert("Login Failed: Incorrect Username or Password.");
      } else {
        alert("Upload failed. Check console for details."); 
      }
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Chemical Equipment Visualizer</h1>
      </header>
      
      {/* Upload & Login Section */}
      <div className="card">
        <h2 className="section-title">Data Upload & Authentication</h2>
        
        {/* Login Inputs */}
        <div style={{ marginBottom: '20px', display: 'flex', gap: '15px', justifyContent: 'center' }}>
            <input 
              type="text" 
              placeholder="Username (admin)" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ddd' }}
            />
            <input 
              type="password" 
              placeholder="Password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ddd' }}
            />
        </div>

        <div className="upload-controls">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} accept=".csv" />
          <button className="btn" onClick={onUpload}>Analyze CSV</button>
          <a href="http://127.0.0.1:8000/api/report/" target="_blank" rel="noreferrer">
             <button className="btn btn-secondary">Download PDF Report</button>
          </a>
        </div>
      </div>

      {/* Stats and Charts */}
      {stats && (
        <div className="dashboard-grid">
          <div className="card">
            <h2 className="section-title">Parameter Statistics
              {stats.filename && (
                <span style={{ 
                  fontSize: '0.9rem', 
                  color: '#008080', 
                  marginLeft: '15px', 
                  fontWeight: 'normal' 
                }}>
                  (File: {stats.filename})
                </span>
              )}
            </h2>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Total Records</span>
                <span className="stat-value">{stats.total_count}</span>
              </div>
              {Object.entries(stats.averages).map(([key, val]) => (
                <div className="stat-item" key={key}>
                  <span className="stat-label">Avg {key}</span>
                  <span className="stat-value">{val.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h2 className="section-title">Type Distribution</h2>
            <div style={{ height: '250px', display: 'flex', justifyContent: 'center' }}>
              <Pie data={{
                labels: Object.keys(stats.type_distribution),
                datasets: [{
                  data: Object.values(stats.type_distribution),
                  backgroundColor: ['#008080', '#2c3e50', '#f1c40f', '#e74c3c', '#95a5a6'],
                  borderWidth: 1
                }]
              }} options={{ maintainAspectRatio: false }} />
            </div>
          </div>
        </div>
      )}

      {/* History Section */}
  <div className="card">
        <h2 className="section-title">Recent Upload History</h2>
        <p style={{fontSize: '0.9rem', color: '#666', marginBottom: '15px'}}>
           Click on any item below to view its charts and summary.
        </p>
        
        {history.length === 0 ? (
          <p style={{ color: '#888', textAlign: 'center' }}>No uploads yet.</p>
        ) : (
          <ul className="history-list">
            {history.map((h) => (
              <li className="history-item" key={h.id} 
                  style={{cursor: 'pointer', transition: 'background 0.2s'}}
                  onClick={() => loadHistoryItem(h.id)} 
                  onMouseOver={(e) => e.currentTarget.style.background = '#f0f8ff'}
                  onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
              >
                <div>
                  <span className="file-name" style={{color: '#008080', fontWeight: 'bold'}}>
                    📊 {h.filename}
                  </span>
                  <br/>
                  <span className="file-date">{new Date(h.uploaded_at).toLocaleString()}</span>
                </div>
                <button className="btn btn-secondary" style={{padding: '5px 10px', fontSize: '0.8rem'}}>
                  View
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;