import { FaGithub, FaDiscord, FaXTwitter } from 'react-icons/fa6'

const Footer = () => {
  return (
    <footer className="relative w-full h-120 overflow-hidden">
      {/* Large CIFRAR Text Background */}
      <div className="absolute inset-0 flex items-center justify-center">
        <h1 className="text-[30vw] font-bold tracking-tight bg-linear-to-r from-emerald-500 to-cyan-400 bg-clip-text text-transparent">
          CIFRAR
        </h1>
      </div>

      {/* Social Icons at Top Right */}
      <div className="absolute top-4 right-6 flex gap-6">
        <a
          href="#"
          className="group text-gray-400 hover:text-emerald-400 transition-all duration-300 hover:scale-105"
          aria-label="GitHub"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaGithub className="text-2xl" />
        </a>
        <a
          href="#"
          className="group text-gray-400 hover:text-emerald-400 transition-all duration-300 hover:scale-105"
          aria-label="X Profile"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaXTwitter className="text-xl" />
        </a>
        <a
          href="#"
          className="group text-gray-400 hover:text-emerald-400 transition-all duration-300 hover:scale-105"
          aria-label="Discord"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaDiscord className="text-2xl" />
        </a>
      </div>

      {/* Means to Encrypt at Bottom Center */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <p className="text-white text-lg uppercase tracking-[0.2em] font-mono">
          MEANS TO ENCRYPT
        </p>
      </div>
    </footer>
  )
}

export default Footer
