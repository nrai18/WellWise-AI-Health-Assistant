import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { validateEmail, validatePassword } from "../../utils/validation";
import "./SignupPage.css";

export default function SignupPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [passwordStrength, setPasswordStrength] = useState(0);
  const navigate = useNavigate();
  const cardRef = useRef(null);
  const dotsRef = useRef(null);

  const calculatePasswordStrength = (pwd) => {
    let strength = 0;
    if (pwd.length >= 6) strength++;
    if (pwd.length >= 10) strength++;
    if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) strength++;
    if (/\d/.test(pwd)) strength++;
    if (/[^a-zA-Z\d]/.test(pwd)) strength++;
    return strength;
  };

  const getStrengthColor = () => {
    if (passwordStrength === 0) return 'bg-gray-200';
    if (passwordStrength <= 2) return 'bg-red-500';
    if (passwordStrength <= 3) return 'bg-yellow-500';
    if (passwordStrength <= 4) return 'bg-blue-500';
    return 'bg-green-500';
  };

  const getStrengthText = () => {
    if (passwordStrength === 0) return 'Enter password';
    if (passwordStrength <= 2) return 'Weak';
    if (passwordStrength <= 3) return 'Fair';
    if (passwordStrength <= 4) return 'Good';
    return 'Strong';
  };

  const handleMouseMove = (e) => {
    const card = cardRef.current;
    if (!card) return;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotateX = ((y - rect.height / 2) / rect.height) * 10;
    const rotateY = ((x - rect.width / 2) / rect.width) * 10;
    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.03)`;
  };

  const handleMouseLeave = () => {
    const card = cardRef.current;
    if (card) card.style.transform = "rotateX(0deg) rotateY(0deg) scale(1)";
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Validate inputs
    if (!name || name.trim().length < 2) {
      setError("Name must be at least 2 characters");
      return;
    }

    if (!validateEmail(email)) {
      setError("Please enter a valid email address");
      return;
    }

    if (!validatePassword(password)) {
      setError(

"Password must be at least 6 characters");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        setSuccess("Signup successful! Redirecting to login...");
        setError("");
        setTimeout(() => navigate("/login"), 2000);
      } else {
        setError(data.message || "Signup failed");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Network error. Please try again.");
    }
  };

  useEffect(() => {
    const canvas = dotsRef.current;
    const ctx = canvas.getContext("2d");
    let width, height, dots;

    const init = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      dots = Array.from({ length: 120 }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 2 + 1,
        dx: (Math.random() - 0.5) * 0.3,
        dy: (Math.random() - 0.5) * 0.3,
      }));
    };

    const animate = () => {
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
      dots.forEach((dot) => {
        dot.x += dot.dx;
        dot.y += dot.dy;
        if (dot.x < 0 || dot.x > width) dot.dx *= -1;
        if (dot.y < 0 || dot.y > height) dot.dy *= -1;
        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dot.r, 0, Math.PI * 2);
        ctx.fill();
      });
      requestAnimationFrame(animate);
    };

    init();
    animate();
    window.addEventListener("resize", init);
    return () => window.removeEventListener("resize", init);
  }, []);

  return (
    <div className="signup-page">
      <canvas ref={dotsRef} className="dots-bg" />

      <div
        ref={cardRef}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        className="signup-card"
      >
        <h2 className="signup-title">Create Your Account</h2>

        <form onSubmit={handleSignup} className="signup-form">
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="input-field"
          />

          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="input-field"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setPasswordStrength(calculatePasswordStrength(e.target.value));
            }}
            required
            className="input-field"
          />
          
          {/* Password Strength Indicator */}
          {password && (
            <div style={{marginTop: '10px'}}>
              <div style={{display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px'}}>
                <div style={{flex: 1, height: '6px', backgroundColor: '#e5e7eb', borderRadius: '10px', overflow: 'hidden'}}>
                  <div 
                    className={getStrengthColor()}
                    style={{
                      height: '100%',
                      width: `${(passwordStrength / 5) * 100}%`,
                      transition: 'all 0.3s ease'
                    }}
                  ></div>
                </div>
                <span style={{fontSize: '13px', fontWeight: 600, color: passwordStrength <= 2 ? '#dc2626' : passwordStrength <= 3 ? '#ca8a04' : passwordStrength <= 4 ? '#2563eb' : '#16a34a'}}>
                  {getStrengthText()}
                </span>
              </div>
              <div style={{fontSize: '11px', color: '#4b5563'}}>
                <p style={{color: password.length >= 6 ? '#16a34a' : '#6b7280', marginBottom: '3px'}}>✓ At least 6 characters</p>
                <p style={{color: /[a-z]/.test(password) && /[A-Z]/.test(password) ? '#16a34a' : '#6b7280', marginBottom: '3px'}}>✓ Upper & lowercase</p>
                <p style={{color: /\d/.test(password) ? '#16a34a' : '#6b7280'}}>✓ Contains number</p>
              </div>
            </div>
          )}

          <button type="submit" className="signup-btn">
            Sign Up
          </button>
        </form>

        {error && <p className="error-text">{error}</p>}
        {success && <p className="success-text">{success}</p>}

        <p className="toggle-link">
          Already have an account?{" "}
          <button onClick={() => navigate("/login")}>Login</button>
        </p>
      </div>
    </div>
  );
}
