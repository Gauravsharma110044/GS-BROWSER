import { currentUser } from "@/lib/current-user"
import prisma from "@/lib/prisma"
import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/authOptions"

export async function POST(req: Request){
  try {
    const user = await currentUser()
    if(!user){
      return new NextResponse('Unauthorized', {status: 401})
    }

    const session = await getServerSession(authOptions)

    if (!session) {
      return new NextResponse('Unauthorized', { status: 401 })
    }

    const { user: sessionUser } = session

    const chat = await prisma.chat.create({
      data: {
        userId: sessionUser.id,
        name: 'New Chat'
      }
    })
    if(!chat){
      return new NextResponse('Failed to create new chat', {status: 400})
    }
    return NextResponse.json(chat)
  } catch (error) {
    console.log(error)
    return NextResponse.json({message: 'Error creating chats'}, {status: 500})
  }
}