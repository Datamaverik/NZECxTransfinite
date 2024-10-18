/* eslint-disable @typescript-eslint/no-explicit-any */
import styles from "../styles/form.module.css";
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
    <div className={styles.textGroup}>
      <label htmlFor={name} className={styles.formLabel}>{label}</label>
      <input
        id={name}
        className={`${styles.inputArea} ${error ? styles.invalid : ""}`}
        {...props}
        {...register(name, registerOptions)}
        aria-invalid={!!error}
      />
      {error && <div className={styles.invalidFeedback}>{error.message}</div>}
    </div>
  );
};

export default TextInputField;
