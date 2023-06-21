import React from 'react'
import ReactDOM from 'react-dom/client'
import Dashboard from './dashboard/Dashboard'
import './main.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Dashboard />
  </React.StrictMode>,
)
