import { useEffect, useRef, useState } from "react";
import { PlaceholdersAndVanishInput } from "./ui/placeholders-and-vanish-input";
import gsap from "gsap";

export function InputBox() {
  const [submitted, setSubmitted] = useState(false);
  const [response, setResponse] = useState("");
  const [code, setCode] = useState<string>("");
  const placeholders = [
    "What's the first rule of Fight Club?",
    "Who is Tyler Durden?",
    "Where is Andrew Laeddis Hiding?",
    "Write a Javascript method to reverse a string",
    "How to assemble your own PC?",
  ];

  const headingRef = useRef<HTMLHeadingElement>(null);
  const inputBoxRef = useRef<HTMLDivElement>(null);
  const responseRef = useRef<HTMLDivElement>(null);
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCode(e.target.value);
  };
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(code);
    setTimeout(() => {
      setResponse("<h1>This is a parsed response from the backend</h1>");
      setSubmitted(true);
    }, 1000);
  };
  useEffect(() => {
    if (submitted) {
      gsap.to(headingRef.current, {
        opacity: 0,
        duration: 1,
        scrub: 0.8,
        onComplete: () => {
          if (headingRef.current) {
            headingRef.current.style.display = "none";
          }
        },
      });
      gsap.to(inputBoxRef.current, { y: "40vh", duration: 1 });
      gsap.to(responseRef.current, { opacity: 1, duration: 1, delay: 1 });
    }
  }, [submitted]);
  return (
    <div className="h-[100vh] max-w-[100vw] max-h-[100vh] flex flex-col justify-center  items-center">
      <h2
        ref={headingRef}
        className="mb-10 sm:mb-20 text-3xl text-center sm:text-7xl dark:text-white text-black"
      >
        Give us your faulty code
      </h2>
      <div ref={inputBoxRef}>
        <PlaceholdersAndVanishInput
          placeholders={placeholders}
          onChange={handleChange}
          onSubmit={onSubmit}
        />
      </div>
      <div
        ref={responseRef}
        style={{ opacity: 0 }}
        className="mt-10 text-center sm:text-4xl dark:text-white text-black"
        dangerouslySetInnerHTML={{ __html: response }}
      />
    </div>
  );
}
