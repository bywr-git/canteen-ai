import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from "./pages/Dashboard";
import Login from './pages/Login'
import Register from './pages/Register'
import Food from './pages/Food'
import Purchases from './pages/Purchases'
import Budget from './pages/Budget'
import { AuthProvider, RequireAuth } from './hooks/AuthProvider'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<RequireAuth><Dashboard /></RequireAuth>} />
          <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
          <Route path="/food" element={<RequireAuth><Food /></RequireAuth>} />
          <Route path="/purchases" element={<RequireAuth><Purchases /></RequireAuth>} />
          <Route path="/budget" element={<RequireAuth><Budget /></RequireAuth>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App;