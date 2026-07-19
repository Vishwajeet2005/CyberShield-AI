export default function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center w-full h-full min-h-[200px]">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 border-4 border-accent-cyan/20 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-accent-cyan rounded-full border-t-transparent animate-spin"></div>
        <div className="absolute inset-2 border-4 border-accent-blue/20 rounded-full"></div>
        <div className="absolute inset-2 border-4 border-accent-blue rounded-full border-b-transparent animate-spin-reverse" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-2 h-2 bg-danger rounded-full animate-pulse glow-red"></div>
        </div>
      </div>
    </div>
  );
}
