import { useEffect, useRef, useState } from "react";
import { PlaceholdersAndVanishInput } from "./ui/placeholders-and-vanish-input";
import * as UserApi from "../network/api";
import gsap from "gsap";

export interface CodeBody {
  code: string;
}

interface parsedResponse {
  code: string;
  fix: string;
  vulnerability: string;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function is_Array_or_object(response:any) {
  if (Array.isArray(response)) {
    return 1;
  } else if (typeof response === "object" && response !== null) {
    return 2;
  } else {
    return -1;
  }
}

function isType(obj: any): obj is parsedResponse {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.code === 'string' &&
    typeof obj.vulnerability === 'string' &&
    typeof obj.fix === 'string'
  );
}

export function InputBox() {
  const [submitted, setSubmitted] = useState(false);
  const [response, setResponse] = useState("");
  const [code, setCode] = useState<string>("");
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [parsedRes, setParsedRes] = useState<parsedResponse[]>([]);

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
  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(code);

    const requestData: CodeBody = {
      code: code,
    };

    const response = await UserApi.vulnRes(requestData);
    // function dfs(response: any): void {
      // if (is_Array_or_object(response)==2){
        // if(isType(response))set
      // }
        // for (const child of node.children) {
          // dfs(child);
        // }
    // }
    console.log(response);

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
