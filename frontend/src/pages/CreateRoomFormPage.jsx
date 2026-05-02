import { useForm } from "react-hook-form";
import { FaShieldAlt, FaBolt, FaInfoCircle } from "react-icons/fa";
import SquareBoxEffect from "../utils/SquareGradientEffect";

const CreateRoomForm = () => {
  const {
    register,
    formState: { errors },
  } = useForm({
    defaultValues: {
      username: "",
      roomName: "",
    },
  });

  return (
    <section className="min-h-screen flex items-center justify-center p-4 relative">
      {/* Dotted Background Pattern */}
      <div
        className={SquareBoxEffect(
          "absolute inset-0",
          "bg-size-[20px_20px]",
          "bg-[radial-gradient(#404040_1px,transparent_1px)]",
          "dark:bg-[radial-gradient(#404040_1px,transparent_1px)]",
        )}
        style={{ zIndex: 0 }}
      />
      {/* Radial fade effect for edges */}
      <div
        className="pointer-events-none absolute inset-0 flex items-center justify-center bg-black mask-[radial-gradient(ellipse_at_center,transparent_40%,black)]"
        style={{ zIndex: 1 }}
      />
      <div className="w-full max-w-xl border border-green-500/30 rounded-xl overflow-hidden bg-zinc-900/90 shadow-xl relative z-10">
        {/* Header */}
        <div className="border-b border-green-500/30 px-6 py-4 flex items-center justify-between bg-zinc-950/80">
          <h1 className="text-xl font-bold tracking-widest">
            CREATE SECURE ROOM
          </h1>
          <div className="text-green-500">
            <FaShieldAlt size={28} />
          </div>
        </div>

        <form className="p-6 space-y-8" autoComplete="off">
          {/* Username Field */}
          <div>
            <label
              className="block text-sm font-medium mb-2 tracking-wider"
              htmlFor="username-input"
            >
              ENTER YOUR USERNAME
            </label>
            <input
              id="username-input"
              type="text"
              {...register("username", { required: "Username is required" })}
              placeholder="ENTER_IDENTIFIER..."
              className="w-full bg-zinc-900 border border-green-500/50 focus:border-green-400 text-green-300 placeholder:text-green-700/70 rounded-lg px-4 py-3 outline-none text-sm transition-all"
              autoComplete="off"
            />
            {errors.username && (
              <p className="text-red-500 text-xs mt-1">
                {errors.username.message}
              </p>
            )}
          </div>

          {/* Room Name Field */}
          <div>
            <label
              className="block text-sm font-medium mb-2 tracking-wider"
              htmlFor="roomname-input"
            >
              ENTER YOUR ROOM NAME
            </label>
            <input
              id="roomname-input"
              type="text"
              {...register("roomName", { required: "Room name is required" })}
              placeholder="SPECIFY_LOCATION..."
              className="w-full bg-zinc-900 border border-green-500/50 focus:border-green-400 text-green-300 placeholder:text-green-700/70 rounded-lg px-4 py-3 outline-none text-sm transition-all"
              autoComplete="off"
            />
            {errors.roomName && (
              <p className="text-red-500 text-xs mt-1">
                {errors.roomName.message}
              </p>
            )}
          </div>

          {/* Warning Note */}
          <div className="bg-zinc-900/90 border border-green-500/30 rounded-lg p-4 flex gap-3 items-start">
            <div className="text-orange-400 mt-0.5">
              <FaInfoCircle size={24} />
            </div>
            <p className="text-sm leading-relaxed">
              after creating a room we provide you a access key so that you can
              share with your friends to join the room.
            </p>
          </div>

          {/* Create Room Button */}
          <button
            type="submit"
            className="w-full bg-green-400 hover:bg-green-500 active:bg-green-600 text-black font-bold py-4 rounded-xl text-lg tracking-wider flex items-center justify-center gap-3 transition-all shadow-lg shadow-green-500/30"
          >
            CREATE A SECURE ROOM
            <FaBolt className="text-xl" />
          </button>
        </form>
      </div>
    </section>
  );
};

export default CreateRoomForm;
