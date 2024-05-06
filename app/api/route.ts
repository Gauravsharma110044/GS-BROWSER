import prisma from "@/lib/prisma"
import { NextResponse } from "next/server"

export async function GET(req: Request){
  try {
    const chats = await prisma.chat.findMany()
    return NextResponse.json(chats) 
  } catch (error) {
    return NextResponse.json({message: 'Error fetching chats'}, {status: 500})
  }
}