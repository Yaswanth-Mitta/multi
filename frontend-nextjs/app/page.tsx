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
      const response = await fetch('/api/research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
      
      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`Server error: ${response.status} - ${errorText}`)
      }
      
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Search error:', error)
      setResults(null)
      alert('Failed to connect to backend. Please check if the server is running and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-8 max-w-7xl">
      <Header />
      
      <div className="max-w-4xl mx-auto overflow-hidden">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            AI-Powered
            <span className="text-primary-600 block">Research Agent</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get comprehensive product analysis and market insights using advanced AI research agents.
          </p>
        </div>

        <SearchForm onSearch={handleSearch} loading={loading} />
        
        {results && (
          <ResultsDisplay 
            results={results} 
            onRefresh={async () => {
              setLoading(true)
              setResults(null)
              await new Promise(resolve => setTimeout(resolve, 100))
              setLoading(false)
              window.scrollTo({ top: 0, behavior: 'smooth' })
            }} 
          />
        )}
        
        {!results && <Features />}
      </div>
    </main>
  )
}