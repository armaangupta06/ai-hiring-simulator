"use client";

import { useState, useEffect } from 'react';
import { testCandidateScoring } from '@/test_api';

export default function TestPage() {
  const [testResults, setTestResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runTest = async () => {
    setLoading(true);
    setError(null);
    try {
      const results = await testCandidateScoring();
      setTestResults(results);
      console.log('Test completed successfully');
    } catch (err) {
      console.error('Test failed:', err);
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
      
      <button 
        onClick={runTest}
        disabled={loading}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4"
      >
        {loading ? 'Running Test...' : 'Run API Test'}
      </button>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p><strong>Error:</strong> {error}</p>
        </div>
      )}
      
      {testResults && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">Test Results</h2>
          
          <div className="bg-gray-100 p-4 rounded">
            <h3 className="font-medium mb-2">API Response Summary:</h3>
            <p>Number of candidates: {testResults.scored_candidates?.length || 0}</p>
            <p>Includes cultural fit: {testResults.includes_cultural_fit ? 'Yes' : 'No'}</p>
          </div>
          
          {testResults.scored_candidates && testResults.scored_candidates.length > 0 && (
            <div className="mt-4">
              <h3 className="font-medium mb-2">First Candidate Data:</h3>
              <div className="bg-gray-100 p-4 rounded overflow-auto max-h-96">
                <pre>{JSON.stringify(testResults.scored_candidates[0], null, 2)}</pre>
              </div>
              
              <div className="mt-4">
                <h3 className="font-medium mb-2">Skills Property Analysis:</h3>
                <div className="bg-gray-100 p-4 rounded">
                  <p>Type: {typeof testResults.scored_candidates[0].skills}</p>
                  <p>Is Array: {Array.isArray(testResults.scored_candidates[0].skills) ? 'Yes' : 'No'}</p>
                  <p>Value: {JSON.stringify(testResults.scored_candidates[0].skills)}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
