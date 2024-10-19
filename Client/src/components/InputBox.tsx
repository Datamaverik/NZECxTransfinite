import { useEffect, useRef, useState } from "react";
import { PlaceholdersAndVanishInput } from "./ui/placeholders-and-vanish-input";
import * as UserApi from "../network/api";
import gsap from "gsap";
import { MultiStepLoader as Loader } from "./ui/multi-step-loader";
import { IconSquareRoundedX } from "@tabler/icons-react";

export interface CodeBody {
  code: string;
}

interface parsedResponse {
  code: string;
  fix: string;
  vulnerability: string;
}

const loadingStates = [
  {
    text: "Comparing with existing vulnerable samples",
  },
  {
    text: "",
  },
  {
    text: "Meeting Tyler Durden",
  },
  {
    text: "He makes soap",
  },
  {
    text: "We goto a bar",
  },
  {
    text: "Start a fight",
  },
  {
    text: "We like it",
  },
  {
    text: "Welcome to F**** C***",
  },
];

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
  const loaderRef = useRef<HTMLDivElement>(null);
  const inputBoxRef = useRef<HTMLDivElement>(null);
  const responseRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCode(e.target.value);
  };
  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(code);
    const requestData: CodeBody = {
      code: code,
    };

    setLoading(true);
    if (loaderRef.current) loaderRef.current.style.display = "block";
    const response = await UserApi.vulnRes(requestData);
    console.log(response);

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

    setTimeout(() => {
      setSubmitted(true);
      setLoading(false);
      if (loaderRef.current) loaderRef.current.style.display = "none";
    }, 1000);
  };
  useEffect(() => {
    if (loaderRef.current) loaderRef.current.style.display = "none";
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
      // gsap.to(inputBoxRef.current, {
      // y: "45vh",
      // onComplete: () => {

      // },
      // duration: 1,
      // });
      gsap.to(responseRef.current, { opacity: 1, duration: 1, delay: 1 });
    }
  }, [submitted]);
  return (
    <div className="h-[100vh] max-w-[100vw] max-h-[100vh] flex flex-col justify-center  items-center">
      <div
        ref={loaderRef}
        className="w-full h-[60vh] flex items-center justify-center"
      >
        {/* Core Loader Modal */}
        <Loader
          loadingStates={loadingStates}
          loading={loading}
          duration={2000}
        />
        {loading && (
          <button
            className="fixed top-4 right-4 text-black dark:text-white z-[120]"
            onClick={() => setLoading(false)}
          >
            <IconSquareRoundedX className="h-10 w-10" />
          </button>
        )}
      </div>
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
          className="max-w-[90vw] max-h-[60vh] overflow-y-scroll overflow-x-hidden text-center sm:text-xl dark:text-white text-black"
        >
          {parsedRes.map((item, index) => (
            <div key={index} className="mb-10">
              <pre className="bg-gray-800 text-white p-4 rounded max-w-[70vw]">
                <code>{item.code}</code>
              </pre>
              <div className="alert alert-warning mt-2 max-w-[70vw]">
                <strong className="text-red-700">Vulnerability:</strong> {item.vulnerability}
              </div>
              <div className="bg- text-blue-500 p-4 rounded mt-2 max-w-[70vw]">
                <strong>Fix:</strong> {item.fix}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
