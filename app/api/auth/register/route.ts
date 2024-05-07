import prisma from "@/lib/prisma"
import { NextResponse } from "next/server"

export async function POST(req: Request){
    try {
        console.log('register Request')
        const {name, email, password} = await req.json()
        const user = await prisma.user.create({
            data: {
                name, email, password
            }
        })
        return NextResponse.json(user, {status: 201})
    } catch (error) {
        return NextResponse.json({message: 'Error creating user'}, {status: 500})
    }
}

export async function GET(req: Request){
    try {
        const user = await prisma.user.findMany()
        return NextResponse.json(user, {status: 201})
    } catch (error) {
        return NextResponse.json({message: 'Error creating user'}, {status: 500})
    }
}

