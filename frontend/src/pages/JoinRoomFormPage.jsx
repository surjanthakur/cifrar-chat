import SquareBoxEffect from '../utils/SquareGradientEffect.js'

const JoinRoomForm = () => {
  return (
    <div className="relative min-h-screen bg-linear-to-br py-10 px-5 sm:px-6 lg:px-8 flex items-center justify-center">
      <div
        className={SquareBoxEffect(
          'absolute inset-0',
          'bg-size-[20px_20px]',
          'bg-[radial-gradient(#404040_1px,transparent_1px)]',
          'dark:bg-[radial-gradient(#404040_1px,transparent_1px)]',
        )}
      />
      <div className="w-full max-w-3xl">
        {/* Main Form Card */}
        <form className="bg-[#0F1117]/80 backdrop-blur-sm rounded-2xl border border-emerald-500 shadow-2xl overflow-hidden">
          <div className="p-6 sm:p-8 space-y-6">
            {/* Username Field */}
            <div>
              <label className="block text-gray-300  tracking-wide text-sm font-medium mb-2">
                enter your username
              </label>
              <input
                type="text"
                placeholder="ENTER_IDENTIFIER..."
                className="w-full px-4 py-3 bg-gray-900/70 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent transition-all duration-200"
              />
            </div>

            {/* Access Key Section */}
            <div className="space-y-2">
              <label className="block text-gray-300  tracking-wide text-sm font-medium mb-1">
                enter room key to join a room
              </label>
              <input
                className="flex-1 flex items-center justify-between bg-gray-900/70 border border-gray-700 rounded-xl px-4 py-3 group transition-all duration-200 focus:ring-green-500 hover:border-green-400"
                placeholder="enter key..."
              ></input>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-4 bg-linear-to-r from-green-600 to-green-700 hover:from-green-500 hover:to-green-600 rounded-xl font-bold text-white shadow-lg transition-all duration-200 transform hover:scale-[1.01] focus:ring-2 focus:ring-green-400 focus:ring-offset-2 focus:ring-offset-[#0A0C10]"
            >
              JOIN A SECURE ROOM
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default JoinRoomForm
