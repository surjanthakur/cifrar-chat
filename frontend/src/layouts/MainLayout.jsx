import { Navbar, Footer } from '../components/ExportFiles'
import { Outlet } from 'react-router-dom'

const MainLayout = () => {
  return (
    <>
      <div className="min-h-screen flex flex-col">
        {/* header */}
        <Navbar />
        {/* main content */}
        <main>
          <Outlet />
        </main>
        {/* footer */}
        <Footer />
      </div>
    </>
  )
}

export default MainLayout
