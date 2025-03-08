"use client";

import { motion } from "framer-motion";
import { CheckCircleIcon } from "@heroicons/react/24/solid";
import { useEffect, useState } from "react";

interface LoadingAnimationProps {
  isLoading: boolean;
  currentStep?: number;
}

export function LoadingAnimation({ isLoading, currentStep = 1 }: LoadingAnimationProps) {
  const [activeStep, setActiveStep] = useState(1);
  
  // Update active step when currentStep prop changes
  useEffect(() => {
    if (currentStep) {
      setActiveStep(currentStep);
    }
  }, [currentStep]);
  
  // We've removed the demo mode that automatically progressed through steps
  // Now the loading animation will only update when the actual API calls complete
  
  const steps = [
    { 
      id: 1, 
      text: "Scoring candidates based on startup description", 
      completed: activeStep > 1, 
      highlight: activeStep === 1
    },
    { 
      id: 2, 
      text: "Generating team archetypes", 
      completed: activeStep > 2, 
      highlight: activeStep === 2
    },
    { 
      id: 3, 
      text: "Optimizing team composition", 
      completed: activeStep > 3, 
      highlight: activeStep === 3
    },
    { 
      id: 4, 
      text: "Preparing your dashboard", 
      completed: activeStep > 4, 
      highlight: activeStep === 4
    },
  ];

  return (
    <div className={`fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-xl transition-opacity duration-500 ${isLoading ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
      <div className="max-w-md w-full mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
          className="p-8"
        >
          <div className="space-y-4">
            {steps.map((step, index) => (
              <motion.div
                key={step.id}
                initial={{ opacity: 0 }}
                animate={{ 
                  opacity: step.highlight ? 1 : step.completed ? 0.8 : 0.5, 
                  filter: step.completed && !step.highlight ? "blur(0.7px)" : "blur(0px)",
                  transition: { duration: 0.2 }
                }}
                className="flex items-center space-x-3"
              >
                <CheckCircleIcon 
                  className={`h-5 w-5 ${step.highlight ? 'text-lime-500' : step.completed ? 'text-white/80' : 'text-gray-600'}`} 
                />
                <span className={`${step.highlight ? 'text-lime-500' : 'text-white'} text-base font-medium`}>
                  {step.text}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
