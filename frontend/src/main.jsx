import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./index.css";

import {
  Route,
  RouterProvider,
  createBrowserRouter,
  createRoutesFromElements,
} from "react-router-dom";

import Layout from "./Layout.jsx";
import Home from "./components/Home/Home.jsx";
import About from "./components/About/About.jsx";
import Step1 from "./components/About/Step1.jsx";
import Step2 from "./components/About/Step2.jsx";
import { FormProvider } from './context/FormContext.jsx';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route index element={<Home />} />
      <Route path="About" element={<About />}>
        <Route path="step1" element={<Step1 />} />
        <Route path="step2" element={<Step2 />} />
      </Route>
    </Route>
  )
);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <FormProvider>
      <RouterProvider router={router} />
    </FormProvider>
  </StrictMode>,
)
