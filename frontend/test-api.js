// Simple script to test the API response structure
// Using CommonJS syntax for Node.js
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const fs = require('fs');

async function testCandidateScoring() {
  console.log('\nTesting candidate scoring with default candidates...');
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
    
    // Log the structure of the first candidate to understand its format
    if (result.scored_candidates && result.scored_candidates.length > 0) {
      console.log('\nFirst candidate structure:');
      const firstCandidate = result.scored_candidates[0];
      
      // Log specific properties we're interested in
      console.log('\nSkills property:');
      console.log('Type:', typeof firstCandidate.skills);
      console.log('Is Array:', Array.isArray(firstCandidate.skills));
      console.log('Value:', firstCandidate.skills);
      
      console.log('\nRating properties:');
      // Raw scores (0-1 range)
      console.log('Raw scores (0-1 range):');
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
      
      // Test the get approach mentioned by the user
      console.log('\nUsing get approach for scores:');
      const overall = firstCandidate.z_normalized_score || (firstCandidate.normalized_overall_score * 100);
      const technical = firstCandidate.z_normalized_technical || (firstCandidate.technical_score * 100);
      const education = firstCandidate.z_normalized_education || (firstCandidate.education_score * 100);
      const softSkills = firstCandidate.z_normalized_soft_skills || (firstCandidate.soft_skills_score * 100);
      const cultureFit = firstCandidate.z_normalized_culture_fit || (firstCandidate.culture_fit_score * 100);
      
      console.log('overall:', overall);
      console.log('technical:', technical);
      console.log('education:', education);
      console.log('softSkills:', softSkills);
      console.log('cultureFit:', cultureFit);
      
      // Save the full candidate structure to a file for inspection
      fs.writeFileSync('candidate-structure.json', JSON.stringify(firstCandidate, null, 2));
      console.log('\nFull candidate structure saved to candidate-structure.json');
    }
    
    return result;
  } catch (error) {
    console.error('Error testing candidate scoring:', error);
    return null;
  }
}

// Run the test
testCandidateScoring();
