'use client'

import { Brain, Search, FileText, ExternalLink } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

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
        <p className="text-lg text-primary-600 font-medium bg-primary-50 px-4 py-2 rounded-lg">
          {results.query}
        </p>
      </div>

      {/* AI Analysis */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <Brain className="h-6 w-6 text-primary-600" />
          <h3 className="text-xl font-semibold text-gray-900">AI Research Analysis</h3>
        </div>
        
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="prose prose-gray max-w-none">
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({children}) => <h1 className="text-2xl font-bold text-gray-900 mb-4 border-b pb-2">{children}</h1>,
                h2: ({children}) => <h2 className="text-xl font-semibold text-gray-800 mb-3 mt-6">{children}</h2>,
                h3: ({children}) => <h3 className="text-lg font-medium text-gray-700 mb-2 mt-4">{children}</h3>,
                p: ({children}) => <p className="text-gray-700 mb-3 leading-relaxed">{children}</p>,
                ul: ({children}) => <ul className="list-disc list-inside mb-4 space-y-1 text-gray-700">{children}</ul>,
                ol: ({children}) => <ol className="list-decimal list-inside mb-4 space-y-1 text-gray-700">{children}</ol>,
                li: ({children}) => <li className="mb-1">{children}</li>,
                strong: ({children}) => <strong className="font-semibold text-gray-900">{children}</strong>,
                em: ({children}) => <em className="italic text-gray-600">{children}</em>,
                code: ({children}) => <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono text-gray-800">{children}</code>,
                pre: ({children}) => <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto mb-4">{children}</pre>,
                blockquote: ({children}) => <blockquote className="border-l-4 border-primary-500 pl-4 italic text-gray-600 mb-4">{children}</blockquote>,
                table: ({children}) => <table className="min-w-full border-collapse border border-gray-300 mb-4">{children}</table>,
                th: ({children}) => <th className="border border-gray-300 px-4 py-2 bg-gray-50 font-semibold text-left">{children}</th>,
                td: ({children}) => <td className="border border-gray-300 px-4 py-2">{children}</td>,
                hr: () => <hr className="my-6 border-gray-300" />,
                a: ({href, children}) => <a href={href} className="text-primary-600 hover:text-primary-700 underline" target="_blank" rel="noopener noreferrer">{children}</a>
              }}
            >
              {results.marketAnalysis.summary}
            </ReactMarkdown>
          </div>
        </div>
        
        {results.marketAnalysis.trends && results.marketAnalysis.trends.length > 0 && (
          <div className="mt-6">
            <h4 className="font-medium text-gray-900 mb-3">Key Insights</h4>
            <div className="grid gap-2">
              {results.marketAnalysis.trends.map((trend, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-gray-700">{trend}</span>
                </div>
              ))}
            </div>
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
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border border-gray-200 hover:shadow-md transition-all"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-primary-500 rounded-full"></div>
                  <div>
                    <p className="font-medium text-gray-900">{source.title}</p>
                    <p className="text-sm text-gray-500">{source.type}</p>
                  </div>
                </div>
                <ExternalLink className="h-4 w-4 text-gray-400" />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}