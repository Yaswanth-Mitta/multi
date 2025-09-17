import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json()
    
    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      )
    }

    // Replace this URL with your Python backend endpoint
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
    
    const response = await fetch(`${backendUrl}/research`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    })

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('API Error:', error)
    
    // Return mock data for development/demo purposes
    return NextResponse.json({
      query: request.body?.query || 'Sample query',
      marketAnalysis: {
        summary: "Based on current market trends and competitive analysis, this product shows strong potential in the market with favorable positioning against competitors.",
        trends: [
          "Increasing demand for high-performance devices",
          "Price-conscious consumer behavior",
          "Growing preference for feature-rich products",
          "Strong online sales growth"
        ],
        competition: "Moderate to high competition with 4-5 major players",
        marketSize: "$3.2B globally with 15% YoY growth"
      },
      purchaseLikelihood: {
        score: 75,
        factors: [
          "Competitive pricing strategy",
          "Strong feature-to-price ratio",
          "Positive market sentiment",
          "Good brand positioning"
        ],
        recommendation: "High likelihood of purchase success with proper marketing strategy"
      },
      sources: [
        { title: "Google Search Market Data", url: "#", type: "search" },
        { title: "Competitive Analysis Report", url: "#", type: "analysis" },
        { title: "Consumer Sentiment Analysis", url: "#", type: "sentiment" },
        { title: "Price Comparison Data", url: "#", type: "pricing" }
      ]
    })
  }
}