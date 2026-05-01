import { useState } from 'react'

const CreateRoomForm = () => {
  // State for form fields
  const [username, setUsername] = useState('')
  const [roomName, setRoomName] = useState('')
  const [expiryOption, setExpiryOption] = useState('20 minutes')

  const expiryOptions = ['20 minutes', '1 hour', '6 hours', '24 hours']

  return (
    <div className="min-h-screen bg-linear-to-br from-[#0A0C10] to-[#0F111A] py-8 px-4 sm:px-6 lg:px-8 flex items-center justify-center">
      <div className="w-full max-w-3xl">
        {/* Main Form Card */}
        <form className="bg-[#0F1117]/80 backdrop-blur-sm rounded-2xl border border-gray-800 shadow-2xl overflow-hidden">
          {/* Header with Module, Status, Auth Level */}
          <div className="border-b border-gray-800 bg-black/30 px-6 py-4 sm:px-8">
            <div className="flex flex-wrap justify-between items-center gap-3">
              <div className="space-y-1">
                <div className="text-xs font-mono text-indigo-400 tracking-wider">
                  MODULE:
                </div>
                <div className="text-sm sm:text-base font-bold text-cyan-300 tracking-wide">
                  INITIALIZE_ENCRYPTED_CHANNEL
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="text-xs font-mono text-gray-400">STATUS</div>
                  <div className="text-sm font-semibold text-emerald-400 flex items-center gap-1">
                    <span className="relative flex h-2 w-2">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </span>
                    STANDBY_PENDING_PARAMS
                  </div>
                </div>
                <div className="h-8 w-px bg-gray-700"></div>
                <div>
                  <div className="text-xs font-mono text-gray-400">
                    AUTH_LVL
                  </div>
                  <div className="text-lg font-mono font-bold text-yellow-400">
                    04
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Form Body */}
          <div className="p-6 sm:p-8 space-y-6">
            {/* Username Field */}
            <div>
              <label className="block text-gray-300 uppercase tracking-wide text-sm font-medium mb-2">
                ENTER YOUR USERNAME
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="ENTER_IDENTIFIER..."
                className="w-full px-4 py-3 bg-gray-900/70 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            {/* Room Name Field */}
            <div>
              <label className="block text-gray-300 uppercase tracking-wide text-sm font-medium mb-2">
                ENTER YOUR ROOM NAME
              </label>
              <input
                type="text"
                value={roomName}
                onChange={(e) => setRoomName(e.target.value)}
                placeholder="SPECIFY_LOCATION..."
                className="w-full px-4 py-3 bg-gray-900/70 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            {/* Access Key Section */}
            <div className="space-y-2">
              <label className="block text-gray-300 uppercase tracking-wide text-sm font-medium mb-1">
                CREATE A ROOM ACCESS KEY
              </label>
              <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
                <div className="flex-1 flex items-center justify-between bg-gray-900/70 border border-gray-700 rounded-xl px-4 py-3 font-mono group transition-all duration-200 hover:border-indigo-500/50">
                  <span className="text-cyan-300 text-sm sm:text-base tracking-wider truncate"></span>
                  <button
                    type="button"
                    className="ml-3 text-gray-400 hover:text-white transition-colors duration-200"
                    aria-label="Copy access key"
                  >
                    hy
                  </button>
                </div>
                <button
                  type="button"
                  className="px-5 py-3 bg-indigo-600 hover:bg-indigo-700 rounded-xl text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2 shadow-md hover:scale-[1.02]"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
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
                        ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-md ring-1 ring-indigo-500/50'
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
            <div className="bg-blue-950/30 border-l-4 border-cyan-500 rounded-lg p-4 backdrop-blur-sm">
              <div className="flex items-start gap-3">
                <svg
                  className="w-5 h-5 text-cyan-400 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clipRule="evenodd"
                  />
                </svg>
                <p className="text-sm text-gray-300 leading-relaxed">
                  before creating a room please copy the access key so that you
                  can share with your friends to join room.
                </p>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-4 bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 rounded-xl font-bold text-white shadow-lg transition-all duration-200 transform hover:scale-[1.01] focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 focus:ring-offset-[#0A0C10]"
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
