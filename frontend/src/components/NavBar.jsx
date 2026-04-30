import { useState, useEffect } from 'react'
import { FaGithub, FaUser } from 'react-icons/fa'
import websiteLogo from '../assets/main-logo.ico'

const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  // Close mobile menu when window is resized to desktop breakpoint
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setIsMobileMenuOpen(false)
      }
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  // Toggle mobile menu
  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen)
  }

  // Close mobile menu when a link is clicked
  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false)
  }

  // Navigation links data
  const navLinks = [
    { name: 'ABOUT US', href: '/about' },
    {
      name: 'GITHUB',
      href: 'https://github.com/surjanthakur/cifrar-chat',
      external: true,
    },
  ]

  return (
    <nav className="sticky top-0 z-50 bg-slate-950/50 backdrop-blur-2xl border-b border-white/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 md:h-20">
          {/* Logo / Brand */}
          <div className="shrink-0">
            <a
              href="/"
              className="text-white text-2xl md:text-3xl font-bold tracking-tight hover:text-green-400 transition-colors duration-200"
            >
              <img
                src={websiteLogo}
                alt="Cifrar Logo"
                className="h-10 w-auto inline-block mr-2"
              />
              CIFRAR
            </a>
          </div>

          {/* Desktop Navigation - hidden on mobile */}
          <div className="hidden md:flex md:items-center md:space-x-8">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                target={link.external ? '_blank' : '_self'}
                rel={link.external ? 'noopener noreferrer' : undefined}
                className="text-gray-300 hover:text-white uppercase tracking-wide text-sm font-medium transition-all duration-200 hover:scale-105 hover:border-b-2 hover:border-green-500 pb-1"
              >
                <span className="flex items-center gap-2">
                  {link.name === 'GITHUB' && <FaGithub size={20} />}
                  {link.name === 'ABOUT US' && <FaUser size={20} />}
                  {link.name}
                </span>
              </a>
            ))}
          </div>

          {/* Mobile menu button - visible only on mobile */}
          <div className="md:hidden">
            <button
              onClick={toggleMobileMenu}
              type="button"
              className="text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-green-500 rounded-md p-2 transition-colors duration-200"
              aria-label="Toggle menu"
            >
              {isMobileMenuOpen ? (
                /* Close icon (X) */
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                /* Hamburger menu icon */
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu - slide down transition */}
      <div
        className={`md:hidden transition-all duration-300 ease-in-out overflow-hidden ${
          isMobileMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="px-4 pt-2 pb-4 space-y-3 bg-[#0A0C10] border-t border-gray-800 shadow-lg">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              target={link.external ? '_blank' : '_self'}
              rel={link.external ? 'noopener noreferrer' : undefined}
              onClick={closeMobileMenu}
              className="text-gray-300 hover:text-white hover:bg-gray-800/50 block px-3 py-2 rounded-md text-base uppercase tracking-wide font-medium transition-colors duration-200"
            >
              <span className="flex items-center gap-3">
                {link.name === 'GITHUB' && <FaGithub size={20} />}
                {link.name === 'ABOUT US' && <FaUser size={20} />}
                {link.name}
              </span>
            </a>
          ))}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
