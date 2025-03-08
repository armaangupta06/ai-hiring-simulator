import { CandidateWithRatings, TeamArchetype } from "@/types";

export const mockCandidates: CandidateWithRatings[] = [
  {
    name: "Alex Johnson",
    location: "San Francisco, CA",
    work_experiences: [
      { company: "Google", roleName: "Senior Software Engineer" },
      { company: "Facebook", roleName: "Software Engineer" },
    ],
    skills: ["Python", "Machine Learning", "AWS", "React", "TypeScript"],
    education: {
      highest_level: "Master's Degree",
      degrees: [
        {
          degree: "Master's Degree",
          subject: "Computer Science",
          school: "Stanford University",
          gpa: "GPA 3.9",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.92,
    education_score: 0.89,
    soft_skills_score: 0.78,
    normalized_overall_score: 0.88,
    ratings: {
      overall: 88,
      technical: 92,
      education: 89,
      softSkills: 78,
      detailedSkills: [
        { name: "Python", value: 94, maxValue: 100 },
        { name: "Machine Learning", value: 90, maxValue: 100 },
        { name: "AWS", value: 85, maxValue: 100 },
        { name: "React", value: 82, maxValue: 100 },
        { name: "TypeScript", value: 88, maxValue: 100 },
      ],
    },
  },
  {
    name: "Maya Rodriguez",
    location: "New York, NY",
    work_experiences: [
      { company: "Amazon", roleName: "Data Scientist" },
      { company: "IBM", roleName: "ML Engineer" },
    ],
    skills: ["Python", "TensorFlow", "PyTorch", "SQL", "Data Visualization"],
    education: {
      highest_level: "PhD",
      degrees: [
        {
          degree: "PhD",
          subject: "Machine Learning",
          school: "MIT",
          gpa: "GPA 4.0",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.95,
    education_score: 0.96,
    soft_skills_score: 0.82,
    normalized_overall_score: 0.91,
    ratings: {
      overall: 91,
      technical: 95,
      education: 96,
      softSkills: 82,
      detailedSkills: [
        { name: "Python", value: 96, maxValue: 100 },
        { name: "TensorFlow", value: 93, maxValue: 100 },
        { name: "PyTorch", value: 92, maxValue: 100 },
        { name: "SQL", value: 88, maxValue: 100 },
        { name: "Data Visualization", value: 90, maxValue: 100 },
      ],
    },
  },
  {
    name: "David Chen",
    location: "Seattle, WA",
    work_experiences: [
      { company: "Microsoft", roleName: "Product Manager" },
      { company: "Dropbox", roleName: "Software Engineer" },
    ],
    skills: ["Product Management", "JavaScript", "React", "User Research", "Agile"],
    education: {
      highest_level: "Bachelor's Degree",
      degrees: [
        {
          degree: "Bachelor's Degree",
          subject: "Computer Science",
          school: "UC Berkeley",
          gpa: "GPA 3.7",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.79,
    education_score: 0.82,
    soft_skills_score: 0.93,
    normalized_overall_score: 0.84,
    ratings: {
      overall: 84,
      technical: 79,
      education: 82,
      softSkills: 93,
      detailedSkills: [
        { name: "Product Management", value: 95, maxValue: 100 },
        { name: "JavaScript", value: 85, maxValue: 100 },
        { name: "React", value: 83, maxValue: 100 },
        { name: "User Research", value: 92, maxValue: 100 },
        { name: "Agile", value: 91, maxValue: 100 },
      ],
    },
  },
  {
    name: "Sarah Kim",
    location: "Austin, TX",
    work_experiences: [
      { company: "Apple", roleName: "UX Designer" },
      { company: "Airbnb", roleName: "Product Designer" },
    ],
    skills: ["UI/UX Design", "Figma", "Sketch", "User Testing", "Prototyping"],
    education: {
      highest_level: "Master's Degree",
      degrees: [
        {
          degree: "Master's Degree",
          subject: "Human-Computer Interaction",
          school: "Carnegie Mellon University",
          gpa: "GPA 3.8",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.81,
    education_score: 0.88,
    soft_skills_score: 0.90,
    normalized_overall_score: 0.86,
    ratings: {
      overall: 86,
      technical: 81,
      education: 88,
      softSkills: 90,
      detailedSkills: [
        { name: "UI/UX Design", value: 94, maxValue: 100 },
        { name: "Figma", value: 92, maxValue: 100 },
        { name: "Sketch", value: 88, maxValue: 100 },
        { name: "User Testing", value: 91, maxValue: 100 },
        { name: "Prototyping", value: 89, maxValue: 100 },
      ],
    },
  },
  {
    name: "James Wilson",
    location: "Chicago, IL",
    work_experiences: [
      { company: "Salesforce", roleName: "DevOps Engineer" },
      { company: "Oracle", roleName: "Systems Administrator" },
    ],
    skills: ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"],
    education: {
      highest_level: "Bachelor's Degree",
      degrees: [
        {
          degree: "Bachelor's Degree",
          subject: "Information Technology",
          school: "University of Illinois",
          gpa: "GPA 3.5",
          isTop50: true,
        },
      ],
    },
    technical_score: 0.87,
    education_score: 0.75,
    soft_skills_score: 0.80,
    normalized_overall_score: 0.82,
    ratings: {
      overall: 82,
      technical: 87,
      education: 75,
      softSkills: 80,
      detailedSkills: [
        { name: "Docker", value: 91, maxValue: 100 },
        { name: "Kubernetes", value: 89, maxValue: 100 },
        { name: "CI/CD", value: 88, maxValue: 100 },
        { name: "AWS", value: 90, maxValue: 100 },
        { name: "Terraform", value: 86, maxValue: 100 },
      ],
    },
  },
  {
    name: "Alex Johnson",
    location: "San Francisco, CA",
    work_experiences: [
      { company: "Google", roleName: "Senior Software Engineer" },
      { company: "Facebook", roleName: "Software Engineer" },
    ],
    skills: ["Python", "Machine Learning", "AWS", "React", "TypeScript"],
    education: {
      highest_level: "Master's Degree",
      degrees: [
        {
          degree: "Master's Degree",
          subject: "Computer Science",
          school: "Stanford University",
          gpa: "GPA 3.9",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.92,
    education_score: 0.89,
    soft_skills_score: 0.78,
    normalized_overall_score: 0.88,
    ratings: {
      overall: 88,
      technical: 92,
      education: 89,
      softSkills: 78,
      detailedSkills: [
        { name: "Python", value: 94, maxValue: 100 },
        { name: "Machine Learning", value: 90, maxValue: 100 },
        { name: "AWS", value: 85, maxValue: 100 },
        { name: "React", value: 82, maxValue: 100 },
        { name: "TypeScript", value: 88, maxValue: 100 },
      ],
    },
  },
  {
    name: "Maya Rodriguez",
    location: "New York, NY",
    work_experiences: [
      { company: "Amazon", roleName: "Data Scientist" },
      { company: "IBM", roleName: "ML Engineer" },
    ],
    skills: ["Python", "TensorFlow", "PyTorch", "SQL", "Data Visualization"],
    education: {
      highest_level: "PhD",
      degrees: [
        {
          degree: "PhD",
          subject: "Machine Learning",
          school: "MIT",
          gpa: "GPA 4.0",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.95,
    education_score: 0.96,
    soft_skills_score: 0.82,
    normalized_overall_score: 0.91,
    ratings: {
      overall: 91,
      technical: 95,
      education: 96,
      softSkills: 82,
      detailedSkills: [
        { name: "Python", value: 96, maxValue: 100 },
        { name: "TensorFlow", value: 93, maxValue: 100 },
        { name: "PyTorch", value: 92, maxValue: 100 },
        { name: "SQL", value: 88, maxValue: 100 },
        { name: "Data Visualization", value: 90, maxValue: 100 },
      ],
    },
  },
  {
    name: "David Chen",
    location: "Seattle, WA",
    work_experiences: [
      { company: "Microsoft", roleName: "Product Manager" },
      { company: "Dropbox", roleName: "Software Engineer" },
    ],
    skills: ["Product Management", "JavaScript", "React", "User Research", "Agile"],
    education: {
      highest_level: "Bachelor's Degree",
      degrees: [
        {
          degree: "Bachelor's Degree",
          subject: "Computer Science",
          school: "UC Berkeley",
          gpa: "GPA 3.7",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.79,
    education_score: 0.82,
    soft_skills_score: 0.93,
    normalized_overall_score: 0.84,
    ratings: {
      overall: 84,
      technical: 79,
      education: 82,
      softSkills: 93,
      detailedSkills: [
        { name: "Product Management", value: 95, maxValue: 100 },
        { name: "JavaScript", value: 85, maxValue: 100 },
        { name: "React", value: 83, maxValue: 100 },
        { name: "User Research", value: 92, maxValue: 100 },
        { name: "Agile", value: 91, maxValue: 100 },
      ],
    },
  },
  {
    name: "Sarah Kim",
    location: "Austin, TX",
    work_experiences: [
      { company: "Apple", roleName: "UX Designer" },
      { company: "Airbnb", roleName: "Product Designer" },
    ],
    skills: ["UI/UX Design", "Figma", "Sketch", "User Testing", "Prototyping"],
    education: {
      highest_level: "Master's Degree",
      degrees: [
        {
          degree: "Master's Degree",
          subject: "Human-Computer Interaction",
          school: "Carnegie Mellon University",
          gpa: "GPA 3.8",
          isTop25: true,
        },
      ],
    },
    technical_score: 0.81,
    education_score: 0.88,
    soft_skills_score: 0.90,
    normalized_overall_score: 0.86,
    ratings: {
      overall: 86,
      technical: 81,
      education: 88,
      softSkills: 90,
      detailedSkills: [
        { name: "UI/UX Design", value: 94, maxValue: 100 },
        { name: "Figma", value: 92, maxValue: 100 },
        { name: "Sketch", value: 88, maxValue: 100 },
        { name: "User Testing", value: 91, maxValue: 100 },
        { name: "Prototyping", value: 89, maxValue: 100 },
      ],
    },
  },
  {
    name: "James Wilson",
    location: "Chicago, IL",
    work_experiences: [
      { company: "Salesforce", roleName: "DevOps Engineer" },
      { company: "Oracle", roleName: "Systems Administrator" },
    ],
    skills: ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"],
    education: {
      highest_level: "Bachelor's Degree",
      degrees: [
        {
          degree: "Bachelor's Degree",
          subject: "Information Technology",
          school: "University of Illinois",
          gpa: "GPA 3.5",
          isTop50: true,
        },
      ],
    },
    technical_score: 0.87,
    education_score: 0.75,
    soft_skills_score: 0.80,
    normalized_overall_score: 0.82,
    ratings: {
      overall: 82,
      technical: 87,
      education: 75,
      softSkills: 80,
      detailedSkills: [
        { name: "Docker", value: 91, maxValue: 100 },
        { name: "Kubernetes", value: 89, maxValue: 100 },
        { name: "CI/CD", value: 88, maxValue: 100 },
        { name: "AWS", value: 90, maxValue: 100 },
        { name: "Terraform", value: 86, maxValue: 100 },
      ],
    },
  },
];

export const mockArchetypes: TeamArchetype[] = [
  {
    name: "Core",
    description: "The Core archetype focuses on building a team with exceptional individual talent. This approach prioritizes high-quality individual performers who can independently drive projects and decisions.",
    weightings: {
      individual_quality: 0.7,
      team_synergy: 0.2,
      team_diversity: 0.1,
    },
  },
  {
    name: "Synergy",
    description: "The Synergy archetype emphasizes building a cohesive team that works well together. This approach values interpersonal compatibility and collaborative skills, fostering a harmonious work environment.",
    weightings: {
      individual_quality: 0.3,
      team_synergy: 0.5,
      team_diversity: 0.2,
    },
  },
  {
    name: "Diversity",
    description: "The Diversity archetype aims to create a team with a wide range of skills, perspectives, and experiences. This approach seeks to leverage diverse backgrounds to drive innovation and creative problem-solving.",
    weightings: {
      individual_quality: 0.3,
      team_synergy: 0.2,
      team_diversity: 0.5,
    },
  },
];
