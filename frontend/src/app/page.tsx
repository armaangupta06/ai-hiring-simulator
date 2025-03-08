"use client";

import { useState, useEffect } from "react";
import { StartingFive } from "@/components/StartingFive";
import { CandidateDetail } from "@/components/CandidateDetail";
import { LandingPage } from "@/components/LandingPage";
import { LoadingAnimation } from "@/components/LoadingAnimation";
import { mockCandidates, mockArchetypes } from "@/data/mockData";
import { CandidateWithRatings, TeamArchetype } from "@/types";
import { BackgroundGradientAnimation } from "@/components/ui/background-gradient-animation";
import { scoreCandidates, generateArchetypes, optimizeTeam } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [showDashboard, setShowDashboard] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(1);
  const [dashboardReady, setDashboardReady] = useState(false);
  const [startupDescription, setStartupDescription] = useState("");
  
  // State for API data
  const [archetypes, setArchetypes] = useState<TeamArchetype[]>(mockArchetypes);
  const [selectedArchetype, setSelectedArchetype] = useState<TeamArchetype | null>(null);
  const [scoredCandidates, setScoredCandidates] = useState<CandidateWithRatings[]>([]);
  const [error, setError] = useState<string | null>(null);
  
  // Split candidates into team and pool
  const [teamCandidates, setTeamCandidates] = useState<CandidateWithRatings[]>([]);
  const [poolCandidates, setPoolCandidates] = useState<CandidateWithRatings[]>([]);
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateWithRatings | null>(null);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  
  // Store the optimization response to access teams for different archetypes
  const [optimizationResponse, setOptimizationResponse] = useState<any>(null);

  // Transform candidate data to match frontend expected structure
  const transformCandidateData = (candidate: any) => {
    // Helper function to ensure a value is an array
    const ensureArray = (value: any): string[] => {
      if (Array.isArray(value)) {
        return value;
      } else if (typeof value === 'string' && value.startsWith('[') && value.endsWith(']')) {
        // Simple fallback for any string representations that might still come through
        try {
          const parsed = JSON.parse(value.replace(/'/g, '"'));
          return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
          console.warn('Failed to parse array string:', value);
          return [];
        }
      } else {
        return [];
      }
    };
    
    // Parse skills using the ensureArray helper
    const skills = ensureArray(candidate.skills);
    
    // Create the ratings object expected by the frontend
    // Prefer z-normalized scores when available
    const ratings = {
      overall: Math.round(candidate.z_normalized_score || (candidate.normalized_overall_score || 0) * 100),
      technical: Math.round(candidate.z_normalized_technical || (candidate.technical_score || 0) * 100),
      education: Math.round(candidate.z_normalized_education || (candidate.education_score || 0) * 100),
      softSkills: Math.round(candidate.z_normalized_soft_skills || (candidate.soft_skills_score || 0) * 100),
      cultureFit: Math.round(candidate.z_normalized_culture_fit || (candidate.culture_fit_score || 0) * 100),
      detailedSkills: [] // Add detailed skills if available
    };
    
    // Return the transformed candidate with the ratings object and normalized data
    return {
      ...candidate,
      skills,
      ratings
    };
  };

  const handleArchetypeChange = (archetype: typeof selectedArchetype) => {
    if (!archetype || !optimizationResponse) return;
    
    setSelectedArchetype(archetype);
    
    // Find the team for the selected archetype
    const selectedTeam = optimizationResponse.teams.find(
      (team: any) => team.archetype_name === archetype.name
    );
    
    if (selectedTeam) {
      // Transform the team members using the same transformation function
      const transformedTeamMembers = selectedTeam.team_members.map(transformCandidateData);
      setTeamCandidates(transformedTeamMembers);
      
      // Update the pool candidates to exclude the new team members
      setPoolCandidates(
        scoredCandidates.filter(
          (c) => !selectedTeam.team_members.some((m: any) => m.name === c.name)
        )
      );
      
      console.log(`Switched to archetype: ${archetype.name} with ${transformedTeamMembers.length} team members`);
    }
  };
  
  // Functions to add/remove/swap candidates
  const addCandidateToTeam = (candidate: CandidateWithRatings) => {
    if (teamCandidates.length >= 5) {
      alert("Your team is already full! Remove a candidate first.");
      return;
    }
    setTeamCandidates([...teamCandidates, candidate]);
    setPoolCandidates(poolCandidates.filter(c => c.name !== candidate.name));
  };

  const removeCandidateFromTeam = (candidate: CandidateWithRatings) => {
    setTeamCandidates(teamCandidates.filter(c => c.name !== candidate.name));
    setPoolCandidates([...poolCandidates, candidate]);
  };
  
  const swapCandidate = (current: CandidateWithRatings, replacement: CandidateWithRatings) => {
    // Remove current candidate from team and add replacement
    const newTeam = teamCandidates.map(c => 
      c.name === current.name ? replacement : c
    );
    
    // Update pool by removing replacement and adding current
    const newPool = poolCandidates
      .filter(c => c.name !== replacement.name)
      .concat(current);
    
    setTeamCandidates(newTeam);
    setPoolCandidates(newPool);
  };
  

  
  const handleViewDetails = (candidate: CandidateWithRatings) => {
    setSelectedCandidate(candidate);
    setIsDetailOpen(true);
  };
  
  const handleCloseDetail = () => {
    setIsDetailOpen(false);
  };

  // Effect to set selected archetype when archetypes are loaded
  useEffect(() => {
    if (archetypes.length > 0 && !selectedArchetype) {
      setSelectedArchetype(archetypes[0]);
    }
  }, [archetypes, selectedArchetype]);

  const handleStartupDescriptionSubmit = async (description: string) => {
    setStartupDescription(description);
    setIsLoading(true);
    setError(null);
    
    try {
      // Step 1: Score candidates
      setLoadingStep(1);
      const scoringResponse = await scoreCandidates({
        startup_description: description,
      });
      
      // Step 2: Generate archetypes
      setLoadingStep(2);
      const archetypesResponse = await generateArchetypes({
        startup_description: description,
        num_archetypes: 3,
        team_size: 5
      });
      
      // Step 3: Optimize team
      setLoadingStep(3);
      const optimizationResponse = await optimizeTeam({
        candidates: scoringResponse.scored_candidates,
        archetypes: archetypesResponse,
        team_size: 5,
        population_size: 975,
        generations: 50
      });
      
      // Store the optimization response for use in archetype switching
      setOptimizationResponse(optimizationResponse);
      
      // Debug: Log the optimization response structure
      console.log('DEBUG - Optimization Response:', optimizationResponse);
      
      // The transformCandidateData function has been moved outside of this function
      
      // Transform all candidates
      const transformedCandidates = scoringResponse.scored_candidates.map(transformCandidateData);
      
      // Update state with transformed results
      setScoredCandidates(transformedCandidates);
      setArchetypes(archetypesResponse);
      
      // DEBUG: Print archetype data
      console.log('DEBUG - Archetypes:', archetypesResponse);
      
      // DEBUG: Print candidate overalls (first 5 candidates)
      console.log('DEBUG - Candidate Overalls (first 5):', 
        transformedCandidates.slice(0, 975).map(c => ({
          name: c.name,
          overall: c.ratings.overall,
          technical: c.ratings.technical,
          education: c.ratings.education,
          softSkills: c.ratings.softSkills,
          cultureFit: c.ratings.cultureFit,
          skills: c.skills
        }))
      );
      
      // Set the first team as the selected team
      if (optimizationResponse.teams.length > 0) {
        const firstTeam = optimizationResponse.teams[0];
        const firstArchetype = archetypesResponse.find(
          (a) => a.name === firstTeam.archetype_name
        );
        
        if (firstArchetype) {
          setSelectedArchetype(firstArchetype);
        }
        

        
        // Transform and split candidates into team and pool
        const transformedTeamMembers = firstTeam.team_members.map(transformCandidateData);
        setTeamCandidates(transformedTeamMembers);
        
        setPoolCandidates(
          transformedCandidates.filter(
            (c) => !firstTeam.team_members.some((m) => m.name === c.name)
          )
        );
      }
      
      // Complete loading and prepare dashboard transition
      setLoadingStep(4);
      
      // First prepare the dashboard in the background
      setDashboardReady(true);
      
      // Small delay before hiding the loading screen
      setTimeout(() => {
        setShowDashboard(true);
        setIsLoading(false);
      }, 800);
    } catch (err) {
      console.error('Error during API calls:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setIsLoading(false);
    }
  };

  // Prepare both views and use AnimatePresence for smooth transitions
  return (
    <>
      <AnimatePresence>
        {!showDashboard && (
          <motion.div
            key="landing"
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
            className="absolute inset-0 z-50"
          >
            <LandingPage onStartupDescriptionSubmit={handleStartupDescriptionSubmit} />
            <LoadingAnimation isLoading={isLoading} currentStep={loadingStep} />
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Dashboard view - preloaded but hidden until ready */}
      <AnimatePresence>
        {dashboardReady && (
          <motion.div
            key="dashboard"
            className="min-h-screen overflow-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: showDashboard ? 1 : 0 }}
            transition={{ duration: 1.2 }}
          >
            <BackgroundGradientAnimation
              gradientBackgroundStart="rgb(12, 12, 24)"
              gradientBackgroundEnd="rgb(8, 8, 16)"
              firstColor="30, 30, 60"
              secondColor="40, 20, 60"
              thirdColor="20, 40, 60"
              fourthColor="25, 25, 50"
              fifthColor="35, 20, 50"
              pointerColor="40, 40, 70"
              size="250%"
              blendingValue="soft-light"
              interactive={true}
              containerClassName="fixed inset-0"
            />
            <motion.div 
              className="relative z-50 flex flex-col min-h-screen pt-6 pointer-events-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: showDashboard ? 1 : 0 }}
              transition={{ duration: 1.5, delay: 0.2 }}
            >
              <motion.main 
                className="flex-1"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: showDashboard ? 1 : 0, y: showDashboard ? 0 : 20 }}
                transition={{ duration: 1.8, delay: 0.4 }}
              >
                {selectedArchetype ? (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: showDashboard ? 1 : 0 }}
                    transition={{ duration: 2, delay: 0.6 }}
                  >
                    <StartingFive 
                      candidates={teamCandidates} 
                      poolCandidates={poolCandidates}
                      archetype={selectedArchetype}
                      archetypes={archetypes}
                      onArchetypeChange={handleArchetypeChange}
                      onRemoveCandidate={removeCandidateFromTeam}
                      onViewDetails={handleViewDetails}
                      onSwapCandidate={swapCandidate}
                    />
                  </motion.div>
                ) : (
                  <div className="flex items-center justify-center h-[600px]">
                    <motion.p 
                      className="text-white text-xl"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.5, repeat: Infinity, repeatType: "reverse" }}
                    >
                      Loading team data...
                    </motion.p>
                  </div>
                )}
              </motion.main>
              
              {/* Candidate Detail Modal */}
              <CandidateDetail 
                candidate={selectedCandidate} 
                isOpen={isDetailOpen} 
                onClose={handleCloseDetail} 
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {error && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-xl">
            <div className="bg-red-900/50 backdrop-blur-md p-6 rounded-lg max-w-md">
              <h3 className="text-xl font-bold text-white mb-2">Error</h3>
              <p className="text-red-200">{error}</p>
              <button 
                onClick={() => setError(null)}
                className="mt-4 px-4 py-2 bg-red-700 hover:bg-red-600 text-white rounded-md"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}
      </>
    );
  }

