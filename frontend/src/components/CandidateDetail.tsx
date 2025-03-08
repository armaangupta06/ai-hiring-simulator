import { CandidateWithRatings } from "@/types";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { motion } from "framer-motion";

interface CandidateDetailProps {
  candidate: CandidateWithRatings | null;
  isOpen: boolean;
  onClose: () => void;
}

export function CandidateDetail({ candidate, isOpen, onClose }: CandidateDetailProps) {
  if (!candidate) return null;

  // Get initials for avatar
  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  // Get color based on rating (NBA 2K style)
  const getRatingColor = (rating: number) => {
    if (rating >= 90) return "text-emerald-400"; // Green for 90+
    if (rating >= 80) return "text-blue-400";    // Blue for 80-89
    if (rating >= 70) return "text-yellow-400";  // Yellow for 70-79
    if (rating >= 60) return "text-orange-400";  // Orange for 60-69
    return "text-red-400";                       // Red for below 60
  };

  const getBgColor = (rating: number) => {
    if (rating >= 90) return "bg-emerald-400"; // Green for 90+
    if (rating >= 80) return "bg-blue-400";    // Blue for 80-89
    if (rating >= 70) return "bg-yellow-400";  // Yellow for 70-79
    if (rating >= 60) return "bg-orange-400";  // Orange for 60-69
    return "bg-red-400";                       // Red for below 60
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[600px] bg-zinc-900 border-zinc-800 text-white">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">Candidate Profile</DialogTitle>
        </DialogHeader>
        
        <div className="grid grid-cols-[1fr_auto] gap-6 py-4">
          {/* Left column - Candidate info */}
          <div>
            <div className="flex items-center gap-4 mb-6">
              <Avatar className="h-20 w-20 border-2 border-zinc-700">
                <AvatarFallback className="bg-zinc-800 text-white text-xl">
                  {getInitials(candidate.name)}
                </AvatarFallback>
              </Avatar>
              
              <div>
                <h3 className="text-2xl font-bold text-white">{candidate.name}</h3>
                <p className="text-zinc-400">{candidate.location}</p>
                <p className="text-zinc-500">
                  {candidate.work_experiences && candidate.work_experiences[0]?.roleName} at {candidate.work_experiences && candidate.work_experiences[0]?.company}
                </p>
              </div>
            </div>
            
            <Separator className="my-4 bg-zinc-800" />
            
            {/* Education */}
            <div className="mb-4">
              <h4 className="text-lg font-semibold mb-2">Education</h4>
              {candidate.education?.degrees?.map((degree, index) => (
                <div key={index} className="mb-2">
                  <p className="text-white">{degree.degree} in {degree.subject}</p>
                  <p className="text-zinc-400 text-sm">{degree.school} {degree.isTop25 ? '(Top 25)' : degree.isTop50 ? '(Top 50)' : ''}</p>
                  <p className="text-zinc-500 text-sm">{degree.gpa}</p>
                </div>
              ))}
            </div>
            
            {/* Work Experience */}
            <div className="mb-4">
              <h4 className="text-lg font-semibold mb-2">Work Experience</h4>
              {candidate.work_experiences?.map((experience, index) => (
                <div key={index} className="mb-2">
                  <p className="text-white">{experience.roleName}</p>
                  <p className="text-zinc-400 text-sm">{experience.company}</p>
                </div>
              ))}
            </div>
            
            {/* Skills */}
            <div>
              <h4 className="text-lg font-semibold mb-2">Skills</h4>
              <div className="flex flex-wrap gap-2">
                {candidate.skills?.map((skill, index) => (
                  <span 
                    key={index} 
                    className="text-sm px-3 py-1 rounded-full bg-zinc-800 text-zinc-300"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
          
          {/* Right column - Ratings */}
          <div className="flex flex-col items-center border-l border-zinc-800 pl-6">
            {/* Overall Rating */}
            <div className="flex flex-col items-center mb-6">
              <div className={`text-6xl font-bold ${getRatingColor(candidate.ratings.overall)}`}>
                {candidate.ratings.overall}
              </div>
              <div className="text-sm text-zinc-400 mt-1">OVERALL</div>
            </div>
            
            {/* Main Ratings */}
            <div className="space-y-6 w-full">
              {/* Technical Rating */}
              <div className="flex flex-col">
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-zinc-400">TECHNICAL</span>
                  <span className={`text-sm font-bold ${getRatingColor(candidate.ratings.technical)}`}>
                    {candidate.ratings.technical}
                  </span>
                </div>
                <Progress 
                  value={candidate.ratings.technical} 
                  className="h-2 bg-zinc-800" 
                  indicatorClassName={getBgColor(candidate.ratings.technical)}
                />
              </div>
              
              {/* Education Rating */}
              <div className="flex flex-col">
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-zinc-400">EDUCATION</span>
                  <span className={`text-sm font-bold ${getRatingColor(candidate.ratings.education)}`}>
                    {candidate.ratings.education}
                  </span>
                </div>
                <Progress 
                  value={candidate.ratings.education} 
                  className="h-2 bg-zinc-800" 
                  indicatorClassName={getBgColor(candidate.ratings.education)}
                />
              </div>
              
              {/* Soft Skills Rating */}
              <div className="flex flex-col">
                <div className="flex justify-between mb-1">
                  <span className="text-sm text-zinc-400">SOFT SKILLS</span>
                  <span className={`text-sm font-bold ${getRatingColor(candidate.ratings.softSkills)}`}>
                    {candidate.ratings.softSkills}
                  </span>
                </div>
                <Progress 
                  value={candidate.ratings.softSkills} 
                  className="h-2 bg-zinc-800" 
                  indicatorClassName={getBgColor(candidate.ratings.softSkills)}
                />
              </div>
            </div>
            
            {/* Detailed Skills Ratings */}
            <div className="mt-6 w-full">
              <h4 className="text-sm font-semibold mb-3 text-zinc-400">DETAILED SKILLS</h4>
              <div className="space-y-3">
                {candidate.ratings.detailedSkills.map((skill, index) => (
                  <div key={index} className="flex flex-col">
                    <div className="flex justify-between mb-1">
                      <span className="text-xs text-zinc-500">{skill.name}</span>
                      <span className={`text-xs font-bold ${getRatingColor(skill.value)}`}>
                        {skill.value}
                      </span>
                    </div>
                    <Progress 
                      value={skill.value} 
                      max={skill.maxValue}
                      className="h-1 bg-zinc-800" 
                      indicatorClassName={getBgColor(skill.value)}
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
