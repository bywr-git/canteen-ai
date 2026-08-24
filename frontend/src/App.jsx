import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from "./pages/Dashboard";
import Login from './pages/Login'
import Register from './pages/Register'
import { AuthProvider, RequireAuth } from './hooks/AuthProvider'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<RequireAuth><Dashboard /></RequireAuth>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App;