/* eslint-disable react/jsx-pascal-case */
// App.jsx
import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./pages/Home";
import Contact from "./pages/Contact";
import Events from "./pages/Events";

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <div className="bg-black h-full w-full flex items-center justify-center">
        <Home />
      </div>
    ),
  },
  {
    path: "/events",
    element: (
      <div className="bg-black h-full w-full flex items-center justify-center">
        <Events />
      </div>
    ),
  },
  {
    path: "/contactus",
    element: (
      <div className="bg-black h-full w-full flex items-center justify-center">
        <Contact />
      </div>
    ),
  },
]);

function App() {
  document.documentElement.classList.add("dark");

  return <RouterProvider router={router} />;
}

export default App;
