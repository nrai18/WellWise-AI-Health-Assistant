// Input validation utilities for security

/**
 * Validate email format
 */
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 * At least 6 characters
 */
export const validatePassword = (password) => {
  return password && password.length >= 6;
};

/**
 * Sanitize string input to prevent XSS
 */
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input;
  
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
};

/**
 * Validate number input
 */
export const validateNumber = (value, min = 0, max = Infinity) => {
  const num = parseFloat(value);
  return !isNaN(num) && num >= min && num <= max;
};

/**
 * Validate age input
 */
export const validateAge = (age) => {
  return validateNumber(age, 1, 120);
};

/**
 * Validate height (cm)
 */
export const validateHeight = (height) => {
  return validateNumber(height, 50, 250);
};

/**
 * Validate weight (kg)
 */
export const validateWeight = (weight) => {
  return validateNumber(weight, 10, 300);
};
