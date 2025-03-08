import { useState, useEffect } from "react";
import { CandidateWithRatings, TeamArchetype } from "@/types";
import { CandidateCard } from "./CandidateCard";
import { motion } from "framer-motion";
import { ArrowsRightLeftIcon } from "@heroicons/react/24/solid";
import { SwapCandidateModal } from "./SwapCandidateModal";

interface StartingFiveProps {
  candidates: CandidateWithRatings[];
  poolCandidates: CandidateWithRatings[];
  archetype: TeamArchetype;
  archetypes: TeamArchetype[];
  onArchetypeChange: (archetype: TeamArchetype) => void;
  onRemoveCandidate?: (candidate: CandidateWithRatings) => void;
  onViewDetails?: (candidate: CandidateWithRatings) => void;
  onSwapCandidate?: (current: CandidateWithRatings, replacement: CandidateWithRatings) => void;
}

export function StartingFive({ 
  candidates, 
  poolCandidates, 
  archetype, 
  archetypes,
  onArchetypeChange,
  onRemoveCandidate, 
  onViewDetails,
  onSwapCandidate 
}: StartingFiveProps) {
  const [swapModalOpen, setSwapModalOpen] = useState(false);
  const [candidateToSwap, setCandidateToSwap] = useState<CandidateWithRatings | null>(null);
  const [scrolled, setScrolled] = useState(false);
  
  const handleCandidateClick = (candidate: CandidateWithRatings) => {
    if (onViewDetails) {
      onViewDetails(candidate);
    }
  };

  // Calculate team average ratings
  const calculateTeamAverages = () => {
    if (candidates.length === 0) return { overall: 0, technical: 0, education: 0, softSkills: 0 };
    
    // Add safety checks for missing ratings
    const overall = Math.round(candidates.reduce((sum, c) => {
      const rating = c.ratings?.overall || 0;
      return sum + rating;
    }, 0) / candidates.length);
    
    const technical = Math.round(candidates.reduce((sum, c) => {
      const rating = c.ratings?.technical || 0;
      return sum + rating;
    }, 0) / candidates.length);
    
    const education = Math.round(candidates.reduce((sum, c) => {
      const rating = c.ratings?.education || 0;
      return sum + rating;
    }, 0) / candidates.length);
    
    const softSkills = Math.round(candidates.reduce((sum, c) => {
      const rating = c.ratings?.softSkills || 0;
      return sum + rating;
    }, 0) / candidates.length);
    
    return { overall, technical, education, softSkills };
  };

  const teamAverages = calculateTeamAverages();

  // Get color based on rating (Purple/Blue scheme)
  const getRatingColor = (rating: number) => {
    if (rating >= 90) return "text-indigo-400"; // Indigo for 90+
    if (rating >= 80) return "text-violet-400"; // Violet for 80-89
    if (rating >= 70) return "text-blue-400";   // Blue for 70-79
    if (rating >= 60) return "text-sky-400";    // Sky for 60-69
    return "text-slate-400";                    // Slate for below 60
  };
  
  // Add scroll event listener to track scroll position for darkening effect
  useEffect(() => {
    const handleScroll = () => {
      const headerHeight = document.getElementById('header-section')?.offsetHeight || 300;
      const scrollY = window.scrollY;
      
      // Set scrolled state for basic visibility toggling
      setScrolled(scrollY > headerHeight - 100);
      
      // Apply gradual darkening effect based on scroll position
      const maxScroll = 500; // Maximum scroll value for full effect
      const scrollRatio = Math.min(scrollY / maxScroll, 1);
      
      // Apply darkening to technical, education, and soft skills stats
      const statsElements = document.querySelectorAll('.stat-category:not(.overall)');
      statsElements.forEach(element => {
        const opacity = 1 - (scrollRatio * 0.6); // Darken up to 60%
        (element as HTMLElement).style.opacity = opacity.toString();
      });
      
      // Apply darkening to the description and archetype selector
      const descriptionElement = document.getElementById('archetype-description');
      if (descriptionElement) {
        const descOpacity = 1 - (scrollRatio * 0.7); // Darken up to 70%
        descriptionElement.style.opacity = descOpacity.toString();
      }
      
      // Apply darkening to candidate cards except the main content
      const cardElements = document.querySelectorAll('.candidate-card .secondary-content');
      cardElements.forEach(element => {
        const cardOpacity = 1 - (scrollRatio * 0.5); // Darken up to 50%
        (element as HTMLElement).style.opacity = cardOpacity.toString();
      });
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="container mx-auto px-6 max-w-[1800px] pb-20">
      {/* Sticky Team Stats */}
      <div className="fixed top-4 right-4 z-50 flex items-center gap-2 md:gap-3 flex-wrap md:flex-nowrap bg-black/40 backdrop-blur-md p-2 rounded-xl border border-indigo-700/30 shadow-lg shadow-indigo-900/20">
        <div className="flex flex-col items-center px-3 py-1.5 overall stat-category transition-opacity duration-300">
          <span className="text-xs font-medium text-indigo-200/80 uppercase tracking-wider">OVERALL</span>
          <span className={`text-2xl font-bold ${getRatingColor(teamAverages.overall)}`}>
            {teamAverages.overall}
          </span>
        </div>
        <div className="flex flex-col items-center px-3 py-1.5 stat-category transition-opacity duration-300">
          <span className="text-xs font-medium text-indigo-200/80 uppercase tracking-wider">TECH</span>
          <span className={`text-2xl font-bold ${getRatingColor(teamAverages.technical)}`}>
            {teamAverages.technical}
          </span>
        </div>
        <div className="flex flex-col items-center px-3 py-1.5 stat-category transition-opacity duration-300">
          <span className="text-xs font-medium text-indigo-200/80 uppercase tracking-wider">EDU</span>
          <span className={`text-2xl font-bold ${getRatingColor(teamAverages.education)}`}>
            {teamAverages.education}
          </span>
        </div>
        <div className="flex flex-col items-center px-3 py-1.5 stat-category transition-opacity duration-300">
          <span className="text-xs font-medium text-indigo-200/80 uppercase tracking-wider">SOFT</span>
          <span className={`text-2xl font-bold ${getRatingColor(teamAverages.softSkills)}`}>
            {teamAverages.softSkills}
          </span>
        </div>
      </div>

      {/* Header Section with overlay when scrolled */}
      <section 
        id="header-section"
        className={`relative py-8 mb-6 transition-all duration-300 ${scrolled ? 'opacity-40' : 'opacity-100'}`}
      >
        <motion.div 
          className="relative z-10"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative">
            <div className="relative z-10">
              <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 via-purple-400 to-blue-300 tracking-tight">
                Starting Five
              </h1>
              <div className="flex items-center gap-2 mt-2">
                <div className="h-1.5 w-1.5 rounded-full bg-indigo-400 animate-pulse"></div>
                <p className="text-indigo-200/90 font-medium">Archetype: {archetype.name}</p>
              </div>
            </div>
          </div>
          
          <div className="mt-6 max-w-3xl">
            <div className="flex flex-col gap-4">
              {/* Archetype Selector */}
              <div className="backdrop-blur-md bg-black/10 rounded-full p-1 flex self-start mb-2">
                {archetypes.map((arch) => (
                  <button
                    key={arch.name}
                    onClick={() => onArchetypeChange(arch)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${arch.name === archetype.name
                      ? "bg-gradient-to-r from-indigo-500 to-indigo-600 text-white shadow-md"
                      : "text-zinc-300 hover:text-white"
                    }`}
                  >
                    {arch.name}
                  </button>
                ))}
              </div>
              
              {/* Archetype Description */}
              <p id="archetype-description" className="text-sm text-blue-200/70 leading-relaxed backdrop-blur-sm py-3 px-4 rounded-lg bg-blue-900/10 border border-blue-800/20 transition-opacity duration-300">
                {archetype.description}
              </p>
            </div>
          </div>
        </motion.div>
      </section>
      
      {/* Cards Section with overlay when not scrolled */}
      <section className={`relative transition-all duration-300 ${scrolled ? 'opacity-100' : 'opacity-90'}`}>
        {!scrolled && (
          <div className="absolute inset-0 bg-black/20 backdrop-blur-sm rounded-2xl z-10"></div>
        )}
        
        <div className="relative z-20">
          {/* Candidates Grid */}
          <div className="flex flex-wrap justify-center gap-8 py-4 min-h-[600px]">
            {candidates.map((candidate, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="w-[380px] relative" /* Increased width from 350px to 380px */
              >
                <div className="h-full">
                  <CandidateCard 
                    candidate={candidate} 
                    onClick={handleCandidateClick}
                    isSelected={false}
                    scrollDarkening={scrolled}
                  />
                  {/* Swap button with improved styling */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setCandidateToSwap(candidate);
                      setSwapModalOpen(true);
                    }}
                    className="absolute bottom-4 right-4 bg-indigo-500 hover:bg-indigo-600 text-white rounded-full p-2 shadow-lg z-20 transition-opacity duration-200 opacity-70 hover:opacity-100"
                    title="Swap Candidate"
                  >
                    <ArrowsRightLeftIcon className="h-5 w-5" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Swap Candidate Modal */}
      <SwapCandidateModal
        isOpen={swapModalOpen}
        onClose={() => setSwapModalOpen(false)}
        currentCandidate={candidateToSwap}
        poolCandidates={poolCandidates}
        onSwapCandidate={(current, replacement) => {
          setSwapModalOpen(false);
          if (onSwapCandidate) {
            onSwapCandidate(current, replacement);
          }
        }}
      />
    </div>
  );
}
