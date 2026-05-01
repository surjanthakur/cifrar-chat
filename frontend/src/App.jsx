import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { lazy } from 'react'

const MainLayout = lazy(() => import('./layouts/MainLayout.jsx'))
const HomePage = lazy(() => import('./pages/HomePage.jsx'))
const CreateRoomForm = lazy(() => import('./pages/CreateRoomFormPage.jsx'))

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/create-room" element={<CreateRoomForm />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
