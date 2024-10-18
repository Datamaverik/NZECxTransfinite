/* eslint-disable @typescript-eslint/no-explicit-any */
import { FieldError, RegisterOptions, UseFormRegister } from "react-hook-form";

interface TextInputFieldProps {
  name: string;
  label: string;
  register: UseFormRegister<any>;
  registerOptions?: RegisterOptions;
  error?: FieldError;
  [x: string]: any; // allows us to pass any other props inside the form element even if it's not defined in the props
}

const TextInputField = ({
  name,
  label,
  register,
  registerOptions,
  error,
  ...props
}: TextInputFieldProps) => {
  return (
    <div className="flex flex-col text-[1.5rem] mb-5 text-gray-400">
      <label htmlFor={name}>{label}</label>
      <input
        className={`rounded-md p-1 border-[2px] ${error ? 'border-red-600' : 'border-gray-300'}`}
        id={name}
        {...props}
        {...register(name, registerOptions)}
        aria-invalid={!!error}
      />
      {error && <div className="text-red-600">{error.message}</div>}
    </div>
  );
};

export default TextInputField;
