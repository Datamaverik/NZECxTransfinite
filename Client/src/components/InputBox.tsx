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
function is_Array_or_object(response: any) {
  if (Array.isArray(response)) {
    return 1;
  } else if (typeof response === "object" && response !== null) {
    return 2;
  } else {
    return -1;
  }
}

function isGithubUrl(input: string): boolean {
  const githubUrlPattern =
    /^https?:\/\/(www\.)?github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+/;
  return githubUrlPattern.test(input);
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function isType(obj: any): obj is parsedResponse {
  return (
    typeof obj === "object" &&
    obj !== null &&
    typeof obj.code === "string" &&
    typeof obj.vulnerability === "string" &&
    typeof obj.fix === "string"
  );
}

export function InputBox() {
  const [submitted, setSubmitted] = useState(false);
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

    let response;
    if (isGithubUrl(requestData.code))
      response = await UserApi.gitResponse(requestData.code);
    else response = await UserApi.vulnRes(requestData);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    function dfs(response: any): void {
      if (is_Array_or_object(response) == 2) {
        if (isType(response)) {
          console.log(response);

          setParsedRes((prev) => [...prev, response]);
          return;
        } else {
          //  parse props
          for (const key in response) {
            if (Object.prototype.hasOwnProperty.call(response, key)) {
              const value = response[key as keyof typeof response];
              dfs(value);
            }
          }
        }
      } else if (is_Array_or_object(response) == 1) {
        // console.log(response);

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        response.forEach((element: any) => {
          dfs(element);
        });
      }
    }
    dfs(response);
    console.log(parsedRes);
    console.log(response);

    setTimeout(() => {
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
      // gsap.to(inputBoxRef.current, { y: "40vh", duration: 1 });
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
      <div className="flex flex-col">
        <div
          ref={inputBoxRef}
          className="absolute bottom-[-95vh] left-0 transform translate-x-[20%]"
        >
          <PlaceholdersAndVanishInput
            placeholders={placeholders}
            onChange={handleChange}
            onSubmit={onSubmit}
          />
        </div>
        <div
          ref={responseRef}
          style={{ opacity: 0 }}
          className="max-w-[90vw] max-h-[60vh] overflow-y-scroll scrollbar-thin scrollbar-thumb-rounded-full scrollbar-thumb-stone-800 scrollbar-track-stone-900 overflow-x-hidden text-center sm:text-xl dark:text-white text-black"
        >
          {parsedRes.map((item, index) => (
            <div key={index} className="mb-10 border-b-8 p-10">
              <strong className="text-3xl text-left flex justify-start ml-5 mb-3">Your Code:</strong>
              <pre className="bg-neutral-900 text-white p-4 rounded-md max-w-[70vw] flex flex-col justify-start">
                <code className="text-wrap text-left">{item.code}</code>
              </pre>
              <div className="alert alert-warning mt-2 max-w-[70vw] text-wrap">
                <strong className="text-red-700">Vulnerability:</strong>{" "}
                {item.vulnerability}
              </div>
              <div className="bg- text-blue-500 p-4 rounded mt-2 max-w-[70vw] text-wrap">
                <strong className="text-3xl text-left flex justify-start ml-5 mb-3">Fix:</strong>
                <pre className="bg-neutral-800 text-blue-400 p-4 rounded-md max-w-[70vw] flex flex-col justify-start">
                  <code className="text-wrap text-left">{item.fix}</code>
                </pre>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
