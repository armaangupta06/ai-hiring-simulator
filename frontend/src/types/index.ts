export interface Candidate {
  name: string;
  email?: string;
  phone?: string;
  location?: string;
  submitted_at?: string;
  work_availability?: string[];
  work_experiences?: {
    company: string;
    roleName: string;
  }[];
  skills?: string[];
  education?: {
    highest_level?: string;
    degrees?: {
      degree: string;
      subject: string;
      school: string;
      gpa?: string;
      startDate?: string;
      endDate?: string;
      isTop50?: boolean;
      isTop25?: boolean;
    }[];
  };
  salary?: number;
  technical_score?: number;
  education_score?: number;
  soft_skills_score?: number;
  culture_fit_score?: number;
  normalized_overall_score?: number;
  z_normalized_score?: number;
  z_normalized_technical?: number;
  z_normalized_education?: number;
  z_normalized_soft_skills?: number;
  z_normalized_culture_fit?: number;
  cluster?: number;
}

export interface SkillRating {
  name: string;
  value: number;
  maxValue: number;
}

export interface CandidateWithRatings extends Candidate {
  ratings: {
    overall: number;
    technical: number;
    education: number;
    softSkills: number;
    cultureFit?: number; // Added culture fit rating
    detailedSkills: SkillRating[];
  };
}

export interface TeamArchetype {
  name: string;
  description: string;
  weightings: {
    individual_quality: number;
    team_synergy: number;
    team_diversity: number;
  };
}
