// src/context/FormContext.jsx
import React, { createContext, useContext, useState } from "react";

const FormContext = createContext();

export const FormProvider = ({ children }) => {
  const [formData, setFormData] = useState({
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
