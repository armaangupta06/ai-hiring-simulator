// Comprehensive test script to analyze API response structure
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const fs = require('fs');

// Helper function to parse Python-style string representation of arrays
const parsePythonArray = (str) => {
  if (!str || typeof str !== 'string') return [];
  
  // Handle Python list format: "['item1', 'item2']" or "[item1, item2]"
  try {
    // Remove the outer quotes and replace single quotes with double quotes for JSON parsing
    const jsonStr = str
      .replace(/^\[\s*'|'\s*\]$/g, '[') // Remove leading [' and trailing ']
      .replace(/'\s*,\s*'/g, '","')    // Replace ', ' with ","
      .replace(/^\[|\]$/g, '[')        // Ensure it starts with [ and ends with ]
      .replace(/'/g, '"')             // Replace remaining single quotes with double quotes
      .replace(/\]$/, '"]')           // Add closing quote to the last element
      .replace(/\["/, '["')           // Add opening quote to the first element
      .replace(/False/g, 'false')     // Replace Python False with JavaScript false
      .replace(/True/g, 'true');      // Replace Python True with JavaScript true
      
    return JSON.parse(jsonStr);
  } catch (e) {
    console.error('Error parsing Python array:', str, e);
    // Fallback: split by commas and clean up
    return str
      .replace(/^\[|\]$/g, '')  // Remove [ and ]
      .replace(/'/g, '')       // Remove quotes
      .split(',')              // Split by comma
      .map(s => s.trim())      // Trim whitespace
      .filter(Boolean);        // Remove empty strings
  }
};

async function testCandidateScoring() {
  console.log('\nComprehensive API Response Testing');
  console.log('==================================');
  const startTime = Date.now();
  
  // Sample startup description
  const startupDescription = `
    We are a fast-growing fintech startup focused on democratizing access to financial services.
    Our company values innovation, collaboration, and user-centric design. We're looking for
    candidates who are passionate about technology, have strong problem-solving skills, and can
    work in a fast-paced environment. Experience with Python, React, and financial systems is a plus.
  `;
  
  // Request payload with no candidates specified
  const payload = {
    startup_description: startupDescription,
    required_skills: ["Python", "React", "Financial Knowledge"]
  };
  
  try {
    // Make the request directly to the FastAPI backend
    const response = await fetch('http://localhost:8000/api/candidates/score', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    
    const endTime = Date.now();
    console.log(`Request took ${(endTime - startTime) / 1000} seconds`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('Scoring successful!');
    console.log(`Received ${result.scored_candidates.length} candidates`);
    
    // Log the structure of the first candidate to understand its format
    if (result.scored_candidates && result.scored_candidates.length > 0) {
      const firstCandidate = result.scored_candidates[0];
      
      console.log('\n=== FIRST CANDIDATE ANALYSIS ===');
      
      // Analyze skills property
      console.log('\n1. Skills Property:');
      console.log('Type:', typeof firstCandidate.skills);
      console.log('Is Array:', Array.isArray(firstCandidate.skills));
      console.log('Raw Value:', firstCandidate.skills);
      
      // Try parsing the skills if it's a string
      if (typeof firstCandidate.skills === 'string') {
        const parsedSkills = parsePythonArray(firstCandidate.skills);
        console.log('Parsed Skills:', parsedSkills);
      }
      
      // Analyze work_experiences property
      console.log('\n2. Work Experiences Property:');
      console.log('Type:', typeof firstCandidate.work_experiences);
      console.log('Is Array:', Array.isArray(firstCandidate.work_experiences));
      console.log('Raw Value:', firstCandidate.work_experiences);
      
      // Try parsing the work_experiences if it's a string
      if (typeof firstCandidate.work_experiences === 'string') {
        try {
          // This is more complex, might need a more sophisticated parser
          console.log('Work experiences appears to be a string representation of a Python list of dictionaries');
        } catch (e) {
          console.error('Error parsing work_experiences:', e);
        }
      }
      
      // Analyze education.degrees property
      console.log('\n3. Education Degrees Property:');
      if (firstCandidate.education && firstCandidate.education.degrees) {
        console.log('Type:', typeof firstCandidate.education.degrees);
        console.log('Is Array:', Array.isArray(firstCandidate.education.degrees));
        console.log('Raw Value:', firstCandidate.education.degrees);
      } else {
        console.log('Education degrees property not found');
      }
      
      // Analyze all rating properties
      console.log('\n4. Rating Properties:');
      
      // Raw scores (0-1 range)
      console.log('\nRaw scores (0-1 range):');
      console.log('normalized_overall_score:', firstCandidate.normalized_overall_score);
      console.log('technical_score:', firstCandidate.technical_score);
      console.log('education_score:', firstCandidate.education_score);
      console.log('soft_skills_score:', firstCandidate.soft_skills_score);
      console.log('culture_fit_score:', firstCandidate.culture_fit_score);
      
      // Z-normalized scores (usually 0-100 range)
      console.log('\nZ-normalized scores (0-100 range):');
      console.log('z_normalized_score:', firstCandidate.z_normalized_score);
      console.log('z_normalized_technical:', firstCandidate.z_normalized_technical);
      console.log('z_normalized_education:', firstCandidate.z_normalized_education);
      console.log('z_normalized_soft_skills:', firstCandidate.z_normalized_soft_skills);
      console.log('z_normalized_culture_fit:', firstCandidate.z_normalized_culture_fit);
      
      // Test our transformation function
      console.log('\n5. Testing Transformation Function:');
      
      // Create the ratings object expected by the frontend
      const ratings = {
        overall: Math.round(firstCandidate.z_normalized_score || (firstCandidate.normalized_overall_score || 0) * 100),
        technical: Math.round(firstCandidate.z_normalized_technical || (firstCandidate.technical_score || 0) * 100),
        education: Math.round(firstCandidate.z_normalized_education || (firstCandidate.education_score || 0) * 100),
        softSkills: Math.round(firstCandidate.z_normalized_soft_skills || (firstCandidate.soft_skills_score || 0) * 100),
        cultureFit: Math.round(firstCandidate.z_normalized_culture_fit || (firstCandidate.culture_fit_score || 0) * 100),
      };
      
      console.log('Transformed Ratings:', ratings);
      
      // Parse skills
      let skills = firstCandidate.skills || [];
      if (typeof skills === 'string') {
        skills = parsePythonArray(skills);
      } else if (!Array.isArray(skills)) {
        skills = [];
      }
      
      console.log('Transformed Skills:', skills);
      
      // Create a transformed candidate object
      const transformedCandidate = {
        ...firstCandidate,
        skills,
        ratings
      };
      
      // Save the full candidate structure to a file for inspection
      fs.writeFileSync('raw-candidate.json', JSON.stringify(firstCandidate, null, 2));
      fs.writeFileSync('transformed-candidate.json', JSON.stringify(transformedCandidate, null, 2));
      console.log('\nRaw and transformed candidate structures saved to JSON files');
    }
    
    return result;
  } catch (error) {
    console.error('Error testing candidate scoring:', error);
    return null;
  }
}

// Run the test
testCandidateScoring();
