import { NextResponse } from 'next/server';

// FastAPI backend URL
const API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

export async function POST(request: Request) {
  try {
    // Get the request body
    const body = await request.json();

    // Forward the request to the FastAPI backend
    const response = await fetch(`${API_URL}/api/teams/optimize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    // Check if the request was successful
    if (!response.ok) {
      return NextResponse.json(
        { error: `Failed to optimize team: ${response.statusText}` },
        { status: response.status }
      );
    }

    // Return the response from the backend
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error optimizing team:', error);
    return NextResponse.json(
      { error: 'Failed to optimize team' },
      { status: 500 }
    );
  }
}
