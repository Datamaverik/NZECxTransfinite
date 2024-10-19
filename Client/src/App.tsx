import { useEffect } from "react";
import "./index.css";
import styles from "./components/scrollSnap.module.css"
import { Landing } from "./components/Landing";
import { InputBox } from "./components/InputBox";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/all";

gsap.registerPlugin(ScrollTrigger);

function App() {
  ScrollTrigger.defaults({
    toggleActions: "restart pause resume pause",
    scroller: ".container"
  });
  
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  return (
    <div className="max-w-[100vw] max-h-[100vh]">
      <div className={styles.panel}>
        <Landing />
      </div>

      <div className={styles.panel}>
        <InputBox />
      </div>
    </div>
  );
}

export default App;
