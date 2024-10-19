import { Vortex } from "./ui/vortex";

export function Landing() {
  return (
    <div className="w-[100vw] mx-auto rounded-md  h-[100vh] overflow-hidden">
      <Vortex
        backgroundColor="black"
        className="flex items-center flex-col justify-center px-2 md:px-10 py-4 w-full h-full"
      >
       <h1 className="text-white text-2xl md:text-6xl font-bold text-center">Mongo mummy kaisi hai</h1>
      </Vortex>
    </div>
  );
}
