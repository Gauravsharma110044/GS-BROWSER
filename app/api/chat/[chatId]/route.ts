import { currentUser } from "@/lib/current-user"
import prisma from "@/lib/prisma"
import { NextResponse } from "next/server"


export async function DELETE(req:Request, {params}: {params: {chatId: string}}){
  try {
    const user = await currentUser()
    if(!user){
      return new NextResponse('Unauthorized', {status: 401})
    }

    if(!params.chatId){
      return new NextResponse('chatId not provided', {status: 401})
    }

    const chat = await prisma.chat.delete({
      where: {
        id: params.chatId,
        userId: user.id
      }
    })

    return NextResponse.json(chat)
  } catch (error) {
    console.log(error)
    return NextResponse.json({message: 'Error deleting chat'}, {status: 500})
  }  
}