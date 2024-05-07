import { currentUser } from "@/lib/current-user"
import prisma from "@/lib/prisma"
import { NextResponse } from "next/server"

export async function POST(req: Request){
  try {
    const user = await currentUser()
    if(!user){
      return new NextResponse('Unauthorized', {status: 401})
    }

    const chat = await prisma.chat.create({
      data: {
        userId: user.id,
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