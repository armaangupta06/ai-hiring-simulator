import { CandidateWithRatings } from "@/types";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Progress } from "@/components/ui/progress";
import { motion } from "framer-motion";
import { useState } from "react";

interface CandidateCardProps {
  candidate: CandidateWithRatings;
  onClick: (candidate: CandidateWithRatings) => void;
  isSelected: boolean;
  onAddToTeam?: (candidate: CandidateWithRatings) => void;
  onRemoveFromTeam?: (candidate: CandidateWithRatings) => void;
  scrollDarkening?: boolean;
}

export function CandidateCard({ candidate, onClick, isSelected, onAddToTeam, onRemoveFromTeam, scrollDarkening = false }: CandidateCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  
  // Get initials for avatar
  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  // Get color based on rating (Purple/Blue scheme)
  const getRatingColor = (rating: number) => {
    if (rating >= 90) return "text-indigo-400"; // Indigo for 90+
    if (rating >= 80) return "text-violet-400"; // Violet for 80-89
    if (rating >= 70) return "text-blue-400";   // Blue for 70-79
    if (rating >= 60) return "text-sky-400";    // Sky for 60-69
    return "text-slate-400";                    // Slate for below 60
  };
  
  // Get background color for progress bars (with higher contrast)
  const getProgressBarColor = (rating: number) => {
    if (rating >= 90) return "bg-indigo-500"; // Brighter indigo for 90+
    if (rating >= 80) return "bg-violet-500"; // Brighter violet for 80-89
    if (rating >= 70) return "bg-blue-500";   // Brighter blue for 70-79
    if (rating >= 60) return "bg-sky-500";    // Brighter sky for 60-69
    return "bg-slate-500";                    // Brighter slate for below 60
  };

  return (
    <motion.div
      whileHover={{ 
        scale: 1.05,
        boxShadow: "0px 0px 8px rgba(255, 255, 255, 0.3)",
        borderRadius: "0.75rem"
      }}
      whileTap={{ scale: 0.95 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      onClick={() => onClick(candidate)}
      className={`cursor-pointer h-full w-full rounded-xl ${isSelected ? 'ring-2 ring-primary ring-offset-2 ring-offset-background' : ''}`}
      style={{ minWidth: '370px' }} /* Increased minimum width to fit longer names */
    >
      <Card className="overflow-hidden border-zinc-800/50 h-full w-full relative backdrop-blur-sm flex flex-col p-0 w-full">
        <div className="relative h-full flex-1 flex flex-col">
          {/* Purple/Blue mesh gradient background */}
          <div className="absolute inset-0 z-0 bg-zinc-950/90 rounded-xl">
            <div 
              className="absolute inset-0 animate-gradient-slow opacity-60"
              style={{
                backgroundSize: '200% 200%',
                backgroundImage: `radial-gradient(circle at 20% 30%, 
                  ${(candidate.ratings?.overall || 0) >= 90 ? 'rgba(99, 102, 241, 0.7), rgba(79, 70, 229, 0)' : 
                    (candidate.ratings?.overall || 0) >= 85 ? 'rgba(124, 58, 237, 0.7), rgba(109, 40, 217, 0)' :
                    (candidate.ratings?.overall || 0) >= 80 ? 'rgba(79, 70, 229, 0.7), rgba(67, 56, 202, 0)' :
                    (candidate.ratings?.overall || 0) >= 70 ? 'rgba(59, 130, 246, 0.7), rgba(37, 99, 235, 0)' :
                    'rgba(56, 189, 248, 0.7), rgba(14, 165, 233, 0)'}
                )`
              }}
            />
            <div 
              className="absolute inset-0 animate-gradient-slow-reverse opacity-60"
              style={{
                backgroundSize: '200% 200%',
                backgroundImage: `radial-gradient(circle at 80% 70%, 
                  ${(candidate.ratings?.overall || 0) >= 90 ? 'rgba(79, 70, 229, 0.5), rgba(99, 102, 241, 0)' : 
                    (candidate.ratings?.overall || 0) >= 85 ? 'rgba(109, 40, 217, 0.5), rgba(124, 58, 237, 0)' :
                    (candidate.ratings?.overall || 0) >= 80 ? 'rgba(67, 56, 202, 0.5), rgba(79, 70, 229, 0)' :
                    (candidate.ratings?.overall || 0) >= 70 ? 'rgba(37, 99, 235, 0.5), rgba(59, 130, 246, 0)' :
                    'rgba(14, 165, 233, 0.5), rgba(56, 189, 248, 0)'}
                )`
              }}
            />
          </div>
          
          {/* Premium trim for high-rated candidates */}
          {(candidate.ratings?.overall || 0) >= 85 && (
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 via-violet-500/5 to-indigo-500/10 animate-shimmer rounded-xl" />
          )}
          
          <div className="p-5 pr-6 pb-16 relative h-full flex flex-col flex-1 z-10">
            <div className="flex justify-between items-start mb-3">
              <div className="flex items-center gap-3 min-w-0 flex-shrink">
                <Avatar className="h-12 w-12 border-2 border-indigo-700/50 shadow-md flex-shrink-0">
                  <AvatarFallback className="bg-indigo-900/70 text-white font-semibold">
                    {getInitials(candidate.name)}
                  </AvatarFallback>
                </Avatar>
                
                <div className="min-w-0 flex-1 pr-2"> {/* Added right padding */}
                  <h3 className="text-xl font-bold text-white truncate">{candidate.name}</h3>
                  <p className="text-indigo-200/80 truncate">{candidate.location}</p>
                  <p className="text-blue-300/60 text-sm truncate">
                    {candidate.work_experiences && candidate.work_experiences[0]?.roleName}
                  </p>
                </div>
              </div>
              
              {/* Overall Rating */}
              <div className="flex flex-col items-center flex-shrink-0 ml-2">
                <div className={`text-4xl font-bold ${getRatingColor(candidate.ratings?.overall || 0)}`}>
                  {candidate.ratings?.overall || 0}
                </div>
                <div className="text-xs text-indigo-200/50">OVR</div>
              </div>
            </div>
            
            <CardContent className="p-0 mt-3">
              <div className="grid grid-cols-4 gap-2 mt-2 secondary-content transition-opacity duration-300">
                {/* Technical Rating */}
                <div className="flex flex-col">
                  <div className="flex justify-between mb-1">
                    <span className="text-xs font-medium text-indigo-200/70">TECH</span>
                    <span className={`text-xs font-bold ${getRatingColor(candidate.ratings?.technical || 0)}`}>
                      {candidate.ratings?.technical || 0}
                    </span>
                  </div>
                  <Progress 
                    value={candidate.ratings?.technical || 0} 
                    className="h-1.5 bg-indigo-900/30 rounded-full" 
                    indicatorClassName={getProgressBarColor(candidate.ratings?.technical || 0)}
                  />
                </div>
                
                {/* Education Rating */}
                <div className="flex flex-col">
                  <div className="flex justify-between mb-1">
                    <span className="text-xs font-medium text-indigo-200/70">EDU</span>
                    <span className={`text-xs font-bold ${getRatingColor(candidate.ratings?.education || 0)}`}>
                      {candidate.ratings?.education || 0}
                    </span>
                  </div>
                  <Progress 
                    value={candidate.ratings?.education || 0} 
                    className="h-1.5 bg-indigo-900/30 rounded-full" 
                    indicatorClassName={getProgressBarColor(candidate.ratings?.education || 0)}
                  />
                </div>
                
                {/* Soft Skills Rating */}
                <div className="flex flex-col">
                  <div className="flex justify-between mb-1">
                    <span className="text-xs font-medium text-indigo-200/70">SOFT</span>
                    <span className={`text-xs font-bold ${getRatingColor(candidate.ratings?.softSkills || 0)}`}>
                      {candidate.ratings?.softSkills || 0}
                    </span>
                  </div>
                  <Progress 
                    value={candidate.ratings?.softSkills || 0} 
                    className="h-1.5 bg-indigo-900/30 rounded-full" 
                    indicatorClassName={getProgressBarColor(candidate.ratings?.softSkills || 0)}
                  />
                </div>
                
                {/* Culture Fit Rating */}
                <div className="flex flex-col">
                  <div className="flex justify-between mb-1">
                    <span className="text-xs font-medium text-indigo-200/70">FIT</span>
                    <span className={`text-xs font-bold ${getRatingColor(candidate.ratings?.cultureFit || 0)}`}>
                      {candidate.ratings?.cultureFit || 0}
                    </span>
                  </div>
                  <Progress 
                    value={candidate.ratings?.cultureFit || 0} 
                    className="h-1.5 bg-indigo-900/30 rounded-full" 
                    indicatorClassName={getProgressBarColor(candidate.ratings?.cultureFit || 0)}
                  />
                </div>
              </div>
              
              {/* Top Skills */}
              <div className="mt-4 secondary-content transition-opacity duration-300">
                <div className="flex flex-wrap gap-1.5">
                  {Array.isArray(candidate.skills) && candidate.skills.slice(0, 3).map((skill, index) => (
                    <span 
                      key={index} 
                      className="text-xs px-2.5 py-1 rounded-full bg-indigo-900/50 text-indigo-200 border border-indigo-700/30 shadow-sm"
                    >
                      {skill}
                    </span>
                  ))}
                  {Array.isArray(candidate.skills) && candidate.skills.length > 3 && (
                    <span className="text-xs px-2.5 py-1 rounded-full bg-blue-900/50 text-blue-200 border border-blue-700/30 shadow-sm">
                      +{candidate.skills.length - 3}
                    </span>
                  )}
                </div>
              </div>
              
              {/* Action buttons - shown on hover */}
              <div className={`absolute bottom-4 right-4 transition-opacity duration-200 ${isHovered ? 'opacity-100' : 'opacity-0'}`}>
                {onAddToTeam && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onAddToTeam(candidate);
                    }}
                    className="bg-indigo-500 hover:bg-indigo-600 text-white rounded-full p-2 shadow-lg"
                    title="Add to Starting Five"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                )}
                
                {onRemoveFromTeam && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onRemoveFromTeam(candidate);
                    }}
                    className="bg-red-500 hover:bg-red-600 text-white rounded-full p-2 shadow-lg"
                    title="Remove from Starting Five"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                )}
              </div>
            </CardContent>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
