import { useEffect, useRef } from "react";
import "./index.css";
import { Landing } from "./components/Landing";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/all";
import { InputBox } from "./components/InputBox";

gsap.registerEffect(ScrollTrigger);

function App() {
  const landingEl = useRef(null);
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  return (
    <div ref={landingEl}>
      <Landing />
      <InputBox />
    </div>
  );
}

export default App;
