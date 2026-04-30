import FeaturesSection from './FeatureSection.jsx'
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

function cn(...inputs) {
  return twMerge(clsx(inputs))
}

const HomePage = () => {
  return (
    <>
      <section className="relative min-h-screen w-full overflow-hidden bg-black font-sans antialiased">
        {/* Dotted Background Pattern */}
        <div
          className={cn(
            'absolute inset-0',
            'bg-size-[20px_20px]',
            'bg-[radial-gradient(#404040_1px,transparent_1px)]',
            'dark:bg-[radial-gradient(#404040_1px,transparent_1px)]',
          )}
        />

        {/* Radial fade effect for edges */}
        <div className="pointer-events-none absolute inset-0 flex items-center justify-center bg-black mask-[radial-gradient(ellipse_at_center,transparent_20%,black)] " />

        {/* Main content */}
        <div className="relative z-10 mx-auto flex min-h-screen flex-col items-center justify-center px-5 py-20 text-center md:px-8 lg:px-12">
          <div className="mx-auto flex w-full max-w-5xl flex-col items-center">
            {/* Top tagline with pill design */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-green-500/30 bg-black/60 px-5 py-2 text-sm font-medium uppercase tracking-wider text-green-400 shadow-lg shadow-green-500/10 backdrop-blur-sm md:mb-8">
              <span className="inline-block h-2 w-2 rounded-full bg-green-400 shadow-glow"></span>
              <span>🔒 no one see what you do here</span>
              <span className="inline-block h-2 w-2 rounded-full bg-green-400 shadow-glow"></span>
            </div>

            {/* Main heading */}
            <h1 className="mb-4 text-4xl font-black leading-tight tracking-tight md:text-8xl lg:text-9xl">
              <span className="block bg-linear-to-r from-gray-100 to-gray-300 bg-clip-text text-transparent">
                PRIVACY WITH
              </span>
              <span className="relative mt-2 inline-block bg-linear-to-r from-green-400 via-emerald-400 to-green-300 bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(74,222,128,0.3)]">
                ENCRYPTED CHATS
                <span className="absolute -bottom-2 left-0 h-0.75 w-full bg-linear-to-r from-transparent via-green-400 to-transparent opacity-70"></span>
              </span>
            </h1>

            {/* Call to action buttons */}
            <div className="mt-12 flex w-full flex-col items-center justify-center gap-7 sm:flex-row sm:gap-6">
              {/* create room button */}
              <button className="group relative w-full overflow-hidden border border-green-500/60 bg-black/40 px-8 py-10 text-base font-semibold uppercase tracking-wider text-green-400 transition-all duration-300 hover:border-green-400 hover:bg-green-500 hover:text-black sm:w-auto sm:px-10 md:px-12 md:text-lg">
                <span className="relative z-10 flex items-center justify-center gap-2">
                  <span>CREATE A PRIVATE ROOM</span>
                  <span className="transition-transform duration-300 group-hover:translate-x-2">
                    →
                  </span>
                </span>
                <span className="absolute inset-0 z-0 bg-linear-to-r from-green-400 to-emerald-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></span>
              </button>

              {/* join room button */}
              <button className="group w-full border border-red-500/40 bg-transparent px-8 py-10 text-base font-semibold uppercase tracking-wider text-white-400 backdrop-blur-sm transition-all duration-300 hover:border-red-400 hover:bg-red-500/70 hover:text-white sm:w-auto sm:px-10 md:px-12 md:text-lg">
                <span className="flex items-center justify-center gap-2">
                  <span>JOIN A PRIVATE ROOM</span>
                  <span className="opacity-70 transition-transform duration-300 group-hover:translate-x-2">
                    ↗
                  </span>
                </span>
              </button>
            </div>
          </div>
        </div>
      </section>
      <FeaturesSection />
    </>
  )
}

export default HomePage
