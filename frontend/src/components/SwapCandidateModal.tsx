import { useState, useEffect, useRef } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { CandidateWithRatings } from "@/types";
import { motion, AnimatePresence } from "framer-motion";

interface SwapCandidateModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentCandidate: CandidateWithRatings | null;
  poolCandidates: CandidateWithRatings[];
  onSwapCandidate: (current: CandidateWithRatings, replacement: CandidateWithRatings) => void;
}

export function SwapCandidateModal({
  isOpen,
  onClose,
  currentCandidate,
  poolCandidates,
  onSwapCandidate,
}: SwapCandidateModalProps) {
  // Instead of returning null, we'll render the Dialog conditionally
  
  // State for sorted candidates
  const [sortedCandidates, setSortedCandidates] = useState<CandidateWithRatings[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Sort candidates by overall rating once when pool changes
  useEffect(() => {
    if (poolCandidates.length > 0) {
      // Sort candidates and take only the top 40
      const sorted = [...poolCandidates]
        .sort((a, b) => b.ratings.overall - a.ratings.overall)
        .slice(0, 40);
      
      setSortedCandidates(sorted);
    }
  }, [poolCandidates]);

  // Get color based on rating difference
  const getDifferenceColor = (diff: number) => {
    if (diff > 0) return "text-green-400";
    if (diff < 0) return "text-red-400";
    return "text-gray-400";
  };

  // Get sign for difference
  const getDifferenceSign = (diff: number) => {
    if (diff > 0) return "+";
    return "";
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent 
        className="bg-zinc-900 border border-zinc-800 text-white max-w-4xl max-h-[80vh] overflow-y-auto"
        ref={containerRef}
      >
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold text-white bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-blue-400">
            Swap {currentCandidate?.name || 'Candidate'}
          </DialogTitle>
        </DialogHeader>

        <div className="mt-4">
          <h3 className="text-lg font-medium text-indigo-200 mb-4">Select a replacement candidate:</h3>
          <p className="text-sm text-indigo-200/60 mb-4">
            Showing top {sortedCandidates.length} candidates
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Display the top candidates */}
            {currentCandidate && sortedCandidates.map((candidate, index) => {
              // Calculate rating differences
              const overallDiff = candidate.ratings.overall - currentCandidate.ratings.overall;
              const technicalDiff = candidate.ratings.technical - currentCandidate.ratings.technical;
              const educationDiff = candidate.ratings.education - currentCandidate.ratings.education;
              const softSkillsDiff = candidate.ratings.softSkills - currentCandidate.ratings.softSkills;
              
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2, delay: index * 0.05 }}
                  className="bg-zinc-800/50 rounded-lg border border-zinc-700/50 p-4 hover:bg-zinc-700/30 cursor-pointer"
                  onClick={() => currentCandidate && onSwapCandidate(currentCandidate, candidate)}
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="text-lg font-semibold text-white">{candidate.name}</h4>
                      <p className="text-sm text-indigo-200/80">{candidate.location}</p>
                    </div>
                    <div className="flex items-center">
                      <span className="text-xl font-bold">{candidate.ratings.overall}</span>
                      <span className={`ml-2 text-sm font-medium ${getDifferenceColor(overallDiff)}`}>
                        {getDifferenceSign(overallDiff)}{overallDiff}
                      </span>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-3 gap-4 mt-3">
                    <div className="flex flex-col">
                      <span className="text-xs text-indigo-200/70">TECH</span>
                      <div className="flex items-center">
                        <span className="text-sm font-bold">{candidate.ratings.technical}</span>
                        <span className={`ml-2 text-xs ${getDifferenceColor(technicalDiff)}`}>
                          {getDifferenceSign(technicalDiff)}{technicalDiff}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex flex-col">
                      <span className="text-xs text-indigo-200/70">EDU</span>
                      <div className="flex items-center">
                        <span className="text-sm font-bold">{candidate.ratings.education}</span>
                        <span className={`ml-2 text-xs ${getDifferenceColor(educationDiff)}`}>
                          {getDifferenceSign(educationDiff)}{educationDiff}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex flex-col">
                      <span className="text-xs text-indigo-200/70">SOFT</span>
                      <div className="flex items-center">
                        <span className="text-sm font-bold">{candidate.ratings.softSkills}</span>
                        <span className={`ml-2 text-xs ${getDifferenceColor(softSkillsDiff)}`}>
                          {getDifferenceSign(softSkillsDiff)}{softSkillsDiff}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {candidate.skills?.slice(0, 3).map((skill, i) => (
                      <span 
                        key={i} 
                        className="text-xs px-2 py-0.5 rounded-full bg-indigo-900/50 text-indigo-200 border border-indigo-700/30"
                      >
                        {skill}
                      </span>
                    ))}
                    {candidate.skills && candidate.skills.length > 3 && (
                      <span className="text-xs px-2 py-0.5 rounded-full bg-blue-900/50 text-blue-200 border border-blue-700/30">
                        +{candidate.skills.length - 3}
                      </span>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
          
          {/* Footer note */}
          {sortedCandidates.length > 0 && (
            <div className="py-6 flex justify-center items-center mt-4">
              <p className="text-sm text-indigo-300">
                Showing the top {sortedCandidates.length} candidates by overall rating
              </p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
