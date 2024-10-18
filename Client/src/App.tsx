import { useEffect, useState } from "react";
import * as UserApi from "./network/api";
import './index.css';
import Login from "./pages/Login";

function App() {
  const [data, setData] = useState<UserApi.TestRouteResponse>({ message: "" });

  useEffect(() => {
    const testHomeRoute = async () => {
      try {
        const response = await UserApi.testRoute();
        console.log(response);
        if (response) setData(response);
      } catch (er) {
        console.error(er);
      }
    };
    testHomeRoute();
  }, []);

  return (
  <div className="flex justify-center">
    <Login/>
  </div>);
}

export default App;
