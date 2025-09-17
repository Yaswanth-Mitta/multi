'use client'

import { useState } from 'react'
import { Search, TrendingUp, ShoppingCart, Zap, Brain, BarChart3 } from 'lucide-react'
import SearchForm from '@/components/SearchForm'
import ResultsDisplay from '@/components/ResultsDisplay'
import Header from '@/components/Header'
import Features from '@/components/Features'

export default function Home() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (query: string) => {
    setLoading(true)
    try {
      // Replace with your backend API endpoint
      const response = await fetch('/api/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch results')
      }
      
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Search error:', error)
      // Mock data for demo
      setResults({
        query,
        marketAnalysis: {
          summary: "Based on current market trends, this product shows strong potential in the competitive landscape.",
          trends: ["High demand for premium features", "Growing market segment", "Competitive pricing advantage"],
          competition: "Moderate competition with 3-4 major players",
          marketSize: "$2.5B globally"
        },
        purchaseLikelihood: {
          score: 78,
          factors: ["Competitive pricing", "Strong feature set", "Positive reviews"],
          recommendation: "High likelihood of purchase success"
        },
        sources: [
          { title: "Market Research Report", url: "#", type: "report" },
          { title: "Consumer Reviews Analysis", url: "#", type: "reviews" },
          { title: "Competitor Analysis", url: "#", type: "analysis" }
        ]
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <Header />
      
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            AI-Powered
            <span className="text-primary-600 block">Market Research</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get comprehensive market analysis and purchase likelihood assessments for any product using advanced AI research agents.
          </p>
        </div>

        <SearchForm onSearch={handleSearch} loading={loading} />
        
        {results && <ResultsDisplay results={results} />}
        
        {!results && <Features />}
      </div>
    </main>
  )
}