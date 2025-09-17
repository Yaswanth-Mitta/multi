'use client'

import { TrendingUp, ShoppingCart, BarChart3, ExternalLink, CheckCircle } from 'lucide-react'

interface ResultsProps {
  results: {
    query: string
    marketAnalysis: {
      summary: string
      trends: string[]
      competition: string
      marketSize: string
    }
    purchaseLikelihood: {
      score: number
      factors: string[]
      recommendation: string
    }
    sources: Array<{
      title: string
      url: string
      type: string
    }>
  }
}

export default function ResultsDisplay({ results }: ResultsProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50'
    if (score >= 60) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'High'
    if (score >= 60) return 'Medium'
    return 'Low'
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Query Summary */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Analysis for:</h2>
        <p className="text-lg text-primary-600 font-medium">{results.query}</p>
      </div>

      {/* Purchase Likelihood Score */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <ShoppingCart className="h-6 w-6 text-primary-600" />
          <h3 className="text-xl font-semibold text-gray-900">Purchase Likelihood</h3>
        </div>
        
        <div className="flex items-center space-x-4 mb-4">
          <div className={`text-3xl font-bold px-4 py-2 rounded-lg ${getScoreColor(results.purchaseLikelihood.score)}`}>
            {results.purchaseLikelihood.score}%
          </div>
          <div>
            <p className="text-lg font-medium text-gray-900">
              {getScoreLabel(results.purchaseLikelihood.score)} Likelihood
            </p>
            <p className="text-gray-600">{results.purchaseLikelihood.recommendation}</p>
          </div>
        </div>

        <div className="space-y-2">
          <h4 className="font-medium text-gray-900">Key Factors:</h4>
          {results.purchaseLikelihood.factors.map((factor, index) => (
            <div key={index} className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="text-gray-700">{factor}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Market Analysis */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <TrendingUp className="h-6 w-6 text-primary-600" />
          <h3 className="text-xl font-semibold text-gray-900">Market Analysis</h3>
        </div>
        
        <p className="text-gray-700 mb-6">{results.marketAnalysis.summary}</p>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Market Trends</h4>
            <ul className="space-y-2">
              {results.marketAnalysis.trends.map((trend, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-gray-700">{trend}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-900">Competition Level</h4>
              <p className="text-gray-700">{results.marketAnalysis.competition}</p>
            </div>
            <div>
              <h4 className="font-medium text-gray-900">Market Size</h4>
              <p className="text-gray-700">{results.marketAnalysis.marketSize}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Sources */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <BarChart3 className="h-6 w-6 text-primary-600" />
          <h3 className="text-xl font-semibold text-gray-900">Data Sources</h3>
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
    </div>
  )
}