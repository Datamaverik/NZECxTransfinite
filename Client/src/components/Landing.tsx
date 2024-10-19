import { Vortex } from "./ui/vortex";

export function Landing() {
  return (
    <div className="w-[100vw] m-0 rounded-md  h-[100vh] overflow-hidden">
      <Vortex
        backgroundColor="black"
        className="flex items-center flex-col justify-center w-full h-full"
      >
        <h1 className="text-white text-2xl md:text-6xl font-bold text-center">
          How's it going
        </h1>
      </Vortex>
    </div>
  );
}
