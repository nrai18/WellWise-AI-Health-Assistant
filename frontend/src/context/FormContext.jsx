// src/context/FormContext.jsx
import React, { createContext, useContext, useState } from "react";

const FormContext = createContext();

export const FormProvider = ({ children }) => {
  const [formData, setFormData] = useState({
    Age: "28",
    Gender: "Male",
    Ethnicity: "Asian",
    Height: "175",
    Weight: "72",
    BMI: "23.5",
    "Blood Pressure": "120/80",
    "Resting Heart Rate": "72",
    SpO2: "98",
    "Diet Type": "Vegetarian",
    "Protein Intake": "Medium",
    "Junk Food Frequency": "Rarely",
    "Sugar Intake": "Low",
    "Diet Quality": "High",
    Smoking: "Never",
    Alcohol: "Occasionally",
    "Sleep Duration": "7",
    "Sleep Quality": "Good",
    "Daily Activity": "8000",
    "Exercise Type": "Running",
    "Work Hours": "8",
    "Existing Conditions": [],
    "Family History": ["Diabetes"],
    "Stress Score": "3",
    "Air Quality Index": "150",
    Exposure: "Low",
    "Urban/Rural": "Urban",
    State: "Delhi",
    City: "New Delhi",
  });

  const updateFormData = (partial) => {
    setFormData((prev) => ({ ...prev, ...partial }));
  };

  const resetForm = () => {
    setFormData({
      Age: "",
      Gender: "",
      Ethnicity: "",
      Height: "",
      Weight: "",
      BMI: "",
      "Blood Pressure": "",
      "Resting Heart Rate": "",
      SpO2: "",
      "Diet Type": "",
      "Protein Intake": "",
      "Junk Food Frequency": "",
      "Sugar Intake": "",
      "Diet Quality": "",
      Smoking: "",
      Alcohol: "",
      "Sleep Duration": "",
      "Sleep Quality": "",
      "Daily Activity": "",
      "Exercise Type": "",
      "Work Hours": "",
      "Existing Conditions": "",
      "Family History": "",
      "Stress Score": "",
      "Air Quality Index": "",
      Exposure: "",
      "Urban/Rural": "",
      State: "",
      City: "",
    });
  };

  return (
    <FormContext.Provider value={{ formData, updateFormData, resetForm }}>
      {children}
    </FormContext.Provider>
  );
};

export const useFormContext = () => useContext(FormContext);
