/**
 * Test script to verify the API responses in the frontend
 * This replicates the functionality of test_default_candidates.py
 */

// Function to test the candidate scoring endpoint
async function testCandidateScoring() {
  console.log('\nTesting candidate scoring with default candidates...');
  const startTime = Date.now();
  
  // Sample startup description (same as in Python test)
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
    // Make the request
    const response = await fetch('/api/candidates/score', {
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
    console.log('API Response Structure:', result);
    
    // Log the structure of the first candidate to understand its format
    if (result.scored_candidates && result.scored_candidates.length > 0) {
      console.log('\nFirst candidate structure:');
      const firstCandidate = result.scored_candidates[0];
      console.log(JSON.stringify(firstCandidate, null, 2));
      
      // Specifically check the skills property
      console.log('\nSkills property type:', typeof firstCandidate.skills);
      console.log('Skills property value:', firstCandidate.skills);
      console.log('Is skills an array?', Array.isArray(firstCandidate.skills));
    }
    
    return result;
  } catch (error) {
    console.error('Error testing candidate scoring:', error);
    return null;
  }
}

// Function to run all tests
async function runTests() {
  console.log('Starting API tests...');
  
  // Test candidate scoring
  const scoringResult = await testCandidateScoring();
  
  console.log('\nTests completed!');
}

// Export the test functions
export { testCandidateScoring, runTests };
