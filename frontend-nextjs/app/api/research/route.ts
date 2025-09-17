import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

function getBackendURL() {
  try {
    const envPath = path.join(process.cwd(), '..', '.env')
    const envContent = fs.readFileSync(envPath, 'utf8')
    const match = envContent.match(/PUBLIC_IP=(.+)/)
    const ip = match ? match[1].trim() : process.env.PUBLIC_IP || 'localhost'
    return `http://${ip}:8000`
  } catch {
    return `http://${process.env.PUBLIC_IP || 'localhost'}:8000`
  }
}

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json()
    
    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      )
    }

    const backendUrl = getBackendURL()
    
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
    return NextResponse.json(
      { error: 'Failed to connect to backend' },
      { status: 500 }
    )
  }
}