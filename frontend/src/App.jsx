import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { lazy } from 'react'

const MainLayout = lazy(() => import('./layouts/MainLayout.jsx'))
const HomePage = lazy(() => import('./pages/HomePage.jsx'))

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route path="/" element={<HomePage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
