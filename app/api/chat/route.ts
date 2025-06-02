import { NextResponse } from 'next/server'
import { GoogleGenerativeAI } from '@google/generative-ai'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/authOptions'
import prisma from '@/lib/prisma'
import { Role } from '@prisma/client'

// Initialize Google Gemini
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || '')

export async function POST(req: Request) {
  try {
    const { message } = await req.json()
    const session = await getServerSession(authOptions)

    if (!session?.user?.email) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Get the Gemini Pro model
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' })

    // Generate response
    const result = await model.generateContent(message)
    const response = await result.response
    const text = response.text()

    // Save the chat message to database
    const user = await prisma.user.findUnique({
      where: { email: session.user.email }
    })

    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 })
    }

    // Create or get the latest chat
    let chat = await prisma.chat.findFirst({
      where: { userId: user.id },
      orderBy: { createdAt: 'desc' }
    })

    if (!chat) {
      chat = await prisma.chat.create({
        data: {
          name: 'New Chat',
          userId: user.id
        }
      })
    }

    // Save the messages
    await prisma.message.createMany({
      data: [
        {
          content: message,
          role: Role.USER,
          chatId: chat.id
        },
        {
          content: text,
          role: Role.MODEL,
          chatId: chat.id
        }
      ]
    })

    return NextResponse.json({ response: text })
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// GET: Return all chats for the authenticated user
export async function GET(req: Request) {
  const session = await getServerSession(authOptions)
  if (!session || !session.user?.email) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  const user = await prisma.user.findUnique({ where: { email: session.user.email } })
  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 })
  }
  const chats = await prisma.chat.findMany({
    where: { userId: user.id },
    orderBy: { createdAt: 'desc' },
    select: { id: true, createdAt: true, updatedAt: true },
  })
  return NextResponse.json(chats)
}