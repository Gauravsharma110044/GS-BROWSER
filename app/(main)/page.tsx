import { getServerSession } from 'next-auth'
import React from 'react'
import { redirect } from 'next/navigation'
import { authOptions } from '../api/auth/[...nextauth]/route'
import Home from '@/components/Home'

const page = async () => {
  const session = await getServerSession(authOptions)
  if(!session){
    return redirect('/login')
  }
  return (
    <div>
      chat
      <Home />
    </div>
  )
}

export default page
