import { getServerSession } from "next-auth"
import React from "react"
import {authOptions} from '@/lib/authOptions'
import { redirect } from "next/navigation"

export default async function AuthLayout({children}: {children: React.ReactNode}){
    const session = await getServerSession(authOptions)
    if(session){
        redirect('/')
    }
    return (
        <div className="flex justify-center items-center pt-[12rem]">
            {children}
        </div>
    )
}