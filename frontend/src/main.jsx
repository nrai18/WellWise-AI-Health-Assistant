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
import { FormProvider } from './context/FormContext.jsx';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route index element={<Home />} />
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
