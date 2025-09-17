'use client'

import { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'

interface SearchFormProps {
  onSearch: (query: string) => void
  loading: boolean
}

export default function SearchForm({ onSearch, loading }: SearchFormProps) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim())
    }
  }

  const exampleQueries = [
    "mobile with 8gb ram, hd camera at 40000k",
    "laptop with 16gb ram under 50000",
    "wireless headphones with noise cancellation"
  ]

  return (
    <div className="card mb-8">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your product query (e.g., mobile with 8gb ram, hd camera at 40000k)"
            className="input-field pl-12 text-lg"
            disabled={loading}
          />
        </div>
        
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="btn-primary w-full py-4 text-lg flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Search className="h-5 w-5" />
              <span>Analyze Product</span>
            </>
          )}
        </button>
      </form>
      
      <div className="mt-6">
        <p className="text-sm text-gray-500 mb-3">Try these examples:</p>
        <div className="flex flex-wrap gap-2">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              onClick={() => setQuery(example)}
              className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-full transition-colors"
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}