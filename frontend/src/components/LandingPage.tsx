"use client";

import { useState } from "react";
import { BackgroundGradientAnimation } from "@/components/ui/background-gradient-animation";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import { motion } from "framer-motion";

interface LandingPageProps {
  onStartupDescriptionSubmit: (description: string) => void;
}

export function LandingPage({ onStartupDescriptionSubmit }: LandingPageProps) {
  const [startupDescription, setStartupDescription] = useState("");

  const placeholders = [
    "We're building a fintech app for small businesses...",
    "Our startup creates AI-powered healthcare solutions...",
    "We're developing a sustainable fashion marketplace...",
    "Our company focuses on renewable energy storage...",
    "We're creating a platform for remote education...",
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setStartupDescription(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (startupDescription.trim()) {
      onStartupDescriptionSubmit(startupDescription);
    }
  };

  return (
    <BackgroundGradientAnimation
      gradientBackgroundStart="rgb(20, 20, 40)" 
      gradientBackgroundEnd="rgb(0, 0, 20)"
      firstColor="64, 64, 191"
      secondColor="128, 0, 128"
      thirdColor="0, 128, 128"
      fourthColor="0, 64, 128"
      fifthColor="64, 0, 64"
      pointerColor="128, 128, 255"
      interactive={true}
    >
      <div className="absolute z-50 inset-0 flex flex-col items-center justify-center max-w-3xl mx-auto px-4 text-center pointer-events-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl mb-4">
            My Intern
          </h1>
          <p className="text-xl text-zinc-300">
            Build your dream team with AI-powered candidate recommendations
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="w-full max-w-xl"
        >
          <div className="mb-3 text-left">
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Describe your startup
            </label>
          </div>
          <PlaceholdersAndVanishInput
            placeholders={placeholders}
            onChange={handleInputChange}
            onSubmit={handleSubmit}
          />
          <p className="mt-2 text-sm text-zinc-400">
            Press Enter to submit your startup description and find the perfect team
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-16 text-sm text-zinc-400"
        >
          <p>
            Powered by AI to match candidates with your startup's unique needs
          </p>
        </motion.div>
      </div>
    </BackgroundGradientAnimation>
  );
}
