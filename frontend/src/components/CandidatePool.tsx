import { CandidateWithRatings } from "@/types";
import { motion } from "framer-motion";
import { CandidateCard } from "./CandidateCard";
import { PlusIcon } from "@heroicons/react/24/solid";

interface CandidatePoolProps {
  candidates: CandidateWithRatings[];
  onAddToTeam: (candidate: CandidateWithRatings) => void;
  onViewDetails: (candidate: CandidateWithRatings) => void;
}

export function CandidatePool({ candidates, onAddToTeam, onViewDetails }: CandidatePoolProps) {
  return (
    <div className="container mx-auto px-6 py-8 max-w-[1800px]" id="candidate-pool">
      {/* Header */}
      <motion.div 
        className="mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-white bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-blue-400">Candidate Pool</h1>
            <p className="text-indigo-200/80">Available candidates for your team</p>
          </div>
        </div>
      </motion.div>
      
      {/* Candidates Grid */}
      <div className="flex flex-wrap justify-center gap-8">
        {candidates.map((candidate, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="w-[350px] relative"
          >
            <div className="h-full">
              <CandidateCard 
                candidate={candidate} 
                onClick={onViewDetails}
                isSelected={false}
                onAddToTeam={onAddToTeam}
              />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
