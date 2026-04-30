import { LockIcon, Trash, Eraser, Zap } from 'lucide-react'

const FeaturesSection = () => {
  const features = [
    {
      icon: <LockIcon />,
      title: 'SECURE CONNECTIONS',
      stat: null,
      description:
        'we use hashing room id to create unique id for each room and its protected with the hashing algorithms.',
    },
    {
      icon: <Zap />,
      title: 'LATENCY_0.02ms',
      stat: '0.02ms',
      accent: 'INSTANT MESSAGES',
      description:
        'we use websockets and pubsub to deliver your messages with faster and low latency.',
    },
    {
      icon: <Eraser />,
      title: 'TEMPORARY IDENTITY',
      stat: null,
      description:
        'No accounts. No passwords to leak. Your identity is a temporary session hash that dissolves when you close the tab.',
    },
    {
      icon: <Trash />,
      title: 'AUTO-WIPE',
      stat: null,
      description:
        'All room history is stored in RAM only. Closing the session triggers an immediate cryptographic shredding of all data.',
    },
  ]

  return (
    <section className="relative w-full overflow-hidden bg-black px-5 py-20 font-sans md:py-28 lg:py-32">
      <div className="relative mx-auto max-w-7xl">
        {/* Headline section */}
        <div className="mb-16 text-center md:mb-20">
          <h2 className="mt-6 text-3xl font-black tracking-tight text-white md:text-5xl lg:text-9xl">
            <span className="bg-linear-to-r from-green-300 to-emerald-400 bg-clip-text text-transparent">
              DON'T BURY ABOUT MESSAGES
            </span>
            <br />
            <span className="relative inline-block mt-2">
              ITS ENCRYPTED
              <span className="absolute -bottom-2 left-0 h-0.5 w-full bg-linear-to-r from-transparent via-green-400 to-transparent"></span>
            </span>
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-base leading-relaxed text-gray-300 md:text-lg">
            Communication bypasses our servers. We never see your messages
            because we physically cannot.{' '}
            <span className="font-semibold text-green-400">
              Your browser is the terminal.
            </span>
          </p>
        </div>

        {/* Features grid */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 md:gap-8">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="group relative border rounded-tl border-green-500/20 bg-black/40 p-6 backdrop-blur-sm transition-all duration-300 hover:border-green-500/60 hover:shadow-[0_0_20px_-5px_rgba(74,222,128,0.3)] md:p-8"
            >
              {/* Card corner accent */}
              <div className="absolute left-0 top-0 h-20 w-20 border-l-2 border-t-2 border-lime-300 rounded-tl"></div>

              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-green-500/10 text-2xl text-green-400 transition-all duration-300 group-hover:bg-green-500/20 group-hover:shadow-glow">
                  {feature.icon}
                </div>

                <div className="flex-1">
                  <div className="mb-2 flex flex-wrap items-baseline justify-between gap-2">
                    <h3 className="text-xl font-bold tracking-tight text-white md:text-2xl">
                      {feature.title}
                    </h3>
                    {feature.stat && (
                      <span className="rounded-full border border-green-500/40 px-2 py-0.5 text-xs font-mono font-bold text-green-400">
                        {feature.stat}
                      </span>
                    )}
                  </div>

                  {feature.accent && (
                    <div className="mb-2 text-sm font-semibold uppercase tracking-wider text-green-400">
                      {feature.accent}
                    </div>
                  )}

                  <p className="text-sm leading-relaxed text-gray-300 md:text-base">
                    {feature.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Trust badge row */}
        <div className="mt-16 flex flex-wrap items-center justify-center gap-x-6 gap-y-3 border-t border-white/20 pt-10 text-center text-xs text-white">
          <span className="inline-flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-green-500/70"></span>
            No metadata collection
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-green-500/70"></span>
            Ephemeral by design
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-green-500/70"></span>
            Open WebSocket backbone
          </span>
        </div>
      </div>
    </section>
  )
}

export default FeaturesSection
