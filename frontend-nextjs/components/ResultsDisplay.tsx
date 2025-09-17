'use client'

import { Brain, Search, FileText, ExternalLink } from 'lucide-react'

interface ResultsProps {
  results: {
    query: string
    marketAnalysis: {
      summary: string
      trends: string[]
      competition: string
      marketSize: string
    }
    sources: Array<{
      title: string
      url: string
      type: string
    }>
  }
}

export default function ResultsDisplay({ results }: ResultsProps) {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Query Summary */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Search className="h-6 w-6 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">Analysis Results</h2>
        </div>
        <p className="text-lg text-primary-600 font-medium">{results.query}</p>
      </div>

      {/* AI Analysis */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Brain className="h-6 w-6 text-primary-600" />
          <h3 className="text-xl font-semibold text-gray-900">AI Research Analysis</h3>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <pre className="whitespace-pre-wrap text-gray-800 font-mono text-sm leading-relaxed">
            {results.marketAnalysis.summary}
          </pre>
        </div>
        
        {results.marketAnalysis.trends && results.marketAnalysis.trends.length > 0 && (
          <div className="mb-4">
            <h4 className="font-medium text-gray-900 mb-3">Key Insights</h4>
            <ul className="space-y-2">
              {results.marketAnalysis.trends.map((trend, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-gray-700">{trend}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Data Sources */}
      {results.sources && results.sources.length > 0 && (
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <FileText className="h-6 w-6 text-primary-600" />
            <h3 className="text-xl font-semibold text-gray-900">Research Sources</h3>
          </div>
          
          <div className="grid gap-3">
            {results.sources.map((source, index) => (
              <a
                key={index}
                href={source.url}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div>
                  <p className="font-medium text-gray-900">{source.title}</p>
                  <p className="text-sm text-gray-500 capitalize">{source.type}</p>
                </div>
                <ExternalLink className="h-4 w-4 text-gray-400" />
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}