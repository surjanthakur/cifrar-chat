import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { lazy } from 'react'
import { HomePage, CreateRoomForm, JoinRoomForm } from './pages/ExportFiles.js'

const MainLayout = lazy(() => import('./layouts/MainLayout.jsx'))

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/create-room" element={<CreateRoomForm />} />
            <Route path="/join-room" element={<JoinRoomForm />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
