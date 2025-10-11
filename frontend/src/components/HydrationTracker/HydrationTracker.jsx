import React, { useState, useMemo, useEffect, useRef } from "react";

// A custom hook for animating numbers
const useCountUp = (end, duration = 1) => {
  const [count, setCount] = useState(0);
  const frameRate = 1000 / 60;
  const totalFrames = Math.round((duration * 1000) / frameRate);

  useEffect(() => {
    let frame = 0;
    const counter = setInterval(() => {
      frame++;
      const progress = frame / totalFrames;
      const currentCount = Math.round(end * progress);
      setCount(currentCount);

      if (frame === totalFrames) {
        clearInterval(counter);
        setCount(end); // Ensure it ends exactly at the target
      }
    }, frameRate);

    return () => clearInterval(counter);
  }, [end, duration, totalFrames, frameRate]);

  return count;
};

// Confetti Component
const Confetti = () => {
  const particles = useMemo(
    () =>
      Array.from({ length: 100 }).map((_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: -20 - Math.random() * 100,
        rotation: Math.random() * 360,
        scale: Math.random() * 0.5 + 0.5,
        duration: Math.random() * 2 + 3,
        delay: Math.random() * 2,
        color: ["#22c55e", "#4ade80", "#86efac", "#bbf7d0"][
          Math.floor(Math.random() * 4)
        ],
      })),
    []
  );

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map((p) => (
        <div
          key={p.id}
          className="absolute w-2 h-4 rounded-full"
          style={{
            left: `${p.x}%`,
            backgroundColor: p.color,
            animation: `fall ${p.duration}s linear ${p.delay}s infinite`,
            transform: `rotate(${p.rotation}deg) scale(${p.scale})`,
          }}
        />
      ))}
    </div>
  );
};

// Main App Component
export default function App() {
  const DAILY_GOAL_ML = 2000;
  const GLASS_SIZE_ML = 250;

  // State is now initialized from localStorage
  const [intake, setIntake] = useState(() => {
    try {
      const savedIntake = localStorage.getItem("hydrationIntake");
      return savedIntake ? JSON.parse(savedIntake) : 0;
    } catch (error) {
      console.error("Error reading from localStorage", error);
      return 0;
    }
  });

  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setTimeout(() => setAnimate(true), 100);
  }, []);

  // Effect to save intake to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem("hydrationIntake", JSON.stringify(intake));
    } catch (error) {
      console.error("Error writing to localStorage", error);
    }
  }, [intake]);

  const addWater = () => {
    setIntake((prevIntake) =>
      Math.min(prevIntake + GLASS_SIZE_ML, DAILY_GOAL_ML)
    );
  };

  const resetIntake = () => {
    setIntake(0);
  };

  const progress = useMemo(() => (intake / DAILY_GOAL_ML) * 100, [intake]);
  const animatedProgress = useCountUp(Math.round(progress), 1);

  const glassesConsumed = intake / GLASS_SIZE_ML;
  const goalInGlasses = DAILY_GOAL_ML / GLASS_SIZE_ML;

  const getEncouragement = () => {
    if (progress === 100) return "Great job! You reached your goal! 🎉";
    if (progress >= 75) return "You're almost there, keep it up!";
    if (progress >= 50) return "You're halfway there!";
    if (progress > 0) return "Good start! Every drop counts.";
    return "Let's get hydrated!";
  };

  const circumference = 2 * Math.PI * 70; // 70 is the radius (r) of the circle
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="bg-green-50 min-h-screen flex items-center justify-center font-sans p-4">
      <div
        className={`relative w-full max-w-sm bg-white rounded-2xl shadow-lg p-8 text-center transition-all duration-500 ease-in-out transform mt-10 ${
          animate ? "scale-100 opacity-100" : "scale-90 opacity-0"
        }`}
      >
        {progress === 100 && <Confetti />}

        <h1 className="text-3xl font-bold text-green-800">Hydration Tracker</h1>
        <p className="text-gray-500 mt-2 mb-6 h-6">{getEncouragement()}</p>

        <div className="relative w-48 h-48 mx-auto mb-6">
          <svg className="w-full h-full" viewBox="0 0 160 160">
            {/* Background Circle */}
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="#f0fdf4"
              strokeWidth="16"
              fill="transparent"
            />
            {/* Progress Circle */}
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="#16a34a"
              strokeWidth="16"
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              transform="rotate(-90 80 80)"
              style={{ transition: "stroke-dashoffset 1s ease-out" }}
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <span className="text-4xl font-extrabold text-green-900 drop-shadow-sm">
                {animatedProgress}%
              </span>
              <p className="text-sm text-green-700 font-medium">Completed</p>
            </div>
          </div>
        </div>

        <div className="text-lg font-semibold text-green-900 mb-6">
          <span>{intake}</span> / <span>{DAILY_GOAL_ML} ml</span>
          <p className="text-sm font-normal text-gray-500 mt-1">
            ({glassesConsumed.toFixed(0)} of {goalInGlasses} glasses)
          </p>
        </div>

        <div className="flex flex-col gap-4">
          <button
            onClick={addWater}
            disabled={intake >= DAILY_GOAL_ML}
            className="w-full bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 transition-all duration-300 disabled:bg-green-300 disabled:cursor-not-allowed transform hover:scale-105 active:scale-95"
          >
            Add a Glass ({GLASS_SIZE_ML}ml)
          </button>
          <button
            onClick={resetIntake}
            className="w-full bg-gray-200 text-gray-700 font-bold py-3 px-4 rounded-lg hover:bg-gray-300 transition-all duration-300 transform hover:scale-105 active:scale-95"
          >
            Reset
          </button>
        </div>
      </div>
      <style>{`
        @keyframes fall {
          to {
            transform: translateY(120vh) rotate(720deg);
          }
        }
      `}</style>
    </div>
  );
}
