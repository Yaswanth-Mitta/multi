import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

function getPublicIP() {
  try {
    const envPath = path.join(process.cwd(), '..', '.env')
    const envContent = fs.readFileSync(envPath, 'utf8')
    const match = envContent.match(/PUBLIC_IP=(.+)/)
    return match ? match[1].trim() : 'localhost'
  } catch {
    return 'localhost'
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

    const publicIP = getPublicIP()
    const backendUrl = `http://${publicIP}:8000`
    
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