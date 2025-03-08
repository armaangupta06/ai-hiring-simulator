import { useState } from "react";
import { TeamArchetype } from "@/types";
import { motion } from "framer-motion";

interface HeaderProps {
  archetypes: TeamArchetype[];
  selectedArchetype: TeamArchetype;
  onArchetypeChange: (archetype: TeamArchetype) => void;
}

export function Header({ archetypes, selectedArchetype, onArchetypeChange }: HeaderProps) {
  return (
    <motion.header 
      className="py-6 absolute top-0 left-0 right-0 z-20"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="container mx-auto px-6 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ 
              type: "spring", 
              stiffness: 260, 
              damping: 20,
              delay: 0.2 
            }}
          >
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-lg">AI</span>
            </div>
          </motion.div>
          <div>
            <h1 className="text-xl font-bold text-white">AI Hiring Simulator</h1>
          </div>
        </div>
        
        <div className="flex items-center">
          <div className="backdrop-blur-md bg-black/10 rounded-full p-1 flex">
            {archetypes.map((archetype) => (
              <button
                key={archetype.name}
                onClick={() => onArchetypeChange(archetype)}
                className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${
                  selectedArchetype.name === archetype.name
                    ? "bg-gradient-to-r from-indigo-500 to-indigo-600 text-white shadow-md"
                    : "text-zinc-300 hover:text-white"
                }`}
              >
                {archetype.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.header>
  );
}
