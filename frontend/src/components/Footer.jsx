const Footer = () => {
  return (
    <footer className="relative w-full h-120 overflow-hidden">
      <span className="absolute top-0 left-0 h-0.5 w-full bg-linear-to-r from-transparent via-green-400 to-transparent"></span>
      {/* Large CIFRAR Text Background */}
      <div className="absolute inset-0 flex items-center justify-center">
        <h1 className="text-[25vw] font-bold tracking-tight bg-linear-to-r from-green-300 to-emerald-400 bg-clip-text text-transparent">
          CIFRAR
        </h1>
      </div>
      {/* Means to Encrypt at Bottom Center */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <p className="text-white text-lg  tracking-[0.2em]">means to encrypt</p>
      </div>
    </footer>
  );
};

export default Footer;
