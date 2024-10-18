import TextInputField from "../components/form/TextInputField";
import { FieldError, useForm } from "react-hook-form";
import * as UserApi from "../network/api";

const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UserApi.loginCredentials>();

  function onSubmit(credentials: UserApi.loginCredentials) {
    console.log(credentials);
  }
  return (
    <div>
      <div></div>
      <div>
        <form action="post" onSubmit={handleSubmit(onSubmit)}>
          <TextInputField
            name="username"
            label="Username"
            type="text"
            placeholder="Username"
            register={register}
            registerOptions={{
              required: "required",
              minLength: 3,
              maxLength: 255,
            }}
            error={errors.username as FieldError}
          />
          <TextInputField
            name="password"
            label="Password"
            type="password"
            placeholder="Password"
            register={register}
            registerOptions={{
              required: "required",
              minLength: 3,
              maxLength: 255,
            }}
            error={errors.password as FieldError}
          />
          <button type="submit">Log In</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
