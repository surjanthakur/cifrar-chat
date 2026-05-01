import { useState } from 'react'
import { FaInfoCircle } from 'react-icons/fa'
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

function cn(...inputs) {
  return twMerge(clsx(inputs))
}

const CreateRoomForm = () => {
  const [expiryOption, setExpiryOption] = useState('20 minutes')
  const expiryOptions = ['20 minutes', '1 hour', '6 hours', '24 hours']

  return (
    <div className="relative min-h-screen bg-linear-to-br py-8 px-4 sm:px-6 lg:px-8 flex items-center justify-center">
      <div
        className={cn(
          'absolute inset-0',
          'bg-size-[20px_20px]',
          'bg-[radial-gradient(#404040_1px,transparent_1px)]',
          'dark:bg-[radial-gradient(#404040_1px,transparent_1px)]',
        )}
      />
      <div className="w-full max-w-3xl">
        {/* Main Form Card */}
        <form className="bg-[#0F1117]/80 backdrop-blur-sm rounded-2xl border border-emerald-500 shadow-2xl overflow-hidden">
          {/* Form Body */}
          <div className="p-6 sm:p-8 space-y-6">
            {/* Username Field */}
            <div>
              <label className="block text-gray-300 uppercase tracking-wide text-sm font-medium mb-2">
                ENTER YOUR USERNAME
              </label>
              <input
                type="text"
                placeholder="ENTER_IDENTIFIER..."
                className="w-full px-4 py-3 bg-gray-900/70 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent transition-all duration-200"
              />
            </div>

            {/* Room Name Field */}
            <div>
              <label className="block text-gray-300 uppercase tracking-wide text-sm font-medium mb-2">
                ENTER YOUR ROOM NAME
              </label>
              <input
                type="text"
                placeholder="SPECIFY_LOCATION..."
                className="w-full px-4 py-3 bg-gray-900/70 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            {/* Access Key Section */}
            <div className="space-y-2">
              <label className="block text-gray-300 uppercase tracking-wide text-sm font-medium mb-1">
                GENERATE A ROOM ACCESS KEY
              </label>
              <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
                {/* Access Key Display */}
                <input
                  className="flex-1 flex items-center justify-between bg-gray-900/70 border border-gray-700 rounded-xl px-4 py-3 group transition-all duration-200 focus:ring-green-500 hover:border-green-400"
                  placeholder="ACCESS_KEY..."
                  readOnly
                ></input>

                {/* generate key button */}
                <button
                  type="button"
                  className="px-5 py-3 bg-green-600 hover:bg-green-700 rounded-xl text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2 shadow-md hover:scale-[1.02]"
                >
                  generate key
                </button>
              </div>
            </div>

            {/* Room Expiry Date Options */}
            <div>
              <label className="block text-gray-300 uppercase tracking-wide text-sm font-medium mb-3">
                ROOM EXPIRY DATE
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {expiryOptions.map((option) => (
                  <label
                    key={option}
                    className={`flex items-center justify-center gap-2 px-3 py-2 rounded-xl border cursor-pointer transition-all duration-200 ${
                      expiryOption === option
                        ? 'bg-green-600/20 border-green-500 text-white shadow-md ring-1 ring-green-500/50'
                        : 'bg-gray-900/50 border-gray-700 text-gray-300 hover:bg-gray-800/70 hover:border-gray-600'
                    }`}
                  >
                    <input
                      type="radio"
                      name="expiry"
                      value={option}
                      checked={expiryOption === option}
                      onChange={(e) => setExpiryOption(e.target.value)}
                      className="sr-only"
                    />
                    <span className="text-sm font-medium">{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Info Note */}
            <div className="bg-green-950/90 border-l-4 border-green-500 rounded-lg p-4 backdrop-blur-sm">
              <div className="flex items-start gap-3">
                <FaInfoCircle size={25} />
                <p className="text-sm text-gray-300 leading-relaxed">
                  before creating a room please copy the access key so that you
                  can share with your friends to join room.
                </p>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-4 bg-linear-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 rounded-xl font-bold text-white shadow-lg transition-all duration-200 transform hover:scale-[1.01] focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-[#0A0C10]"
            >
              CREATE A SECURE ROOM
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateRoomForm
