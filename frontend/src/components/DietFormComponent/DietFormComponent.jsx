import React, { createContext, StrictMode, useContext, useState } from "react";
import ReactDOM from "react-dom/client";
import { useForm, Controller } from "react-hook-form";

const FormContext = createContext();
export const FormProvider = ({ children }) => (
  <FormContext.Provider value={{}}>{children}</FormContext.Provider>
);

const DietContext = createContext();

export const DietProvider = ({ children }) => {
  const [dietFormData, setDietFormData] = useState({
    age: "",
    height: "",
    weight: "",
    gender: "Male",
    activityLevel: 0,
    weightLossPlan: "Maintain weight",
    mealsPerDay: 2,
  });

  const updateDietFormData = (newData) => {
    setDietFormData((prevData) => ({ ...prevData, ...newData }));
  };

  return (
    <DietContext.Provider value={{ dietFormData, updateDietFormData }}>
      {children}
    </DietContext.Provider>
  );
};

export const useDietContext = () => useContext(DietContext);

const NumberInput = ({
  name,
  control,
  label,
  min = 0,
  max = 200,
  placeholder = "",
}) => (
  <Controller
    name={name}
    control={control}
    rules={{
      required: `${label} is required`,
      min: { value: min, message: `Minimum value is ${min}` },
      max: { value: max, message: `Maximum value is ${max}` },
    }}
    render={({ field: { onChange, value }, fieldState: { error } }) => (
      <div>
        <label className="block text-emerald-700 font-semibold mb-1">
          {label}
        </label>
        <div className="relative flex items-center">
          <button
            type="button"
            onClick={() => {
              const numValue = parseInt(value, 10);
              if (!isNaN(numValue) && numValue > min) {
                onChange(numValue - 1);
              }
            }}
            className="absolute left-0 h-full px-3 text-gray-600 hover:text-emerald-700 transition-colors rounded-l-md bg-gray-200 hover:bg-gray-300 z-10"
          >
            -
          </button>
          <input
            type="number"
            value={value}
            placeholder={placeholder}
            onChange={(e) => {
              const val = e.target.value;
              if (val === "") {
                onChange("");
                return;
              }
              const num = parseInt(val, 10);
              if (!isNaN(num) && num <= max) {
                onChange(num);
              }
            }}
            className="w-full p-2 rounded-md bg-gray-100 text-gray-800 text-center outline-none focus:ring-2 focus:ring-emerald-400 transition relative"
          />
          <button
            type="button"
            onClick={() => {
              const numValue = parseInt(value, 10);
              if (isNaN(numValue)) {
                onChange(min);
              } else if (numValue < max) {
                onChange(numValue + 1);
              }
            }}
            className="absolute right-0 h-full px-3 text-gray-600 hover:text-emerald-700 transition-colors rounded-r-md bg-gray-200 hover:bg-gray-300 z-10"
          >
            +
          </button>
        </div>
        {error && <p className="text-red-500 text-sm mt-1">{error.message}</p>}
      </div>
    )}
  />
);

export const DietFormComponent = () => {
  const { dietFormData, updateDietFormData } = useDietContext();
  const { handleSubmit, control, watch } = useForm({
    defaultValues: dietFormData,
  });

  const activityLevel = watch("activityLevel", 0);
  const mealsPerDay = watch("mealsPerDay", 2);

  const activityLabels = [
    "Little/no exercise",
    "Light exercise (1-2 days/wk)",
    "Moderate exercise (3-5 days/wk)",
    "Heavy exercise (6-7 days/wk)",
    "Very active & physical job",
  ];

  const onSubmit = (data) => {
    console.log("Form Submitted Data:", data);
    updateDietFormData(data);
    alert("Check the console for the final form data object!");
  };

  return (
    <div className="bg-gray-50 min-h-screen p-4 sm:p-8 flex items-center justify-center font-sans mt-10">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="relative w-full max-w-4xl mx-auto bg-gradient-to-br from-emerald-50 via-white to-green-50 p-10 rounded-3xl shadow-xl overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-300/20 via-green-200/20 to-blue-300/20 blur-3xl animate-pulseSlow -z-10"></div>

        <div className="relative">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-center text-gray-800 mb-8">
            Diet Recommendation
          </h1>
          <p className="text-center text-gray-500 mb-10 -mt-6">
            Modify the values and click Generate.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-gray-700">
            <div className="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
              <NumberInput
                name="age"
                control={control}
                label="Age"
                min={1}
                max={120}
                placeholder="e.g., 25"
              />
            </div>
            <div className="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
              <NumberInput
                name="height"
                control={control}
                label="Height (cm)"
                min={50}
                max={250}
                placeholder="e.g., 170"
              />
            </div>
            <div className="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
              <NumberInput
                name="weight"
                control={control}
                label="Weight (kg)"
                min={10}
                max={200}
                placeholder="e.g., 65"
              />
            </div>

            <div className="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
              <label className="block text-emerald-700 font-semibold mb-2">
                Gender
              </label>
              <Controller
                name="gender"
                control={control}
                render={({ field }) => (
                  <div className="flex items-center space-x-6 pt-1">
                    {["Male", "Female"].map((gender) => (
                      <label
                        key={gender}
                        className="flex items-center cursor-pointer"
                      >
                        <input
                          type="radio"
                          {...field}
                          value={gender}
                          checked={field.value === gender}
                          className="hidden"
                        />
                        <span
                          className={`w-5 h-5 rounded-full border-2 ${
                            field.value === gender
                              ? "border-emerald-500 bg-emerald-500"
                              : "border-gray-300 bg-gray-100"
                          } transition-all`}
                        ></span>
                        <span className="ml-2 text-gray-700">{gender}</span>
                      </label>
                    ))}
                  </div>
                )}
              />
            </div>

            <div className="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 sm:col-span-2">
              <label
                htmlFor="activityLevel"
                className="block text-emerald-700 font-semibold"
              >
                Activity
              </label>
              <span className="text-emerald-600 text-sm font-medium">
                {activityLabels[activityLevel]}
              </span>
              <Controller
                name="activityLevel"
                control={control}
                render={({ field }) => (
                  <input
                    id="activityLevel"
                    type="range"
                    min="0"
                    max="4"
                    step="1"
                    {...field}
                    className="w-full h-2 bg-emerald-100 rounded-lg appearance-none cursor-pointer mt-2 range-thumb"
                  />
                )}
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Little/no exercise</span>
                <span>Very active</span>
              </div>
            </div>

            <div className="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
              <label
                htmlFor="weightLossPlan"
                className="block text-emerald-700 font-semibold mb-1"
              >
                Weight Goal
              </label>
              <Controller
                name="weightLossPlan"
                control={control}
                render={({ field }) => (
                  <select
                    {...field}
                    className="w-full p-2 rounded-md bg-gray-100 focus:ring-2 focus:ring-emerald-400 outline-none transition border-gray-300"
                  >
                    <option value="Lose weight">Lose weight</option>
                    <option value="Maintain weight">Maintain weight</option>
                    <option value="Gain weight">Gain weight</option>
                  </select>
                )}
              />
            </div>

            <div className="group bg-white/80 backdrop-blur-md p-5 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
              <label
                htmlFor="mealsPerDay"
                className="block text-emerald-700 font-semibold"
              >
                Meals per day
              </label>
              <span className="text-emerald-600 font-medium text-sm">
                {mealsPerDay}
              </span>
              <Controller
                name="mealsPerDay"
                control={control}
                render={({ field }) => (
                  <input
                    id="mealsPerDay"
                    type="range"
                    min="2"
                    max="6"
                    step="1"
                    {...field}
                    className="w-full h-2 bg-emerald-100 rounded-lg appearance-none cursor-pointer mt-2 range-thumb"
                  />
                )}
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>2</span>
                <span>6</span>
              </div>
            </div>
          </div>

          <div className="mt-10 text-center">
            <button
              type="submit"
              className="py-2.5 px-8 bg-gradient-to-r from-emerald-500 via-green-500 to-teal-500 hover:from-emerald-600 hover:to-green-600 text-white font-semibold rounded-full shadow-lg hover:shadow-emerald-400/40 transition-all duration-500 hover:scale-110"
            >
              Generate
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};




