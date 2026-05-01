import { Navbar, Footer } from "../components/ExportFiles";
import { Outlet } from "react-router-dom";

const MainLayout = () => {
  return (
    <div className="min-h-scree flex flex-col">
      {/* header */}
      <Navbar />
      {/* main content */}
      <main className="flex-1 w-full">
        <div className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>

      {/* footer */}
      <Footer />
    </div>
  );
};

export default MainLayout;
